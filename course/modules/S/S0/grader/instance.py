"""Deterministic per-learner instances for the Atlas A3 autograder.

make_instance(seed) produces a deterministic SIMULATED financial series dataset
with planted gaps, stale runs, corporate-action breaks, an explained split, and outliers.
All datasets are SIMULATED synthetic trajectories.
"""

from __future__ import annotations

import datetime
import json
import math
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic test instance for a given workspace seed."""
    rng = random.Random(seed)

    # 1. Base parameters derived deterministically from seed
    n_rows = 110 + (seed % 25)  # 110 to 134 rows
    start_date = datetime.date(2021, 1, 4) + datetime.timedelta(days=(seed % 100))
    dates: list[str] = [(start_date + datetime.timedelta(days=i)).isoformat() for i in range(n_rows)]

    # Starting price between 40.0 and 180.0
    p0 = round(40.0 + (seed % 35) * 4.0 + rng.uniform(0.1, 3.9), 2)
    splits: list[float] = [1.0] * n_rows

    stale_start = 22 + (seed % 5)
    stale_len = 6
    stale_end = stale_start + stale_len - 1

    split_row = 60 + (seed % 5)
    break_row = 75 + (seed % 6)
    outlier_row = 92 + (seed % 6)

    # Explained 2-for-1 corporate action split
    splits[split_row] = 2.0

    # Sequential trajectory generation ensuring proper continuity
    prices: list[float | None] = [p0]
    for t in range(1, n_rows):
        ret = rng.uniform(-0.007, 0.007)
        prev = prices[-1]
        assert prev is not None

        if stale_start < t <= stale_end:
            # Maintain exact price for stale run
            nxt = prev
        elif t == split_row:
            # 2-for-1 split: nominal price halves, split_ratio = 2.0
            # Split-adjusted return r_t = ln(0.501) + ln(2.0) ~ 0.002 (not a break, not an outlier)
            nxt = round(prev * 0.5 * math.exp(ret), 4)
        elif t == break_row:
            # Unexplained corporate break: 40% price drop with split_ratio = 1.0
            # Split-adjusted return r_t = ln(0.60) + ret ~ -0.5108 (exceeds break_log = 0.25)
            nxt = round(prev * 0.60 * math.exp(ret), 4)
        elif t == outlier_row:
            # Statistical outlier: 11% jump with split_ratio = 1.0
            # Return r_t = ln(1.11) + ret ~ 0.1044 (exceeds 5.0 * MAD, but <= break_log 0.25)
            nxt = round(prev * 1.11 * math.exp(ret), 4)
        else:
            nxt = round(prev * math.exp(ret), 4)
            if nxt == prev:
                nxt = round(prev * 1.002, 4)
        prices.append(nxt)

    # Plant gaps (None and NaN) at positions outside events
    gap1 = 12 + (seed % 6)
    gap2 = 42 + (seed % 7)
    prices[gap1] = None
    prices[gap2] = float("nan")

    expected_gaps = sorted([gap1, gap2])
    expected_stale_runs = [(stale_start, stale_end)]
    expected_breaks = [break_row]
    expected_outliers = [outlier_row]

    primary_dataset: dict[str, Any] = {
        "name": f"SIMULATED_A3_SERIES_{seed}",
        "date": dates,
        "price": prices,
        "split_ratio": splits,
    }

    # Clean dataset with no gaps, no stale runs >= 5, no breaks, no outliers
    clean_n = 40
    clean_dates = [(datetime.date(2022, 1, 3) + datetime.timedelta(days=i)).isoformat() for i in range(clean_n)]
    clean_prices: list[float] = [100.0]
    for _ in range(clean_n - 1):
        ret = rng.uniform(-0.005, 0.005)
        p_nxt = round(clean_prices[-1] * math.exp(ret), 4)
        if p_nxt == clean_prices[-1]:
            p_nxt = round(clean_prices[-1] * 1.002, 4)
        clean_prices.append(p_nxt)
    clean_dataset: dict[str, Any] = {
        "name": "SIMULATED_CLEAN",
        "date": clean_dates,
        "price": clean_prices,
    }

    # Zero-scale dataset where prices are constant so MAD is 0.0
    zero_scale_dates = [(datetime.date(2023, 1, 2) + datetime.timedelta(days=i)).isoformat() for i in range(15)]
    zero_scale_dataset: dict[str, Any] = {
        "name": "SIMULATED_ZERO_SCALE",
        "date": zero_scale_dates,
        "price": [100.0] * 15,
        "split_ratio": [1.0] * 15,
    }

    # Invalid cases that must raise ValueError
    invalid_cases: list[dict[str, Any]] = [
        {"desc": "missing_name", "dataset": {"date": ["2020-01-01"], "price": [10.0]}},
        {"desc": "missing_date", "dataset": {"name": "X", "price": [10.0]}},
        {"desc": "missing_price", "dataset": {"name": "X", "date": ["2020-01-01"]}},
        {"desc": "empty_dataset", "dataset": {"name": "X", "date": [], "price": []}},
        {"desc": "mismatched_lengths", "dataset": {"name": "X", "date": ["2020-01-01", "2020-01-02"], "price": [10.0]}},
        {
            "desc": "mismatched_splits",
            "dataset": {"name": "X", "date": ["2020-01-01"], "price": [10.0], "split_ratio": [1.0, 2.0]},
        },
        {"desc": "invalid_date_format", "dataset": {"name": "X", "date": ["2020/01/01"], "price": [10.0]}},
        {
            "desc": "non_increasing_dates",
            "dataset": {"name": "X", "date": ["2020-01-02", "2020-01-01"], "price": [10.0, 11.0]},
        },
        {
            "desc": "duplicate_dates",
            "dataset": {"name": "X", "date": ["2020-01-01", "2020-01-01"], "price": [10.0, 11.0]},
        },
        {"desc": "zero_price", "dataset": {"name": "X", "date": ["2020-01-01"], "price": [0.0]}},
        {"desc": "negative_price", "dataset": {"name": "X", "date": ["2020-01-01"], "price": [-5.0]}},
        {"desc": "infinite_price", "dataset": {"name": "X", "date": ["2020-01-01"], "price": [float("inf")]}},
        {
            "desc": "invalid_split_ratio_zero",
            "dataset": {"name": "X", "date": ["2020-01-01"], "price": [10.0], "split_ratio": [0.0]},
        },
        {
            "desc": "invalid_split_ratio_negative",
            "dataset": {"name": "X", "date": ["2020-01-01"], "price": [10.0], "split_ratio": [-1.0]},
        },
        {
            "desc": "invalid_split_ratio_nan",
            "dataset": {"name": "X", "date": ["2020-01-01"], "price": [10.0], "split_ratio": [float("nan")]},
        },
        {"desc": "no_valid_returns_single_row", "dataset": {"name": "X", "date": ["2020-01-01"], "price": [10.0]}},
        {
            "desc": "no_valid_returns_all_gaps_alternating",
            "dataset": {"name": "X", "date": ["2020-01-01", "2020-01-02", "2020-01-03"], "price": [10.0, None, 12.0]},
        },
    ]

    payload: dict[str, Any] = {
        "dataset": primary_dataset,
        "clean_dataset": clean_dataset,
        "zero_scale_dataset": zero_scale_dataset,
        "expected_gaps": expected_gaps,
        "expected_stale_runs": expected_stale_runs,
        "expected_breaks": expected_breaks,
        "expected_outliers": expected_outliers,
        "split_row": split_row,
        "invalid_cases": invalid_cases,
    }

    return {
        "seed": int(seed),
        "name": str(primary_dataset["name"]),
        "rows": n_rows,
        "payload": json.dumps(payload, sort_keys=True),
    }
