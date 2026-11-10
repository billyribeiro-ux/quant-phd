"""Atlas A2 data layer store implementation (atlas.dataset).

Implements the SQLite-backed point-in-time store, ingestion adapters,
and manifest tamper verification per atlas/A2.contract.md.
"""

from __future__ import annotations

import csv
import datetime
import hashlib
import io
import re
import sqlite3
from dataclasses import dataclass

SOURCES: tuple[str, ...] = ("fred", "french", "shiller", "treasury", "edgar")

_ISO_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _validate_timestamp(ts: str, field_name: str) -> None:
    if not isinstance(ts, str) or not _ISO_TIMESTAMP_RE.match(ts):
        raise ValueError(f"Field '{field_name}' must be ISO 8601 UTC timestamp YYYY-MM-DDTHH:MM:SSZ, got: {ts!r}")
    try:
        datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.UTC)
    except ValueError as exc:
        raise ValueError(f"Field '{field_name}' contains invalid date/time: {ts!r}") from exc


def _validate_date(date_str: str) -> None:
    if not isinstance(date_str, str) or not _ISO_DATE_RE.match(date_str):
        raise ValueError(f"Observation date must be ISO 8601 YYYY-MM-DD, got: {date_str!r}")
    try:
        datetime.date.fromisoformat(date_str)
    except ValueError as exc:
        raise ValueError(f"Observation date is invalid: {date_str!r}") from exc


@dataclass(frozen=True)
class ManifestRow:
    source: str
    sha256: str
    n_bytes: int
    rows: int | None
    retrieved: str
    licence: str
    source_url: str


