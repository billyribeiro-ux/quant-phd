"""Lab S0-L04-1: Stale-run detection and spotting a split-adjustment error.

Demonstrates identifying maximal stale price runs and detecting unadjusted corporate-action
splits in financial time series. Compares raw vs split-adjusted log returns and volatility.
Data label: SIMULATED (no cleared equity dataset with corporate actions is currently embedded;
pending cleared redistribution rights).
"""

from __future__ import annotations

import math
import random
import statistics


def detect_stale_runs(prices: list[float], min_run: int = 5) -> list[tuple[int, int]]:
    """Identify maximal runs of identical prices of length >= min_run."""
    runs: list[tuple[int, int]] = []
    if not prices:
        return runs
    start = 0
    curr_len = 1
    for i in range(1, len(prices)):
        if prices[i] == prices[i - 1]:
            curr_len += 1
        else:
            if curr_len >= min_run:
                runs.append((start, i - 1))
            start = i
            curr_len = 1
    if curr_len >= min_run:
        runs.append((start, len(prices) - 1))
    return runs


def main() -> None:
    # SIMULATED daily price path over 100 trading days
    seed = 101
    rng = random.Random(seed)
    n = 100

    prices: list[float] = [100.0]
    split_ratios: list[float] = [1.0] * n

    stale_start = 25
    stale_len = 6
    split_day = 60

    # True split: 2-for-1 split on day 60
    split_ratios[split_day] = 2.0

    for t in range(1, n):
        ret = rng.uniform(-0.008, 0.008)
        if stale_start < t < stale_start + stale_len:
            # Stale print: identical price
            nxt = prices[-1]
        elif t == split_day:
            # Nominal price halves due to 2-for-1 split plus daily market movement
            nxt = round(prices[-1] * 0.50 * math.exp(ret), 4)
        else:
            nxt = round(prices[-1] * math.exp(ret), 4)
            if nxt == prices[-1]:
                nxt = round(prices[-1] * 1.002, 4)
        prices.append(nxt)

    # 1. Detect stale runs
    stale_runs = detect_stale_runs(prices, min_run=5)

    # 2. Compute raw unadjusted returns vs split-adjusted returns
    raw_returns: list[float] = [
        math.log(prices[t] / prices[t - 1]) for t in range(1, n)
    ]
    adj_returns: list[float] = [
        math.log(prices[t] / prices[t - 1]) + math.log(split_ratios[t])
        for t in range(1, n)
    ]

    # Inspect returns at the split event (day 60 -> index 59 in returns)
    r_raw_split = raw_returns[split_day - 1]
    r_adj_split = adj_returns[split_day - 1]

    # Annualized volatility: std * sqrt(252)
    vol_raw = statistics.stdev(raw_returns) * math.sqrt(252)
    vol_adj = statistics.stdev(adj_returns) * math.sqrt(252)

    print(f"Sample length: {n} trading days")
    print(f"Detected stale runs: {stale_runs}")
    print(f"Stale run covers expected range: {stale_runs == [(stale_start, stale_start + stale_len - 1)]}")
    print(f"Day {split_day} unadjusted raw return: {r_raw_split:.5f} ({math.exp(r_raw_split) - 1.0:.2%})")
    print(f"Day {split_day} split-adjusted return:  {r_adj_split:.5f} ({math.exp(r_adj_split) - 1.0:.2%})")
    print(f"Annualized volatility (raw):      {vol_raw:.2%}")
    print(f"Annualized volatility (adjusted): {vol_adj:.2%}")
    print(f"Split-adjustment removes phantom crash: {r_raw_split < -0.60 and abs(r_adj_split) < 0.02}")
    print(f"Volatility distortion factor: {vol_raw / vol_adj:.2f}x")


main()
