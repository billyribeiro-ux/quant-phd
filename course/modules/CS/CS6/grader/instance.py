"""CS6 Project Instance Generator.

Generates deterministic problem instances for full-portfolio Monte Carlo VaR simulation
with reproducible parallel RNG streams.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic, valid problem instance from an integer seed."""
    rng = np.random.default_rng(seed)

    n_assets = int(rng.integers(3, 6))
    s0 = [float(x) for x in np.round(rng.uniform(60.0, 140.0, size=n_assets), 2)]
    weights = [float(x) for x in np.round(rng.uniform(-15.0, 35.0, size=n_assets), 2)]
    volatilities = [float(x) for x in np.round(rng.uniform(0.15, 0.35, size=n_assets), 4)]
    drift = float(np.round(rng.uniform(0.02, 0.05), 4))
    horizon = float(np.round(rng.choice([1.0, 5.0, 10.0]) / 252.0, 6))
    n_paths = int(rng.choice([4000, 6000, 8000]))
    alpha = float(rng.choice([0.95, 0.99]))
    base_seed = int(seed * 10007 + 13)

    # Positive definite correlation matrix
    raw = rng.normal(size=(n_assets, n_assets))
    cov = raw @ raw.T + float(n_assets) * np.eye(n_assets)
    d = np.sqrt(np.diag(cov))
    corr = cov / np.outer(d, d)
    corr_list: list[list[float]] = [[float(np.round(corr[i, j], 6)) for j in range(n_assets)] for i in range(n_assets)]
    # Ensure exact unit diagonal
    for i in range(n_assets):
        corr_list[i][i] = 1.0

    # Options portfolios: European calls and puts
    n_options = int(rng.integers(2, 5))
    option_underlyings: list[int] = []
    option_strikes: list[float] = []
    option_expiries: list[float] = []
    option_is_calls: list[bool] = []
    option_quantities: list[float] = []

    for _ in range(n_options):
        a_idx = int(rng.integers(0, n_assets))
        strike = float(np.round(s0[a_idx] * rng.uniform(0.9, 1.1), 2))
        expiry = float(np.round(horizon + rng.uniform(0.1, 0.5), 4))
        is_call = bool(rng.choice([True, False]))
        qty = float(np.round(rng.uniform(-10.0, 20.0), 2))

        option_underlyings.append(a_idx)
        option_strikes.append(strike)
        option_expiries.append(expiry)
        option_is_calls.append(is_call)
        option_quantities.append(qty)

    return {
        "n_assets": n_assets,
        "s0": s0,
        "weights": weights,
        "volatilities": volatilities,
        "drift": drift,
        "corr_matrix": corr_list,
        "horizon": horizon,
        "option_underlyings": option_underlyings,
        "option_strikes": option_strikes,
        "option_expiries": option_expiries,
        "option_is_calls": option_is_calls,
        "option_quantities": option_quantities,
        "n_paths": n_paths,
        "alpha": alpha,
        "base_seed": base_seed,
    }
