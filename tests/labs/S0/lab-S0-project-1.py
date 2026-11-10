"""Lab S0-project-1: Rung 1 worked example of Atlas A3 data-quality profiler.

Walks through full end-to-end profiling of a SIMULATED financial series, verifying
gap detection, stale run identification, corporate-action breaks, and MAD outlier detection.
All price series are SIMULATED synthetic trajectories.
"""

from __future__ import annotations

import datetime
import math
import statistics
from collections.abc import Mapping
from typing import Any

Dataset = Mapping[str, Any]


def profile_series(
    dataset: Dataset,
    *,
    stale_run: int = 5,
    outlier_k: float = 5.0,
    break_log: float = 0.25,
) -> dict[str, Any]:
    """Profile an in-memory dataset mapping adhering to Atlas A3 contract."""
    name = str(dataset["name"])
    date_seq = list(dataset["date"])
    price_seq = list(dataset["price"])
    n_rows = len(date_seq)

    split_seq = list(dataset.get("split_ratio", [1.0] * n_rows))

    # Gaps and cleaned price values
    gaps: list[int] = []
    clean_prices: list[float | None] = []
    for idx, p in enumerate(price_seq):
        if p is None or (isinstance(p, float) and math.isnan(p)):
            gaps.append(idx)
            clean_prices.append(None)
        else:
            clean_prices.append(float(p))

    # Stale runs: maximal runs of length >= stale_run (a gap ends a run)
    stale_runs: list[tuple[int, int]] = []
    curr_price: float | None = None
    curr_start: int | None = None
    curr_len = 0
    for idx, p in enumerate(clean_prices):
        if p is None:
            if curr_start is not None and curr_len >= stale_run:
                stale_runs.append((curr_start, idx - 1))
            curr_price = None
            curr_start = None
            curr_len = 0
        else:
            if curr_price is not None and p == curr_price:
                curr_len += 1
            else:
                if curr_start is not None and curr_len >= stale_run:
                    stale_runs.append((curr_start, idx - 1))
                curr_price = p
                curr_start = idx
                curr_len = 1
    if curr_start is not None and curr_len >= stale_run:
        stale_runs.append((curr_start, n_rows - 1))

    # Split-adjusted returns: r_t = ln(P_t / P_{t-1}) + ln(split_ratio_t)
    valid_returns: list[tuple[int, float]] = []
    for t in range(1, n_rows):
        p_prev = clean_prices[t - 1]
        p_curr = clean_prices[t]
        if p_prev is not None and p_curr is not None:
            r_t = math.log(p_curr / p_prev) + math.log(float(split_seq[t]))
            valid_returns.append((t, r_t))

    # Corporate-action breaks vs non-break returns
    breaks: list[int] = []
    non_break_returns: list[tuple[int, float]] = []
    for t, r_t in valid_returns:
        if abs(r_t) > break_log:
            breaks.append(t)
        else:
            non_break_returns.append((t, r_t))

    # Outliers via median and MAD of non-break returns
    outliers: list[int] = []
    if non_break_returns:
        r_vals = [r for _, r in non_break_returns]
        m = statistics.median(r_vals)
        d = statistics.median([abs(r - m) for r in r_vals])
        threshold = outlier_k * d
        for t, r_t in non_break_returns:
            if abs(r_t - m) > threshold:
                outliers.append(t)

    return {
        "name": name,
        "rows": n_rows,
        "gaps": sorted(gaps),
        "stale_runs": sorted(stale_runs),
        "corporate_action_breaks": sorted(breaks),
        "outliers": sorted(outliers),
    }


def main() -> None:
    # SIMULATED toy dataset with planted data-quality defects
    dates = [(datetime.date(2023, 1, 2) + datetime.timedelta(days=i)).isoformat() for i in range(12)]
    # Row 2 is a gap (None). Rows 4-9 are a stale run of price 50.0 (length 6 >= 5).
    # Row 10 is an unadjusted corporate break: price drops from 50.0 to 25.0 with split_ratio 1.0 (r_t ~ -0.693).
    # Row 11 has price 28.0 (an outlier return ~ +0.113 vs normal variation).
    prices: list[float | None] = [
        100.0, 101.0, None, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 25.0, 28.0
    ]
    splits = [1.0] * 12

    dataset: dict[str, Any] = {
        "name": "SIMULATED_WORKED_EXAMPLE",
        "date": dates,
        "price": prices,
        "split_ratio": splits,
    }

    report = profile_series(dataset, stale_run=5, outlier_k=4.0, break_log=0.25)

    print(f"Dataset name: {report['name']}")
    print(f"Total rows: {report['rows']}")
    print(f"Flagged gaps: {report['gaps']}")
    print(f"Flagged stale runs: {report['stale_runs']}")
    print(f"Flagged corporate breaks: {report['corporate_action_breaks']}")
    print(f"Flagged outliers: {report['outliers']}")
    print(f"Gap detected at index 2: {report['gaps'] == [2]}")
    print(f"Stale run detected at (3, 9): {report['stale_runs'] == [(3, 9)]}")
    print(f"Corporate break at row 10: {report['corporate_action_breaks'] == [10]}")


main()
