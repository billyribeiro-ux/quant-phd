"""Lab S0-project-3: Rung 4 stretch lab applying Atlas A3 profiler to real market data.

Applies the profile engine to Federal Reserve H.10 daily FX rates (EUR/USD) and H.15 Treasury
constant-maturity yields. Demonstrates real-world stale run detection, the calendar limitation
(absent holiday rows are not flagged as gaps), and low-yield relative log step sensitivity.
Data sources:
- Board of Governors of the Federal Reserve System, G.5/H.10 Foreign Exchange Rates (2026-10-19)
- Board of Governors of the Federal Reserve System, H.15 Selected Interest Rates (2026-10-20)
"""

from __future__ import annotations

import csv
import math
import statistics
from collections.abc import Mapping
from pathlib import Path
from typing import Any

Dataset = Mapping[str, Any]


def profile_market_series(
    dataset: Dataset,
    *,
    stale_run: int = 5,
    outlier_k: float = 5.0,
    break_log: float = 0.25,
) -> dict[str, Any]:
    """Pure implementation of Atlas A3 profile engine for project stretch evaluation."""
    name = str(dataset["name"])
    date_seq = list(dataset["date"])
    price_seq = list(dataset["price"])
    n_rows = len(date_seq)
    split_seq = list(dataset.get("split_ratio", [1.0] * n_rows))

    gaps: list[int] = []
    clean_prices: list[float | None] = []
    for idx, p in enumerate(price_seq):
        if p is None or (isinstance(p, float) and math.isnan(p)):
            gaps.append(idx)
            clean_prices.append(None)
        else:
            clean_prices.append(float(p))

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

    valid_returns: list[tuple[int, float]] = []
    for t in range(1, n_rows):
        p_prev = clean_prices[t - 1]
        p_curr = clean_prices[t]
        if p_prev is not None and p_curr is not None:
            r_t = math.log(p_curr / p_prev) + math.log(float(split_seq[t]))
            valid_returns.append((t, r_t))

    breaks: list[int] = []
    non_break_returns: list[tuple[int, float]] = []
    for t, r_t in valid_returns:
        if abs(r_t) > break_log:
            breaks.append(t)
        else:
            non_break_returns.append((t, r_t))

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
    # 1. Profile FX Daily (EUR/USD spot rate)
    fx_path = Path("data") / "fx_daily.csv"
    with fx_path.open(newline="", encoding="utf-8") as f:
        fx_rows = [row for row in csv.DictReader(f) if row.get("EUR")]

    fx_dataset: dict[str, Any] = {
        "name": "FX_EUR_USD",
        "date": [r["date"] for r in fx_rows],
        "price": [float(r["EUR"]) for r in fx_rows],
    }
    fx_report = profile_market_series(fx_dataset, stale_run=5, outlier_k=5.0, break_log=0.25)

    print(f"FX Daily rows: {fx_report['rows']}")
    print(f"FX Daily gaps: {len(fx_report['gaps'])}")
    print(f"FX Daily stale runs: {len(fx_report['stale_runs'])}")
    print(f"FX Daily corporate breaks: {len(fx_report['corporate_action_breaks'])}")
    print(f"FX Daily outliers: {len(fx_report['outliers'])}")

    # 2. Profile UST Daily (10-Year CMT yield)
    ust_path = Path("data") / "ust_daily.csv"
    with ust_path.open(newline="", encoding="utf-8") as f:
        ust_rows = [row for row in csv.DictReader(f) if row.get("cmt_10y")]

    ust_dataset: dict[str, Any] = {
        "name": "UST_10Y_YIELD",
        "date": [r["date"] for r in ust_rows],
        "price": [float(r["cmt_10y"]) for r in ust_rows],
    }
    ust_report = profile_market_series(ust_dataset, stale_run=5, outlier_k=5.0, break_log=0.25)

    print(f"UST Daily rows: {ust_report['rows']}")
    print(f"UST Daily gaps: {len(ust_report['gaps'])}")
    print(f"UST Daily stale runs: {len(ust_report['stale_runs'])}")
    print(f"UST Daily corporate breaks: {len(ust_report['corporate_action_breaks'])}")
    print(f"UST Daily outliers: {len(ust_report['outliers'])}")

    # Calendar limitation: no gaps detected because market holidays are omitted from the CSV table
    print(f"Calendar limitation holds (holiday rows absent): {len(fx_report['gaps']) == 0}")
    # Real stale prints detected in Treasury series
    print(f"Stale prints detected in UST series: {len(ust_report['stale_runs']) > 0}")
    # COVID March 2020 low-yield jumps triggered breaks
    print(f"Low-yield rate spikes triggered breaks: {len(ust_report['corporate_action_breaks']) > 0}")


main()
