"""Instance generator for PM3 project: Unsmoothing private credit returns.

Generates realistic quarterly reported private credit return series alongside
a public syndicated leveraged loan proxy series across deterministic RNG seeds.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a reproducible test instance for a given integer seed.

    Parameters
    ----------
    seed : int
        Deterministic random number generator seed.

    Returns
    -------
    dict[str, Any]
        Dictionary containing reported_returns, public_proxy_returns, and rf_quarterly.
    """
    rng = np.random.default_rng(seed)
    n_quarters = 40  # 10 years of quarterly observations

    # Baseline market parameters: public leveraged loan proxy
    # Average ~7.0% - 8.5% annualized return, ~6.5% - 8.0% annualized volatility
    mu_m = 0.018 + 0.003 * rng.uniform(0.0, 1.0)
    sigma_m = 0.035 + 0.006 * rng.uniform(0.0, 1.0)
    rf_q = 0.0050 + 0.0015 * rng.uniform(0.0, 1.0)  # ~2.0% - 2.6% annualized

    proxy_returns = rng.normal(mu_m, sigma_m, size=n_quarters)

    # True unobserved private credit parameters:
    # Direct lending pays ~200-350 bps illiquidity spread over public loans, beta ~ 1.0 - 1.15
    beta_true = 1.00 + 0.15 * rng.uniform(0.0, 1.0)
    alpha_true = 0.006 + 0.003 * rng.uniform(0.0, 1.0)  # robust positive excess return
    noise_sigma = 0.008 + 0.004 * rng.uniform(0.0, 1.0)
    noise = rng.normal(0.0, noise_sigma, size=n_quarters)

    true_returns = alpha_true + beta_true * proxy_returns + noise

    # Appraisal smoothing decay factor phi (0.50 to 0.68 in middle-market private debt)
    phi = 0.52 + 0.16 * rng.uniform(0.0, 1.0)

    # Generate reported returns under AR(1) smoothing
    reported_returns = np.zeros(n_quarters)
    reported_returns[0] = true_returns[0]
    for t in range(1, n_quarters):
        reported_returns[t] = phi * reported_returns[t - 1] + (1.0 - phi) * true_returns[t]

    return {
        "seed": seed,
        "n_quarters": n_quarters,
        "reported_returns": reported_returns,
        "public_proxy_returns": proxy_returns,
        "rf_quarterly": float(rf_q),
        "true_phi": float(phi),
    }
