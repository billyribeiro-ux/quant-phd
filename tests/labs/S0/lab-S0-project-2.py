"""Lab S0-project-2: Completion problem solution for core Atlas A3 data-quality algorithms.

Tests core detection logic for gaps, stale runs, split-adjusted log returns,
and corporate-action breaks on SIMULATED price quotes.
"""

from __future__ import annotations

import math
from collections.abc import Sequence


def flag_gaps(prices: Sequence[float | None]) -> list[int]:
    """Identify row indices where price is missing (None or NaN)."""
    gaps: list[int] = []
    for idx, p in enumerate(prices):
        if p is None or (isinstance(p, float) and math.isnan(p)):
            gaps.append(idx)
    return gaps


def flag_stale_runs(prices: Sequence[float | None], stale_run: int = 5) -> list[tuple[int, int]]:
    """Identify maximal runs of identical non-gap prices of length >= stale_run."""
    runs: list[tuple[int, int]] = []
    curr_price: float | None = None
    curr_start: int | None = None
    curr_len = 0
    for idx, p in enumerate(prices):
        if p is None or (isinstance(p, float) and math.isnan(p)):
            if curr_start is not None and curr_len >= stale_run:
                runs.append((curr_start, idx - 1))
            curr_price = None
            curr_start = None
            curr_len = 0
        else:
            val = float(p)
            if curr_price is not None and val == curr_price:
                curr_len += 1
            else:
                if curr_start is not None and curr_len >= stale_run:
                    runs.append((curr_start, idx - 1))
                curr_price = val
                curr_start = idx
                curr_len = 1
    if curr_start is not None and curr_len >= stale_run:
        runs.append((curr_start, len(prices) - 1))
    return runs


def compute_split_adjusted_return(
    p_prev: float,
    p_curr: float,
    split_ratio: float = 1.0,
) -> float:
    """Compute split-adjusted log return: r_t = ln(P_t / P_{t-1}) + ln(split_ratio_t)."""
    return math.log(p_curr / p_prev) + math.log(split_ratio)


def is_corporate_break(r_t: float, break_log: float = 0.25) -> bool:
    """Return True if absolute split-adjusted log return exceeds break threshold."""
    return abs(r_t) > break_log


def main() -> None:
    # SIMULATED price trajectory
    quotes: list[float | None] = [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, None, 45.0, 45.0]

    # 1. Identify gaps
    gaps = flag_gaps(quotes)
    print(f"Total quotes: {len(quotes)}")
    print(f"Gaps found: {gaps}")

    # 2. Identify stale runs
    stale_runs = flag_stale_runs(quotes, stale_run=5)
    print(f"Stale runs found: {stale_runs}")

    # 3. Check corporate action break on unadjusted price jump
    r_unadj = compute_split_adjusted_return(100.0, 50.0, 1.0)
    is_break_unadj = is_corporate_break(r_unadj, break_log=0.25)
    print(f"Unadjusted return: {r_unadj:.5f}, is_break: {is_break_unadj}")

    # 4. Check explained split
    r_adj = compute_split_adjusted_return(100.0, 50.0, 2.0)
    is_break_adj = is_corporate_break(r_adj, break_log=0.25)
    print(f"Split-adjusted return: {r_adj:.5f}, is_break: {is_break_adj}")

    print(f"Gaps match index 6: {gaps == [6]}")
    print(f"Stale run covers indices (0, 5): {stale_runs == [(0, 5)]}")
    print(f"Unadjusted break detected: {is_break_unadj}")
    print(f"Explained split not flagged: {not is_break_adj}")


main()
