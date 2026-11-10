"""CS3 Project Lab 2: Atlas A2 completion problem reference solution.

Implements core validation, cryptographic hashing, and as-of SQL querying
for the Atlas A2 data layer store.
Data: SIMULATED Treasury and FRED records.
"""

from __future__ import annotations

import datetime
import hashlib
import re
import sqlite3

_ISO_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def validate_iso_timestamp(ts: str, field_name: str = "timestamp") -> None:
    """Validate that ts is an ISO 8601 UTC timestamp with trailing Z."""
    if not isinstance(ts, str) or not _ISO_TIMESTAMP_RE.match(ts):
        raise ValueError(f"Field '{field_name}' must be YYYY-MM-DDTHH:MM:SSZ")
    try:
        datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.UTC)
    except ValueError as exc:
        raise ValueError(f"Field '{field_name}' has invalid date/time") from exc


def compute_payload_digest(payload: bytes) -> str:
    """Compute lowercase hex SHA-256 digest of exact payload bytes."""
    return hashlib.sha256(payload).hexdigest()


def execute_asof_query(conn: sqlite3.Connection, source: str, series: str, query_time: str) -> dict[str, str] | None:
    """Query the most recent observation prior to or at query_time."""
    validate_iso_timestamp(query_time, "t")
    cur = conn.execute(
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
        (source, series, query_time, query_time),
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


def main() -> None:
    # 1. Validation check
    valid_ts = "2020-03-15T16:30:00Z"
    validate_iso_timestamp(valid_ts)
    print(f"Timestamp '{valid_ts}' is valid: True")

    # 2. Cryptographic digest check
    fixture_bytes = b"date,DGS10\n2020-03-01,1.15\n"
    digest = compute_payload_digest(fixture_bytes)
    print(f"Payload digest: {digest}")
    assert digest == hashlib.sha256(fixture_bytes).hexdigest()

    # 3. As-of query check on in-memory SQLite database
    conn = sqlite3.connect(":memory:")
    with conn:
        conn.execute(
            """
            CREATE TABLE observations (
                seq INTEGER PRIMARY KEY AUTOINCREMENT,
                manifest_seq INTEGER,
                source TEXT,
                series TEXT,
                date TEXT,
                value TEXT,
                retrieved TEXT
            )
            """
        )
        conn.execute(
            "INSERT INTO observations VALUES (1, 1, 'fred', 'DGS10', '2020-03-01', '1.15', '2020-03-02T10:00:00Z')"
        )
        conn.execute(
            "INSERT INTO observations VALUES (2, 2, 'fred', 'DGS10', '2020-03-05', '1.20', '2020-03-06T10:00:00Z')"
        )

    res_early = execute_asof_query(conn, "fred", "DGS10", "2020-03-04T00:00:00Z")
    res_late = execute_asof_query(conn, "fred", "DGS10", "2020-03-10T00:00:00Z")

    print(f"As-of query at 2020-03-04: {res_early}")
    print(f"As-of query at 2020-03-10: {res_late}")

    assert res_early is not None and res_early["date"] == "2020-03-01"
    assert res_late is not None and res_late["date"] == "2020-03-05"
    print("Completion lab solution verified: True")
    conn.close()


if __name__ == "__main__":
    main()
