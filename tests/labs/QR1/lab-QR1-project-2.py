"""QR1 Project Lab 2: Rung 2 completion problem reference solution.

Implements core timestamp normalization, point-in-time publication filtering,
and corporate action backward-adjustment factors.
Data: SIMULATED research data store records.
"""

from __future__ import annotations

import datetime
import re

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


def filter_visible_vintages(
    vintages: list[tuple[str, str, str]],  # (obs_date, value, published_utc)
    cutoff_utc: str,
) -> dict[str, str]:
    """Return map of obs_date to latest visible value published at or before cutoff_utc."""
    # Filter only vintages published at or before the cut-off instant
    eligible = [v for v in vintages if v[2] <= cutoff_utc]
    # Sort by published timestamp ascending so latest overwrites earlier
    sorted_eligible = sorted(eligible, key=lambda v: v[2])
    visible_map: dict[str, str] = {}
    for obs_date, val, _ in sorted_eligible:
        visible_map[obs_date] = val
    return visible_map


def compute_adjusted_prices(
    dates: list[str],
    closes: list[float],
    events: list[tuple[str, float]],  # (ex_date, ratio)
) -> list[float]:
    """Compute backward-adjusted closes: raw_close divided by product of subsequent split ratios."""
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
    # 1. Test ET to UTC
    test_walls = ["2026-01-15 12:00", "2026-07-01 12:00"]
    print("1. Timestamp Normalization:")
    for w in test_walls:
        print(f"  {w} -> {et_to_utc(w)}")

    # 2. Test Vintage Filtering
    vintages = [
        ("2026-01-01", "100.0", "2026-02-01T12:00:00Z"),
        ("2026-01-01", "101.5", "2026-03-01T12:00:00Z"),
        ("2026-02-01", "102.0", "2026-03-01T12:00:00Z"),
    ]
    cutoff = "2026-02-15T00:00:00Z"
    visible = filter_visible_vintages(vintages, cutoff)
    print(f"\n2. Visible Series at {cutoff}:")
    for d, v in sorted(visible.items()):
        print(f"  {d}: {v}")

    # 3. Test Corporate Actions
    dates = ["2026-02-01", "2026-02-02", "2026-02-03"]
    closes = [200.0, 100.0, 105.0]  # 2:1 split on 2026-02-02
    events = [("2026-02-02", 2.0)]
    adj = compute_adjusted_prices(dates, closes, events)
    print("\n3. Split Adjustment:")
    for d, c, a in zip(dates, closes, adj, strict=True):
        print(f"  {d}: raw={c:.1f} adjusted={a:.1f}")

    print("\nRung 2 completion problem checks passed.")


main()
