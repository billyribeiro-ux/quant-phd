"""QR1 Lesson 1 Inline Lab 1: Timestamp semantics and UTC normalization.

Demonstrates conversion of heterogeneous exchange and release timestamps with
explicit timezone offsets into canonical ISO 8601 UTC representation and
verifies point-in-time visibility filters against decision cut-offs.
Data: SIMULATED macroeconomic and market release records.
"""

from __future__ import annotations

import datetime
from typing import NamedTuple


class RawRelease(NamedTuple):
    series: str
    obs_date: str
    local_time: str  # YYYY-MM-DD HH:MM:SS
    tz_offset: str  # e.g., "-05:00", "+00:00", "+09:00"
    value: float


class NormalizedRelease(NamedTuple):
    series: str
    obs_date: str
    utc_timestamp: str  # YYYY-MM-DDTHH:MM:SSZ
    value: float


def parse_offset_to_timedelta(offset_str: str) -> datetime.timedelta:
    """Parse timezone offset string '+HH:MM' or '-HH:MM' into datetime.timedelta."""
    sign = -1 if offset_str.startswith("-") else 1
    raw = offset_str.lstrip("+-")
    parts = raw.split(":")
    hours = int(parts[0])
    minutes = int(parts[1]) if len(parts) > 1 else 0
    return datetime.timedelta(minutes=sign * (hours * 60 + minutes))


def normalize_to_utc(local_time_str: str, offset_str: str) -> str:
    """Convert local timestamp and offset to canonical ISO 8601 UTC 'YYYY-MM-DDTHH:MM:SSZ'."""
    dt = datetime.datetime.strptime(local_time_str, "%Y-%m-%d %H:%M:%S")
    offset = parse_offset_to_timedelta(offset_str)
    # UTC = local - offset
    utc_dt = dt - offset
    return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def filter_visible_releases(
    releases: list[NormalizedRelease],
    cutoff_utc: str,
) -> list[NormalizedRelease]:
    """Filter records whose publication UTC timestamp is at or before cutoff_utc."""
    return [r for r in releases if r.utc_timestamp <= cutoff_utc]


def main() -> None:
    # SIMULATED release records across global reporting venues
    raw_data: list[RawRelease] = [
        RawRelease("US_CPI", "2026-02-01", "2026-03-12 08:30:00", "-04:00", 312.4),
        RawRelease("UK_CPI", "2026-02-01", "2026-03-12 07:00:00", "+00:00", 131.8),
        RawRelease("JP_CPI", "2026-02-01", "2026-03-13 08:30:00", "+09:00", 106.2),
        RawRelease("US_NFP", "2026-02-01", "2026-03-06 08:30:00", "-05:00", 225.0),
        RawRelease("US_GDP", "2025-Q4", "2026-03-26 08:30:00", "-04:00", 28100.5),
        RawRelease("DE_PMI", "2026-02-01", "2026-03-02 09:30:00", "+01:00", 47.3),
    ]

    normalized: list[NormalizedRelease] = []
    for r in raw_data:
        utc_ts = normalize_to_utc(r.local_time, r.tz_offset)
        normalized.append(NormalizedRelease(r.series, r.obs_date, utc_ts, r.value))

    print(f"Total raw releases ingested: {len(normalized)}")
    for nr in sorted(normalized, key=lambda x: x.utc_timestamp):
        print(f"  {nr.series:8s} obs={nr.obs_date:10s} published_utc={nr.utc_timestamp} val={nr.value:.1f}")

    # Decision cut-off: 2026-03-12 12:00:00 UTC
    decision_cutoff = "2026-03-12T12:00:00Z"
    visible = filter_visible_releases(normalized, decision_cutoff)

    # Brute-force verification
    expected_series = {"DE_PMI", "US_NFP", "UK_CPI"}
    actual_series = {r.series for r in visible}

    print(f"Decision cut-off: {decision_cutoff}")
    print(f"Visible records count: {len(visible)}")
    print(f"Visible series: {sorted(actual_series)}")
    mismatches = len(actual_series ^ expected_series)
    print(f"Look-ahead filtering mismatches: {mismatches}")


main()
