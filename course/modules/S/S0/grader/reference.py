"""Reference solution for Atlas A3: data-quality profiler (atlas.dataquality).

Implements profile(dataset, *, stale_run=5, outlier_k=5.0, break_log=0.25)
strictly adhering to atlas/A3.contract.md.
"""

from __future__ import annotations

import datetime
import math
import statistics
from collections.abc import Mapping, Sequence
from typing import Any

Dataset = Mapping[str, Any]


def profile(
    dataset: Dataset,
    *,
    stale_run: int = 5,
    outlier_k: float = 5.0,
    break_log: float = 0.25,
) -> dict[str, Any]:
    """Profile an in-memory dataset mapping for gaps, stale runs, corporate breaks, and outliers.

    Parameters
    ----------
    dataset : Dataset
        Mapping containing:
        - "name": str label
        - "date": Sequence[str] ISO calendar dates "YYYY-MM-DD", strictly increasing
        - "price": Sequence[float | None] present prices (> 0); None or NaN indicates a gap
        - "split_ratio": optional Sequence[float] corporate action split ratios (> 0, default 1.0)
    stale_run : int, default 5
        Minimum number of consecutive rows with identical present price to flag a stale run (>= 2).
    outlier_k : float, default 5.0
        Multiple of the MAD of non-break returns to flag an outlier (> 0).
    break_log : float, default 0.25
        Threshold on absolute split-adjusted log return to classify as corporate-action break (> 0).

    Returns
    -------
    dict[str, Any]
        Dictionary with keys:
        - "name": str
        - "rows": int
        - "gaps": list[int]
        - "stale_runs": list[tuple[int, int]]
        - "corporate_action_breaks": list[int]
        - "outliers": list[int]
    """
    if not isinstance(dataset, Mapping):
        raise ValueError("dataset must be a mapping")

    for req_key in ("name", "date", "price"):
        if req_key not in dataset:
            raise ValueError(f"dataset missing required key: {req_key!r}")

    name = dataset["name"]
    if not isinstance(name, str):
        raise ValueError("'name' must be a str")

    date_seq = dataset["date"]
    if not isinstance(date_seq, Sequence) or isinstance(date_seq, (str, bytes)):
        raise ValueError("'date' must be a sequence of strings")

    price_seq = dataset["price"]
    if not isinstance(price_seq, Sequence) or isinstance(price_seq, (str, bytes)):
        raise ValueError("'price' must be a sequence")

    n_rows = len(date_seq)
    if n_rows == 0:
        raise ValueError("dataset cannot be empty")
    if len(price_seq) != n_rows:
        raise ValueError(f"length mismatch: 'date' has {n_rows} rows but 'price' has {len(price_seq)}")

    if "split_ratio" in dataset:
        split_seq = dataset["split_ratio"]
        if not isinstance(split_seq, Sequence) or isinstance(split_seq, (str, bytes)):
            raise ValueError("'split_ratio' must be a sequence of positive numbers")
        if len(split_seq) != n_rows:
            raise ValueError(f"length mismatch: 'split_ratio' has {len(split_seq)} rows, expected {n_rows}")
    else:
        split_seq = [1.0] * n_rows

    # Parameter validation
    if isinstance(stale_run, bool) or not isinstance(stale_run, int) or stale_run < 2:
        raise ValueError(f"stale_run must be an integer >= 2, got {stale_run!r}")
    if (
        isinstance(outlier_k, bool)
        or not isinstance(outlier_k, (int, float))
        or not math.isfinite(outlier_k)
        or outlier_k <= 0
    ):
        raise ValueError(f"outlier_k must be a finite float > 0, got {outlier_k!r}")
    if (
        isinstance(break_log, bool)
        or not isinstance(break_log, (int, float))
        or not math.isfinite(break_log)
        or break_log <= 0
    ):
        raise ValueError(f"break_log must be a finite float > 0, got {break_log!r}")

    # Validate dates: parse ISO format and check strictly increasing
    parsed_dates: list[datetime.date] = []
    for idx, d_str in enumerate(date_seq):
        if not isinstance(d_str, str):
            raise ValueError(f"date at row {idx} must be a string, got {type(d_str).__name__}")
        try:
            p_date = datetime.date.fromisoformat(d_str)
        except Exception as exc:
            raise ValueError(f"date at row {idx} does not parse as ISO date: {d_str!r}") from exc
        if parsed_dates and p_date <= parsed_dates[-1]:
            raise ValueError(
                f"dates must be strictly increasing: row {idx} ({p_date}) <= row {idx - 1} ({parsed_dates[-1]})"
            )
        parsed_dates.append(p_date)

    # Validate split ratios
    clean_splits: list[float] = []
    for idx, s_val in enumerate(split_seq):
        if isinstance(s_val, bool) or not isinstance(s_val, (int, float)) or not math.isfinite(s_val) or s_val <= 0:
            raise ValueError(f"split_ratio at row {idx} must be a finite number > 0, got {s_val!r}")
        clean_splits.append(float(s_val))

    # Validate prices and identify gaps
    gaps: list[int] = []
    clean_prices: list[float | None] = []
    for idx, p_val in enumerate(price_seq):
        if p_val is None or (isinstance(p_val, float) and math.isnan(p_val)):
            gaps.append(idx)
            clean_prices.append(None)
        elif isinstance(p_val, bool) or not isinstance(p_val, (int, float)) or not math.isfinite(p_val) or p_val <= 0:
            raise ValueError(f"price at row {idx} must be a positive finite number, got {p_val!r}")
        else:
            clean_prices.append(float(p_val))

    # Stale runs: maximal runs of consecutive rows with the same present price (length >= stale_run)
    # A gap ends a run.
    stale_runs: list[tuple[int, int]] = []
    current_run_price: float | None = None
    current_run_start: int | None = None
    current_run_len: int = 0

    for idx, p_opt in enumerate(clean_prices):
        if p_opt is None:
            if current_run_start is not None and current_run_len >= stale_run:
                stale_runs.append((current_run_start, idx - 1))
            current_run_price = None
            current_run_start = None
            current_run_len = 0
        else:
            if current_run_price is not None and p_opt == current_run_price:
                current_run_len += 1
            else:
                if current_run_start is not None and current_run_len >= stale_run:
                    stale_runs.append((current_run_start, idx - 1))
                current_run_price = p_opt
                current_run_start = idx
                current_run_len = 1

    if current_run_start is not None and current_run_len >= stale_run:
        stale_runs.append((current_run_start, n_rows - 1))

    # Compute split-adjusted log returns for consecutive pairs with no gaps
    valid_returns: list[tuple[int, float]] = []
    for t in range(1, n_rows):
        p_prev = clean_prices[t - 1]
        p_curr = clean_prices[t]
        if p_prev is not None and p_curr is not None:
            # Raw log return: ln(price_t / price_{t-1})
            # Split-adjusted: r_t = ln(price_t / price_{t-1}) + ln(split_ratio_t)
            r_t = math.log(p_curr / p_prev) + math.log(clean_splits[t])
            valid_returns.append((t, r_t))

    if not valid_returns:
        raise ValueError("no valid returns exist in dataset to profile for breaks or outliers")

    # Corporate-action breaks: |r_t| > break_log
    breaks: list[int] = []
    non_break_returns: list[tuple[int, float]] = []
    for t, r_t in valid_returns:
        if abs(r_t) > break_log:
            breaks.append(t)
        else:
            non_break_returns.append((t, r_t))

    # Outliers: |r_t - m| > outlier_k * d on non-break returns
    outliers: list[int] = []
    if non_break_returns:
        r_vals = [r for _, r in non_break_returns]
        m = statistics.median(r_vals)
        devs = [abs(r - m) for r in r_vals]
        d = statistics.median(devs)
        if d == 0.0:
            raise ValueError(f"zero scale: MAD of non-break returns is {d}")
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
