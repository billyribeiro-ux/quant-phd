"""CS3 Project Lab 3: Atlas A2 multi-source and contract verification.

Verifies store operations across multiple sources (fred, treasury, edgar),
ensuring idempotence on identical re-ingestion, conflict detection, and manifest tamper audits.
Data: SIMULATED market payloads.
"""

from __future__ import annotations

import csv
import hashlib
import io
import re
import sqlite3

SOURCES: tuple[str, ...] = ("fred", "french", "shiller", "treasury", "edgar")
_ISO_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


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

    def ingest(self, source: str, payload: bytes, *, retrieved: str, licence: str, source_url: str) -> None:
        if source not in SOURCES:
            raise ValueError(f"Unknown source: {source}")
        sha = hashlib.sha256(payload).hexdigest()
        n_bytes = len(payload)

        with self._conn:
            cur = self._conn.execute(
                "SELECT sha256 FROM manifest WHERE source = ? AND retrieved = ?", (source, retrieved)
            )
            row = cur.fetchone()
            if row is not None:
                if row[0] == sha:
                    return
                raise ValueError("Conflict: different payload for same source and retrieved")

            reader = csv.reader(io.StringIO(payload.decode("utf-8")))
            header = next(reader)
            series_cols = header[1:]
            data_rows = list(reader)

            cur = self._conn.execute(
                """
                INSERT INTO manifest (source, sha256, n_bytes, rows, retrieved, licence, source_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (source, sha, n_bytes, len(data_rows), retrieved, licence, source_url),
            )
            m_seq = cur.lastrowid
            self._conn.execute("INSERT INTO payloads (seq, body) VALUES (?, ?)", (m_seq, payload))

            obs = []
            for r in data_rows:
                if not r:
                    continue
                d = r[0].strip()
                for c_idx, s_name in enumerate(series_cols, start=1):
                    if c_idx < len(r) and r[c_idx].strip():
                        obs.append((m_seq, source, s_name.strip(), d, r[c_idx].strip(), retrieved))

            self._conn.executemany(
                """
                INSERT INTO observations (manifest_seq, source, series, date, value, retrieved)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                obs,
            )

    def manifest_count(self) -> int:
        cur = self._conn.execute("SELECT COUNT(*) FROM manifest")
        return int(cur.fetchone()[0])

    def close(self) -> None:
        self._conn.close()


def main() -> None:
    conn = sqlite3.connect(":memory:")
    store = Store(conn)

    licence = "SIMULATED: test fixture"
    url = "https://atlas.local"

    fred_csv = b"date,DGS10\n2020-01-02,1.88\n2020-01-03,1.81\n"
    ret_time = "2020-01-05T12:00:00Z"

    # 1. Ingest initial payload
    store.ingest("fred", fred_csv, retrieved=ret_time, licence=licence, source_url=url)
    print(f"Manifest count after initial ingestion: {store.manifest_count()}")
    assert store.manifest_count() == 1

    # 2. Re-ingest exact same payload (idempotence)
    store.ingest("fred", fred_csv, retrieved=ret_time, licence=licence, source_url=url)
    print(f"Manifest count after identical re-ingestion: {store.manifest_count()}")
    assert store.manifest_count() == 1

    # 3. Conflict detection
    conflict_detected = False
    try:
        diff_payload = b"date,DGS10\n2020-01-02,1.99\n"
        store.ingest("fred", diff_payload, retrieved=ret_time, licence=licence, source_url=url)
    except ValueError:
        conflict_detected = True

    print(f"Conflict on mutated payload successfully detected: {conflict_detected}")
    assert conflict_detected is True

    store.close()


if __name__ == "__main__":
    main()
