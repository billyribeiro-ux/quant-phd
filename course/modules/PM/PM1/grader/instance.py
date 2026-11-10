"""Deterministic instance generator for PM1: Private Equity (PME Engine).

Generates realistic private equity fund cash flows, public market benchmark price paths,
and underlying fund parameters (true alpha, market beta, investment horizon) for an integer seed.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic fund cash flow and public market benchmark instance."""
    rng = np.random.default_rng(seed)
    times = np.linspace(0.0, 10.0, 21)  # 21 semi-annual points from t=0.0 to t=10.0
    dt = 0.5

    # 1. Public Market Benchmark Path (Geometric Brownian Motion)
    mu_m = 0.06 + (seed % 5) * 0.01  # Annual drift: 6.0% to 10.0%
    sigma_m = 0.14 + (seed % 7) * 0.01  # Annual volatility: 14.0% to 20.0%
    z_m = rng.normal(0.0, 1.0, len(times) - 1)
    log_ret_m = (mu_m - 0.5 * sigma_m**2) * dt + sigma_m * np.sqrt(dt) * z_m

    bench_prices = np.zeros(len(times), dtype=np.float64)
    bench_prices[0] = 100.0
    for i in range(len(z_m)):
        bench_prices[i + 1] = bench_prices[i] * np.exp(log_ret_m[i])

    # 2. Fund Performance Parameters
    true_alpha = float(round(-0.01 + (seed % 9) * 0.01, 4))  # -1.0% to +7.0% annual alpha
    beta = float(round(0.85 + (seed % 6) * 0.10, 2))  # Market beta: 0.85 to 1.35
    commitment = 100.0

    # 3. Capital Calls: Paced over first 4 years (t <= 4.0, steps 0 to 8)
    base_weights = np.array([0.18, 0.12, 0.18, 0.14, 0.14, 0.10, 0.08, 0.04, 0.02] + [0.0] * 12)
    noise = rng.uniform(0.92, 1.08, len(base_weights))
    call_weights = base_weights * noise
    call_weights = (call_weights / float(np.sum(call_weights))) * commitment
    calls = np.round(call_weights, 4)

    # 4. Distributions & Unrealized NAV Generation
    distributions = np.zeros(len(times), dtype=np.float64)
    nav = 0.0

    for i in range(len(times)):
        if calls[i] <= 0:
            continue
        c = float(calls[i])
        # Later tranches remain unrealized at year 10 (harvesting tail NAV)
        hold = 6.5 + float(rng.uniform(0.0, 2.0)) if i >= 6 else 3.5 + float(rng.uniform(0.0, 3.5))
        exit_t = min(times[i] + hold, 10.0)
        exit_idx = int(np.round(exit_t / dt))
        idx_start, idx_end = i, exit_idx
        if idx_end > idx_start:
            mkt_growth = float(bench_prices[idx_end] / bench_prices[idx_start])
            cum_log_m = float(np.log(mkt_growth))
            actual_hold = (idx_end - idx_start) * dt
            fund_growth = float(np.exp(beta * cum_log_m + true_alpha * actual_hold))
        else:
            fund_growth = 1.0
        proceeds = c * fund_growth
        if exit_idx < len(times) - 1:
            distributions[exit_idx] += proceeds
        else:
            nav += proceeds

    distributions = np.round(distributions, 4)
    nav = float(round(nav, 4))

    return {
        "seed": seed,
        "true_alpha": true_alpha,
        "beta": beta,
        "commitment": commitment,
        "times": times.tolist(),
        "calls": calls.tolist(),
        "distributions": distributions.tolist(),
        "nav": nav,
        "benchmark_prices": bench_prices.tolist(),
    }
