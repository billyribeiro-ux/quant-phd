"""Deterministic instance generator for QR5 project: Deep Hedging vs. Delta Hedging.

Generates seeded market parameters, simulated Geometric Brownian Motion training paths,
and held-out test paths (including jump-diffusion stress paths) for evaluating
deep neural hedging policies, Black-Scholes delta hedging, and Whalley-Wilmott asymptotic bands.
"""

from __future__ import annotations

import functools
from typing import Any

import numpy as np


@functools.lru_cache(maxsize=128)
def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic deep hedging verification instance for the given seed."""
    rng = np.random.default_rng(seed)

    s0 = float(rng.uniform(90.0, 110.0))
    moneyness = float(rng.uniform(0.95, 1.05))
    strike = float(round(s0 * moneyness, 2))

    t_exp = float(rng.uniform(0.10, 0.25))  # roughly 25 to 63 trading days
    n_steps = int(rng.integers(15, 26))  # 15 to 25 rebalancing steps
    dt = t_exp / n_steps

    sigma = float(rng.uniform(0.18, 0.32))
    mu = float(rng.uniform(0.02, 0.08))
    r = float(rng.uniform(0.01, 0.05))

    cost_rate = float(rng.uniform(0.002, 0.008))  # 20 to 80 bps proportional transaction cost
    risk_aversion = float(rng.uniform(0.5, 2.0))  # absolute risk aversion gamma
    alpha = 0.95  # Expected Shortfall / CVaR confidence level

    n_train_paths = 500
    n_test_paths = 250

    # 1. Simulate GBM training paths
    # dS_t = mu S_t dt + sigma S_t dW_t
    train_shocks = rng.normal(0.0, 1.0, size=(n_train_paths, n_steps))
    train_paths = np.zeros((n_train_paths, n_steps + 1), dtype=np.float64)
    train_paths[:, 0] = s0
    drift_factor = (mu - 0.5 * sigma**2) * dt
    vol_factor = sigma * np.sqrt(dt)

    for step in range(n_steps):
        train_paths[:, step + 1] = train_paths[:, step] * np.exp(drift_factor + vol_factor * train_shocks[:, step])

    # 2. Simulate held-out GBM test paths
    test_shocks = rng.normal(0.0, 1.0, size=(n_test_paths, n_steps))
    test_paths = np.zeros((n_test_paths, n_steps + 1), dtype=np.float64)
    test_paths[:, 0] = s0
    for step in range(n_steps):
        test_paths[:, step + 1] = test_paths[:, step] * np.exp(drift_factor + vol_factor * test_shocks[:, step])

    # 3. Simulate held-out Jump-Diffusion stress paths (Merton 1976 jump diffusion)
    # Compound Poisson jumps: lambda_j jumps per year, log-jump size ~ Normal(mu_j, sigma_j^2)
    lambda_j = float(rng.uniform(1.0, 3.0))
    mu_j = float(rng.uniform(-0.10, -0.02))
    sigma_j = float(rng.uniform(0.05, 0.15))

    test_jump_paths = np.zeros((n_test_paths, n_steps + 1), dtype=np.float64)
    test_jump_paths[:, 0] = s0
    jump_shocks = rng.normal(0.0, 1.0, size=(n_test_paths, n_steps))
    poisson_counts = rng.poisson(lambda_j * dt, size=(n_test_paths, n_steps))

    for step in range(n_steps):
        n_jumps = poisson_counts[:, step]
        jump_amplitude = np.zeros(n_test_paths, dtype=np.float64)
        has_jumps = n_jumps > 0
        if np.any(has_jumps):
            jump_amplitude[has_jumps] = rng.normal(
                mu_j * n_jumps[has_jumps],
                sigma_j * np.sqrt(n_jumps[has_jumps]),
            )
        total_increment = drift_factor + vol_factor * jump_shocks[:, step] + jump_amplitude
        test_jump_paths[:, step + 1] = test_jump_paths[:, step] * np.exp(total_increment)

    # 4. Neural hedging hyperparameters
    hidden_dim = 16
    epochs = 25
    lr = 0.015

    return {
        "seed": seed,
        "s0": s0,
        "strike": strike,
        "t_exp": t_exp,
        "n_steps": n_steps,
        "dt": dt,
        "sigma": sigma,
        "mu": mu,
        "r": r,
        "cost_rate": cost_rate,
        "risk_aversion": risk_aversion,
        "alpha": alpha,
        "n_train_paths": n_train_paths,
        "n_test_paths": n_test_paths,
        "train_paths": train_paths,
        "test_paths": test_paths,
        "test_jump_paths": test_jump_paths,
        "lambda_j": lambda_j,
        "mu_j": mu_j,
        "sigma_j": sigma_j,
        "hidden_dim": hidden_dim,
        "epochs": epochs,
        "lr": lr,
    }
