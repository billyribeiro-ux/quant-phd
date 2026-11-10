"""QR1 Project Lab 1: Rung 1 worked example of vintage-aware ingestion engine.

Demonstrates complete implementation and step-by-step verification of
point-in-time vintage indexing, UTC timestamp normalization, prevailing tick
lookups, and corporate action adjustment factor computation.
Data: SIMULATED research data store records.
"""

from __future__ import annotations

import datetime
import re
import sqlite3

_WALL_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})$")


def et_to_utc(wall: str) -> str:
    """Convert Eastern wall-clock time 'YYYY-MM-DD HH:MM' to ISO 8601 UTC 'YYYY-MM-DDTHH:MM:SSZ'."""
    m = _WALL_RE.match(wall)
    if not m:
        raise ValueError(f"Malformed Eastern wall timestamp: {wall!r}")
    year, month, day, hour, minute = map(int, m.groups())
    dt = datetime.datetime(year, month, day, hour, minute)

    # US DST rule: Second Sunday of March to First Sunday of November
    d_mar1 = datetime.date(year, 3, 1)
    sun2_mar = 1 + (6 - d_mar1.weekday()) % 7 + 7
    spring_date = datetime.date(year, 3, sun2_mar)

    d_nov1 = datetime.date(year, 11, 1)
    sun1_nov = 1 + (6 - d_nov1.weekday()) % 7
    fall_date = datetime.date(year, 11, sun1_nov)

    curr_date = dt.date()
    if curr_date == spring_date and 2 <= dt.hour < 3:
        raise ValueError(f"Wall time in spring DST gap does not exist: {wall!r}")

    is_dst = (
        (spring_date < curr_date < fall_date)
        or (curr_date == spring_date and dt.hour >= 3)
        or (curr_date == fall_date and dt.hour < 2)
    )

    offset_hours = -4 if is_dst else -5
    utc_dt = dt - datetime.timedelta(hours=offset_hours)
    return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def adjust_closes(
    dates: list[str],
    closes: list[float],
    events: list[tuple[str, float]],
) -> list[float]:
    """Compute backward-adjusted closes: for date d, divide by product of ratios with ex_date > d."""
    if len(dates) != len(closes):
        raise ValueError("Dates and closes length mismatch")
    for _, ratio in events:
        if ratio <= 0:
            raise ValueError(f"Split ratio must be positive: {ratio}")

    adjusted: list[float] = []
    for d, c in zip(dates, closes, strict=True):
        factor = 1.0
        for ex_date, ratio in events:
            if ex_date > d:
                factor *= ratio
        adjusted.append(c / factor)
    return adjusted


def main() -> None:
    # 1. Verify Timestamp Normalization
    wall_release = "2026-03-12 08:30"
    utc_release = et_to_utc(wall_release)
    print(f"1. Timestamp Normalization: {wall_release} ET -> {utc_release} UTC")

    # 2. In-memory Vintage Database Setup
    conn = sqlite3.connect(":memory:")
    with conn:
        conn.execute(
            """
            CREATE TABLE vintages (
                seq INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                series TEXT NOT NULL,
                obs_date TEXT NOT NULL,
                value TEXT NOT NULL,
                published TEXT NOT NULL,
                retrieved TEXT NOT NULL
            )
            """
        )
        conn.execute("CREATE INDEX idx_vintages ON vintages(source, series, obs_date, published, seq)")

    # 3. Ingest Vintages (Initial advance release, second estimate revision, third estimate revision)
    source = "fred"
    series = "GDP_GROWTH"
    obs_date = "2025-Q4"

    records = [
        (source, series, obs_date, "2.1", "2026-01-29T13:30:00Z", "2026-01-29T13:35:00Z"),
        (source, series, obs_date, "2.4", "2026-02-26T13:30:00Z", "2026-02-26T13:35:00Z"),
        (source, series, obs_date, "2.3", "2026-03-26T13:30:00Z", "2026-03-26T13:35:00Z"),
    ]

    with conn:
        conn.executemany(
            "INSERT INTO vintages (source, series, obs_date, value, published, retrieved) VALUES (?, ?, ?, ?, ?, ?)",
            records,
        )

    print("\n2. Ingested Macro Vintages:")
    for r in records:
        print(f"  Obs {r[2]} published={r[4]} val={r[3]}%")

    # 4. Point-in-time queries
    def query_visible(t: str) -> str | None:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT value FROM vintages
            WHERE source = ? AND series = ? AND obs_date = ? AND published <= ?
            ORDER BY published DESC, seq DESC LIMIT 1
            """,
            (source, series, obs_date, t),
        )
        row = cur.fetchone()
        return row[0] if row else None

    cutoffs = [
        ("2026-01-15T00:00:00Z", "Prior to any publication"),
        ("2026-02-15T00:00:00Z", "Post-Advance release"),
        ("2026-03-15T00:00:00Z", "Post-Second release"),
        ("2026-04-15T00:00:00Z", "Post-Third release"),
    ]

    print("\n3. Point-in-Time Cut-off Queries:")
    for cut_t, label in cutoffs:
        val = query_visible(cut_t)
        print(f"  Cut-off {cut_t} [{label}]: visible={val}")

    # 5. Split Adjustment Check
    dates = ["2026-03-02", "2026-03-03", "2026-03-04", "2026-03-05"]
    closes = [100.0, 100.0, 50.0, 52.0]  # 2:1 split on 2026-03-04
    events = [("2026-03-04", 2.0)]
    adj = adjust_closes(dates, closes, events)

    print("\n4. Corporate Action Adjustment:")
    for d, raw, a in zip(dates, closes, adj, strict=True):
        print(f"  {d}: raw={raw:.1f} adjusted={a:.1f}")

    conn.close()
    print("\nRung 1 worked example completed successfully.")


main()