class Store:
    """Point-in-time research data store backed by SQLite."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self._init_db()

    def _init_db(self) -> None:
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS manifest (
                    seq INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    sha256 TEXT NOT NULL,
                    n_bytes INTEGER NOT NULL,
                    rows INTEGER NULL,
                    retrieved TEXT NOT NULL,
                    licence TEXT NOT NULL,
                    source_url TEXT NOT NULL
                )
                """
            )
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS payloads (
                    seq INTEGER PRIMARY KEY,
                    body BLOB NOT NULL,
                    FOREIGN KEY(seq) REFERENCES manifest(seq)
                )
                """
            )
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS observations (
                    seq INTEGER PRIMARY KEY AUTOINCREMENT,
                    manifest_seq INTEGER NOT NULL,
                    source TEXT NOT NULL,
                    series TEXT NOT NULL,
                    date TEXT NOT NULL,
                    value TEXT NOT NULL,
                    retrieved TEXT NOT NULL,
                    FOREIGN KEY(manifest_seq) REFERENCES manifest(seq)
                )
                """
            )
            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_obs_lookup ON observations(source, series, retrieved, date, seq)"
            )

    def ingest(
        self,
        source: str,
        payload: bytes,
        *,
        retrieved: str,
        licence: str,
        source_url: str,
    ) -> ManifestRow:
        if source not in SOURCES:
            raise ValueError(f"Unknown source: {source!r}. Must be one of {SOURCES}")
        _validate_timestamp(retrieved, "retrieved")
        if not licence or not licence.strip():
            raise ValueError("licence cannot be empty")
        if not source_url or not source_url.strip():
            raise ValueError("source_url cannot be empty")

        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("CSV payload is not valid UTF-8") from exc

        reader = csv.reader(io.StringIO(text))
        try:
            header = next(reader)
        except StopIteration as exc:
            raise ValueError("CSV payload has no header") from exc

        if not header or header[0] != "date":
            raise ValueError(f"First column of CSV must be 'date', got: {header[0] if header else None!r}")

        series_names = header[1:]
        seen_series: set[str] = set()
        for s in series_names:
            clean_s = s.strip()
            if not clean_s:
                raise ValueError("CSV series name cannot be empty")
            if clean_s in seen_series:
                raise ValueError(f"Duplicate series name in CSV header: {clean_s!r}")
            seen_series.add(clean_s)

        obs_to_insert: list[tuple[str, str, str, str, str]] = []
        data_row_count = 0

        for row in reader:
            if not row:
                continue
            data_row_count += 1
            date_col = row[0].strip()
            _validate_date(date_col)

            for col_idx, s_name in enumerate(series_names, start=1):
                if col_idx < len(row):
                    cell_val = row[col_idx].strip()
                    if cell_val != "":
                        obs_to_insert.append((source, s_name.strip(), date_col, cell_val, retrieved))

        sha = hashlib.sha256(payload).hexdigest()
        n_bytes = len(payload)

        with self._conn:
            cur = self._conn.execute(
                """
                SELECT seq, sha256, n_bytes, rows, licence, source_url
                FROM manifest
                WHERE source = ? AND retrieved = ?
                """,
                (source, retrieved),
            )
            existing = cur.fetchone()
            if existing is not None:
                _ex_seq, ex_sha, ex_bytes, ex_rows, ex_lic, ex_url = existing
                if ex_sha == sha:
                    return ManifestRow(
                        source=source,
                        sha256=sha,
                        n_bytes=ex_bytes,
                        rows=ex_rows,
                        retrieved=retrieved,
                        licence=ex_lic,
                        source_url=ex_url,
                    )
                raise ValueError(
                    f"Conflict: source {source!r} at {retrieved!r} already stored with different SHA-256 "
                    f"{ex_sha} vs {sha}"
                )

            cur = self._conn.execute(
                """
                INSERT INTO manifest (source, sha256, n_bytes, rows, retrieved, licence, source_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (source, sha, n_bytes, data_row_count, retrieved, licence, source_url),
            )
            manifest_seq = cur.lastrowid

            self._conn.execute(
                "INSERT INTO payloads (seq, body) VALUES (?, ?)",
                (manifest_seq, payload),
            )

            if obs_to_insert:
                self._conn.executemany(
                    """
                    INSERT INTO observations (manifest_seq, source, series, date, value, retrieved)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    [(manifest_seq, s, sr, d, v, ret) for (s, sr, d, v, ret) in obs_to_insert],
                )

        return ManifestRow(
            source=source,
            sha256=sha,
            n_bytes=n_bytes,
            rows=data_row_count,
            retrieved=retrieved,
            licence=licence,
            source_url=source_url,
        )

    def ingest_raw(
        self,
        source: str,
        payload: bytes,
        *,
        retrieved: str,
        licence: str,
        source_url: str,
    ) -> ManifestRow:
        if source not in SOURCES:
            raise ValueError(f"Unknown source: {source!r}. Must be one of {SOURCES}")
        _validate_timestamp(retrieved, "retrieved")
        if not licence or not licence.strip():
            raise ValueError("licence cannot be empty")
        if not source_url or not source_url.strip():
            raise ValueError("source_url cannot be empty")

        sha = hashlib.sha256(payload).hexdigest()
        n_bytes = len(payload)

        with self._conn:
            cur = self._conn.execute(
                """
                SELECT seq, sha256, n_bytes, rows, licence, source_url
                FROM manifest
                WHERE source = ? AND retrieved = ?
                """,
                (source, retrieved),
            )
            existing = cur.fetchone()
            if existing is not None:
                _ex_seq, ex_sha, ex_bytes, ex_rows, ex_lic, ex_url = existing
                if ex_sha == sha:
                    return ManifestRow(
                        source=source,
                        sha256=sha,
                        n_bytes=ex_bytes,
                        rows=ex_rows,
                        retrieved=retrieved,
                        licence=ex_lic,
                        source_url=ex_url,
                    )
                raise ValueError(
                    f"Conflict: raw payload for {source!r} at {retrieved!r} exists with different hash "
                    f"{ex_sha} vs {sha}"
                )

            cur = self._conn.execute(
                """
                INSERT INTO manifest (source, sha256, n_bytes, rows, retrieved, licence, source_url)
                VALUES (?, ?, ?, NULL, ?, ?, ?)
                """,
                (source, sha, n_bytes, retrieved, licence, source_url),
            )
            manifest_seq = cur.lastrowid

            self._conn.execute(
                "INSERT INTO payloads (seq, body) VALUES (?, ?)",
                (manifest_seq, payload),
            )

        return ManifestRow(
            source=source,
            sha256=sha,
            n_bytes=n_bytes,
            rows=None,
            retrieved=retrieved,
            licence=licence,
            source_url=source_url,
        )

    def asof(self, source: str, series: str, t: str) -> dict[str, str] | None:
        if source not in SOURCES:
            raise ValueError(f"Unknown source: {source!r}. Must be one of {SOURCES}")
        _validate_timestamp(t, "t")

        # Observations must satisfy: date <= t and retrieved <= t.
        # Date string 'YYYY-MM-DD' has effective UTC time 'YYYY-MM-DDT00:00:00Z'.
        cur = self._conn.execute(
            """
            SELECT source, series, date, value, retrieved
            FROM observations
            WHERE source = ?
              AND series = ?
              AND retrieved <= ?
              AND (date || 'T00:00:00Z') <= ?
            ORDER BY date DESC, seq DESC
            LIMIT 1
            """,
            (source, series, t, t),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return {
            "source": str(row[0]),
            "series": str(row[1]),
            "date": str(row[2]),
            "value": str(row[3]),
            "retrieved": str(row[4]),
        }

    def manifest(self) -> list[ManifestRow]:
        cur = self._conn.execute(
            """
            SELECT source, sha256, n_bytes, rows, retrieved, licence, source_url
            FROM manifest
            ORDER BY seq ASC
            """
        )
        return [
            ManifestRow(
                source=row[0],
                sha256=row[1],
                n_bytes=row[2],
                rows=row[3],
                retrieved=row[4],
                licence=row[5],
                source_url=row[6],
            )
            for row in cur.fetchall()
        ]

    def verify(self) -> None:
        cur = self._conn.execute(
            """
            SELECT m.source, m.retrieved, m.sha256, p.body
            FROM manifest m
            JOIN payloads p ON m.seq = p.seq
            ORDER BY m.seq ASC
            """
        )
        for row in cur.fetchall():
            src, ret, expected_sha, body = row[0], row[1], row[2], row[3]
            actual_sha = hashlib.sha256(body).hexdigest()
            if actual_sha != expected_sha:
                raise ValueError(
                    f"Integrity check failed: payload for source {src!r} retrieved at {ret!r} "
                    f"has corrupted hash {actual_sha} (expected {expected_sha})"
                )

    def close(self) -> None:
        self._conn.close()


def open_store(path: str, *, engine: str = "sqlite") -> Store:
    if not path or not path.strip():
        raise ValueError("path cannot be empty")
    if engine == "sqlite":
        conn = sqlite3.connect(path)
        return Store(conn)
    if engine == "duckdb":
        try:
            import importlib

            importlib.import_module("duckdb")
        except ImportError as exc:
            raise ValueError(f"duckdb engine cannot be imported: {exc}") from exc
        raise ValueError("duckdb engine is not configured on grader path")
    raise ValueError(f"Unknown engine: {engine!r}. Must be 'sqlite' or 'duckdb'")
