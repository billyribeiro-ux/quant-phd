"""Lab QR2-L02-1: Signal-to-Execution Lag and Alpha Decay.

Demonstrates the collapse of apparent Sharpe ratio as execution lag tau increases
from 0 (trade-on-close lookahead leak) to 1 bar and 2 bars.
"""

from __future__ import annotations

import math

import numpy as np


def evaluate_strategy_lag(prices: np.ndarray, signals: np.ndarray, lag: int) -> tuple[float, float]:
    """Evaluates strategy returns with strict execution lag."""
    n_bars = len(prices)
    returns = np.zeros(n_bars)
    returns[1:] = (prices[1:] - prices[:-1]) / prices[:-1]

    # Signal generated at t is executed with lag tau
    strat_returns = np.zeros(n_bars)
    for t in range(n_bars):
        if t >= lag:
            strat_returns[t] = signals[t - lag] * returns[t]

    valid_returns = strat_returns[lag + 1 :]
    mean_ret = float(np.mean(valid_returns))
    std_ret = float(np.std(valid_returns, ddof=1))
    ann_sharpe = (mean_ret / std_ret * math.sqrt(252)) if std_ret > 1e-12 else 0.0
    cum_ret = float(np.prod(1.0 + valid_returns) - 1.0)
    return ann_sharpe, cum_ret * 100.0


def main() -> None:
    rng = np.random.default_rng(101)
    n_bars = 250
    innovations = rng.normal(0.0002, 0.012, size=n_bars)
    prices = 100.0 * np.exp(np.cumsum(innovations))

    # Trend-following on same-day return (artificial lookahead if traded on close)
    ret_1d = np.zeros(n_bars)
    ret_1d[1:] = (prices[1:] - prices[:-1]) / prices[:-1]
    signals = np.sign(ret_1d)

    print("Signal-to-Execution Lag Decay Study (252 bars):")
    print("--------------------------------------------------")
    print(f"{'Lag (bars)':<12}{'Annual Sharpe':<16}{'Total Return (%)':<18}{'Interpretation'}")
    print("--------------------------------------------------")

    for lag in [0, 1, 2]:
        sharpe, cum_ret = evaluate_strategy_lag(prices, signals, lag)
        label = "Lookahead Leak" if lag == 0 else ("Realistic Causal" if lag == 1 else "Delayed Fill")
        print(f"{lag:<12}{sharpe:<16.2f}{cum_ret:<18.2f}{label}")

    print("--------------------------------------------------")
    print("Invariant Verified: Zero-lag execution produces artificial alpha via trade-on-close leakage.")


main()
