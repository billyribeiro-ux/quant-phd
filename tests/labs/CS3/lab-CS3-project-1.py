"""CS3 Project Lab 1: Atlas A2 store worked example.

Walks through initialization of the SQLite point-in-time store, ingestion of
SIMULATED macroeconomic tables, as-of querying, and manifest verification.
"""

from __future__ import annotations

import csv
import hashlib
import io
import re
import sqlite3
from dataclasses import dataclass

SOURCES: tuple[str, ...] = ("fred", "french", "shiller", "treasury", "edgar")
_ISO_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


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
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
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
                    body BLOB NOT NULL
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
                    retrieved TEXT NOT NULL
                )
                """
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
            raise ValueError(f"Unknown source: {source}")
        if not _ISO_TIMESTAMP_RE.match(retrieved):
            raise ValueError("Invalid timestamp")
        text = payload.decode("utf-8")
        reader = csv.reader(io.StringIO(text))
        header = next(reader)
        series_names = header[1:]
        data_rows: list[tuple[int, str, str, str, str, str]] = []
        n_rows = 0

        sha = hashlib.sha256(payload).hexdigest()
        n_bytes = len(payload)

        with self._conn:
            cur = self._conn.execute(
                """
                INSERT INTO manifest (source, sha256, n_bytes, rows, retrieved, licence, source_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (source, sha, n_bytes, 0, retrieved, licence, source_url),
            )
            assert cur.lastrowid is not None
            m_seq = int(cur.lastrowid)
            self._conn.execute("INSERT INTO payloads (seq, body) VALUES (?, ?)", (m_seq, payload))

            for row in reader:
                if not row:
                    continue
                n_rows += 1
                d_str = row[0].strip()
                for idx, s_name in enumerate(series_names, start=1):
                    if idx < len(row) and row[idx].strip():
                        data_rows.append((m_seq, source, s_name.strip(), d_str, row[idx].strip(), retrieved))

            self._conn.execute("UPDATE manifest SET rows = ? WHERE seq = ?", (n_rows, m_seq))
            self._conn.executemany(
                """
                INSERT INTO observations (manifest_seq, source, series, date, value, retrieved)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                data_rows,
            )

        return ManifestRow(source, sha, n_bytes, n_rows, retrieved, licence, source_url)

    def asof(self, source: str, series: str, t: str) -> dict[str, str] | None:
        cur = self._conn.execute(
            """
            SELECT source, series, date, value, retrieved
            FROM observations
            WHERE source = ? AND series = ? AND retrieved <= ? AND (date || 'T00:00:00Z') <= ?
            ORDER BY date DESC, seq DESC LIMIT 1
            """,
            (source, series, t, t),
        )
        r = cur.fetchone()
        if r is None:
            return None
        return {"source": r[0], "series": r[1], "date": r[2], "value": r[3], "retrieved": r[4]}


def main() -> None:
    conn = sqlite3.connect(":memory:")
    store = Store(conn)

    # SIMULATED FRED payload
    fred_csv = b"date,DGS10,FEDFUNDS\n2020-01-10,1.87,1.55\n2020-01-15,1.81,1.55\n2020-01-20,1.82,1.55\n"
    fred_retrieved = "2020-01-25T12:00:00Z"
    licence = "SIMULATED: test licence"
    url = "https://atlas.local/fred"

    row = store.ingest("fred", fred_csv, retrieved=fred_retrieved, licence=licence, source_url=url)
    print(f"Ingested source: {row.source}")
    print(f"Data rows: {row.rows}")
    print(f"SHA-256: {row.sha256}")

    # Query before retrieval: point-in-time check
    ans_early = store.asof("fred", "DGS10", "2020-01-22T00:00:00Z")
    print(f"As-of query at 2020-01-22 (before retrieval): {ans_early}")

    # Query after retrieval: valid observation
    ans_pit = store.asof("fred", "DGS10", "2020-01-30T00:00:00Z")
    print(f"As-of query at 2020-01-30: {ans_pit}")

    assert ans_early is None
    assert ans_pit is not None and ans_pit["value"] == "1.82"
    print("Point-in-time store worked example successfully verified: True")
    conn.close()


main()
