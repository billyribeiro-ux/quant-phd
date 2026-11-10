"""Deterministic instance generator for QR2 project (Atlas A9: backtester).

Generates seeded market environments, price paths, execution parameters,
signals, and planted-lookahead test vectors for grading.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic backtester verification instance for the given seed."""
    rng = np.random.default_rng(seed)

    n_bars = 300 + int(rng.integers(0, 100))
    initial_cash = 100_000.0 + float(rng.uniform(0.0, 50_000.0))

    # Generate realistic geometric price path with stochastic drift and vol
    drift = float(rng.normal(0.0003, 0.0001))
    vol = float(rng.uniform(0.01, 0.025))
    innovations = rng.normal(drift, vol, size=n_bars)
    log_prices = np.log(100.0 + rng.uniform(-20.0, 50.0)) + np.cumsum(innovations)
    prices = np.exp(log_prices)

    # Volumes (log-normal) and daily volatility estimates
    volumes = np.exp(rng.normal(np.log(1_000_000.0), 0.3, size=n_bars))
    volatilities = np.clip(np.abs(rng.normal(vol, 0.005, size=n_bars)), 0.005, 0.08)

    # Generate moving-average crossover signals (purely causal)
    fast_period = int(rng.integers(5, 12))
    slow_period = int(rng.integers(20, 35))

    # rolling periods: fast_period, slow_period

    # Causal rolling means using only past data
    fast_ma = np.zeros(n_bars)
    slow_ma = np.zeros(n_bars)
    for t in range(n_bars):
        if t >= fast_period - 1:
            fast_ma[t] = np.mean(prices[t - fast_period + 1 : t + 1])
        else:
            fast_ma[t] = np.mean(prices[: t + 1])

        if t >= slow_period - 1:
            slow_ma[t] = np.mean(prices[t - slow_period + 1 : t + 1])
        else:
            slow_ma[t] = np.mean(prices[: t + 1])

    legitimate_signals = np.zeros(n_bars, dtype=np.float64)
    legitimate_signals[fast_ma > slow_ma] = 1.0
    legitimate_signals[fast_ma < slow_ma] = -1.0

    # Planted-lookahead signal: leaks future 1-bar price innovation
    # s_t = sign(P_{t+1} - P_t)
    future_diff = np.diff(prices)
    planted_signals = np.zeros(n_bars, dtype=np.float64)
    planted_signals[:-1] = np.sign(future_diff)
    planted_signals[-1] = 0.0

    # Cost parameters
    commission_bps = float(rng.uniform(3.0, 10.0))
    half_spread_bps = float(rng.uniform(1.0, 5.0))
    impact_coeff = float(rng.uniform(0.3, 0.7))

    # Cross-validation parameters
    wf_train_size = int(rng.integers(60, 100))
    wf_test_size = int(rng.integers(20, 40))
    wf_step_size = int(rng.integers(10, 20))

    cv_n_splits = int(rng.integers(4, 7))
    cv_label_lookahead = int(rng.integers(2, 6))
    cv_embargo_pct = float(rng.uniform(0.01, 0.03))

    cpcv_n_groups = 6
    cpcv_k_test_groups = 2

    # Trial matrix for research integrity checks (T x N)
    n_trials = int(rng.integers(5, 12))
    trial_returns = rng.normal(0.0002, 0.01, size=(n_bars, n_trials))
    # Give the selected trial a positive mean
    selected_trial = int(rng.integers(0, n_trials))
    trial_returns[:, selected_trial] += rng.uniform(0.0005, 0.0015)

    return {
        "seed": seed,
        "n_bars": n_bars,
        "initial_cash": initial_cash,
        "prices": prices,
        "volumes": volumes,
        "volatilities": volatilities,
        "legitimate_signals": legitimate_signals,
        "planted_signals": planted_signals,
        "commission_bps": commission_bps,
        "half_spread_bps": half_spread_bps,
        "impact_coeff": impact_coeff,
        "wf_train_size": wf_train_size,
        "wf_test_size": wf_test_size,
        "wf_step_size": wf_step_size,
        "cv_n_splits": cv_n_splits,
        "cv_label_lookahead": cv_label_lookahead,
        "cv_embargo_pct": cv_embargo_pct,
        "cpcv_n_groups": cpcv_n_groups,
        "cpcv_k_test_groups": cpcv_k_test_groups,
        "trial_returns": trial_returns,
        "selected_trial": selected_trial,
    }
