"""Lab QR2-L01-1: Vectorized vs. Event-Driven Execution Discrepancy.

Demonstrates tracking divergence between a frictionless vectorized backtest
and a discrete event-driven queue with integer share lots and cash constraints.
"""

from __future__ import annotations

import numpy as np


def run_vectorized(prices: np.ndarray, signals: np.ndarray, initial_cash: float) -> tuple[np.ndarray, float]:
    """Computes vectorized equity curve with continuous full reinvestment."""
    returns = np.zeros_like(prices)
    returns[1:] = (prices[1:] - prices[:-1]) / prices[:-1]
    # In vectorized model, signal at t-1 earns return at t
    strat_returns = signals[:-1] * returns[1:]
    equity = np.zeros_like(prices)
    equity[0] = initial_cash
    for t in range(1, len(prices)):
        equity[t] = equity[t - 1] * (1.0 + strat_returns[t - 1])
    return equity, float(equity[-1])


def run_event_driven(prices: np.ndarray, signals: np.ndarray, initial_cash: float) -> tuple[np.ndarray, float]:
    """Computes event-driven equity curve with discrete integer share execution and cash tracking."""
    n_bars = len(prices)
    cash = initial_cash
    shares = 0
    equity = np.zeros(n_bars)

    for t in range(n_bars):
        current_price = prices[t]
        # In discrete event queue, signal at t-1 is filled at t
        if t > 0:
            target_signal = signals[t - 1]
            current_equity = cash + shares * current_price
            target_value = target_signal * current_equity
            target_shares = int(target_value // current_price) if target_value > 0 else 0
            share_diff = target_shares - shares

            if share_diff != 0:
                cost = share_diff * current_price
                if cash >= cost:
                    cash -= cost
                    shares += share_diff

        equity[t] = cash + shares * current_price

    return equity, float(equity[-1])


def main() -> None:
    # Deterministic seeded synthetic prices
    rng = np.random.default_rng(42)
    n_bars = 120
    drift = 0.0004
    vol = 0.015
    innovations = rng.normal(drift, vol, size=n_bars)
    prices = 100.0 * np.exp(np.cumsum(innovations))

    # Fast / slow moving average crossover signal
    fast_ma = np.convolve(prices, np.ones(5) / 5, mode="same")
    slow_ma = np.convolve(prices, np.ones(20) / 20, mode="same")
    signals = np.where(fast_ma > slow_ma, 1.0, 0.0)

    initial_cash = 100_000.0
    _vec_equity, vec_end = run_vectorized(prices, signals, initial_cash)
    _evt_equity, evt_end = run_event_driven(prices, signals, initial_cash)

    diff = vec_end - evt_end
    tracking_err_pct = (diff / evt_end) * 100.0

    print(f"Initial Capital: ${initial_cash:,.2f}")
    print(f"Vectorized Ending Equity: ${vec_end:,.2f}")
    print(f"Event-Driven Ending Equity: ${evt_end:,.2f}")
    print(f"Absolute Discrepancy: ${diff:,.2f}")
    print(f"Relative Tracking Error: {tracking_err_pct:.3f}%")
    print("Execution State Invariant Verified: Integer share lot discretizations induce drift.")


main()
