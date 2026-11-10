"""QR1 Project Lab 3: Rung 3 independent project deliverable verification.

Executes comprehensive verification on seed 0 test instance against the
vintage-aware ingestion engine reference implementation.
Data: SIMULATED research data store records.
"""

from __future__ import annotations

import datetime
import re
import sqlite3

_WALL_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})$")


def et_to_utc(wall: str) -> str:
    m = _WALL_RE.match(wall)
    if not m:
        raise ValueError(f"Malformed Eastern wall timestamp: {wall!r}")
    y, mth, d, h, mn = map(int, m.groups())
    dt = datetime.datetime(y, mth, d, h, mn)

    d_mar1 = datetime.date(y, 3, 1)
    sun2_mar = 1 + (6 - d_mar1.weekday()) % 7 + 7
    spring_date = datetime.date(y, 3, sun2_mar)

    d_nov1 = datetime.date(y, 11, 1)
    sun1_nov = 1 + (6 - d_nov1.weekday()) % 7
    fall_date = datetime.date(y, 11, sun1_nov)

    cdate = dt.date()
    if cdate == spring_date and 2 <= dt.hour < 3:
        raise ValueError("Spring DST gap does not exist")

    is_dst = (
        (spring_date < cdate < fall_date)
        or (cdate == spring_date and dt.hour >= 3)
        or (cdate == fall_date and dt.hour < 2)
    )
    offset = datetime.timedelta(hours=-4 if is_dst else -5)
    return (dt - offset).strftime("%Y-%m-%dT%H:%M:%SZ")


def last_trade_at(ticks: list[tuple[str, int, float]], t: str) -> float | None:
    cand = [tick for tick in ticks if tick[0] <= t]
    if not cand:
        return None
    return max(cand, key=lambda x: (x[0], x[1]))[2]


def adjust_closes(dates: list[str], closes: list[float], events: list[tuple[str, float]]) -> list[float]:
    if len(dates) != len(closes):
        raise ValueError("length mismatch")
    for _, r in events:
        if r <= 0:
            raise ValueError("ratio must be positive")
    res: list[float] = []
    for d, c in zip(dates, closes, strict=True):
        f = 1.0
        for ed, r in events:
            if ed > d:
                f *= r
        res.append(c / f)
    return res


def main() -> None:
    # 1. Verification of Seed-0 Anchors
    anchors = [
        ("2026-01-15 12:00", "2026-01-15T17:00:00Z"),
        ("2026-07-01 12:00", "2026-07-01T16:00:00Z"),
    ]
    print("1. Eastern Time to UTC Anchors:")
    for w, exp in anchors:
        act = et_to_utc(w)
        assert act == exp
        print(f"  {w} -> {act} [VERIFIED]")

    # 2. Point-in-time Vintage Ingestion & Query Verification
    conn = sqlite3.connect(":memory:")
    with conn:
        conn.execute(
            """
            CREATE TABLE vintages (
                seq INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT, series TEXT, obs_date TEXT, value TEXT, published TEXT, retrieved TEXT
            )
            """
        )

    # Seed-0 sample vintages
    vintages = [
        ("fred", "CORE_CPI", "2024-01-01", "125.50", "2024-02-15T13:30:00Z", "2024-02-15T13:35:00Z"),
        ("fred", "CORE_CPI", "2024-02-01", "126.80", "2024-03-15T13:30:00Z", "2024-03-15T13:35:00Z"),
        ("fred", "CORE_CPI", "2024-01-01", "125.90", "2024-04-15T13:30:00Z", "2024-04-15T13:40:00Z"),  # Revision
    ]
    with conn:
        conn.executemany(
            "INSERT INTO vintages(source, series, obs_date, value, published, retrieved) VALUES (?,?,?,?,?,?)", vintages
        )

    def query_vis(obs: str, cut: str) -> str | None:
        cur = conn.cursor()
        cur.execute(
            "SELECT value FROM vintages WHERE source='fred' AND series='CORE_CPI' "
            "AND obs_date=? AND published<=? ORDER BY published DESC, seq DESC LIMIT 1",
            (obs, cut),
        )
        r = cur.fetchone()
        return r[0] if r else None

    # Before revision: sees 125.50
    cut1 = "2024-03-01T00:00:00Z"
    val1 = query_vis("2024-01-01", cut1)
    # After revision: sees 125.90
    cut2 = "2024-05-01T00:00:00Z"
    val2 = query_vis("2024-01-01", cut2)

    print("\n2. Point-in-time Vintage Queries:")
    print(f"  Obs 2024-01-01 at {cut1}: visible={val1} (Advance)")
    print(f"  Obs 2024-01-01 at {cut2}: visible={val2} (Revised)")
    assert val1 == "125.50" and val2 == "125.90"
    conn.close()

    # 3. Prevailing Tick Lookup Verification
    ticks = [
        ("2024-06-01T09:30:00.000Z", 1, 150.10),
        ("2024-06-01T09:30:01.000Z", 2, 150.25),
        ("2024-06-01T09:30:01.000Z", 3, 150.30),  # Tie at 01.000, seq 3 wins
    ]
    px = last_trade_at(ticks, "2024-06-01T09:30:01.000Z")
    print(f"\n3. Prevailing Last Trade on Timestamp Tie: px={px} [VERIFIED]")
    assert px == 150.30

    # 4. Corporate Action Split Verification
    dates = ["2024-07-03", "2024-07-06"]
    closes = [200.0, 100.0]  # 2:1 split on 2024-07-06
    splits = [("2024-07-06", 2.0)]
    adj = adjust_closes(dates, closes, splits)
    adj_ret = (adj[1] / adj[0]) - 1.0
    print(f"\n4. Corporate Action Split Adjustment: adj_ret={adj_ret:+.2e} [INVARIANCE VERIFIED]")
    assert abs(adj_ret) <= 1e-12

    print("\nRung 3 project deliverable verification passed.")


main()
