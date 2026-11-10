"""CS1 lab L08: Tabular data alignment and index alignment mechanics.

Uses embedded real market snapshots fx_daily.csv and ust_daily.csv from the Federal Reserve
(cleared in course/assets/data/market/MANIFEST.json).
Demonstrates why positional matching fails and how index alignment matches records on date keys.
"""

from __future__ import annotations

import csv
from pathlib import Path


def load_series(filepath: Path, date_col: str, val_col: str) -> dict[str, float]:
    """Load a single-column time series indexed by date from a CSV file."""
    series: dict[str, float] = {}
    with filepath.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_str = row[date_col]
            val_str = row[val_col]
            if val_str and val_str != "ND":
                series[date_str] = float(val_str)
    return series


def align_by_index(
    series_a: dict[str, float], series_b: dict[str, float]
) -> tuple[list[str], list[tuple[float, float]]]:
    """Inner join alignment on matching index keys."""
    common_dates = sorted(set(series_a.keys()) & set(series_b.keys()))
    aligned_values = [(series_a[d], series_b[d]) for d in common_dates]
    return common_dates, aligned_values


def main() -> None:
    data_dir = Path("data")
    fx_path = data_dir / "fx_daily.csv"
    ust_path = data_dir / "ust_daily.csv"

    eur_series = load_series(fx_path, "date", "EUR")
    cmt_series = load_series(ust_path, "date", "cmt_10y")

    # 1. Total series lengths
    len_fx = len(eur_series)
    len_ust = len(cmt_series)
    print(f"fx EUR observations: {len_fx}")
    print(f"ust 10y observations: {len_ust}")

    # 2. Index set operations
    fx_dates = set(eur_series.keys())
    ust_dates = set(cmt_series.keys())
    common_dates = fx_dates & ust_dates
    fx_only_dates = fx_dates - ust_dates
    ust_only_dates = ust_dates - fx_dates

    print(f"common dates count: {len(common_dates)}")
    print(f"fx-only dates count: {len(fx_only_dates)}")
    print(f"ust-only dates count: {len(ust_only_dates)}")

    # 3. Inner alignment
    aligned_dates, aligned_pairs = align_by_index(eur_series, cmt_series)
    first_date = aligned_dates[0]
    first_eur, first_cmt = aligned_pairs[0]
    print(f"first aligned date: {first_date}")
    print(f"first aligned EUR rate: {first_eur:.4f}")
    print(f"first aligned 10Y yield: {first_cmt:.2f}")

    # 4. Positional misalignment demonstration
    fx_ordered_dates = list(eur_series.keys())
    ust_ordered_dates = list(cmt_series.keys())
    mismatch_idx = next(i for i in range(min(len_fx, len_ust)) if fx_ordered_dates[i] != ust_ordered_dates[i])
    print(f"first positional mismatch index: {mismatch_idx}")
    print(f"positional date fx: {fx_ordered_dates[mismatch_idx]}")
    print(f"positional date ust: {ust_ordered_dates[mismatch_idx]}")
    print(f"index alignment preserves exact date match: {aligned_dates[mismatch_idx] in common_dates}")


main()
