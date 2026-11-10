"""Instance generator for AP3 project: Euler-Equation GMM & Hansen-Jagannathan Engine.

SIMULATED: generates deterministic pseudo-random synthetic panels of aggregate
consumption growth, gross asset returns, and instruments for seeds 0-49.
Asset returns are generated in exact population equilibrium under CCAPM
Euler orthogonality: E[beta * (c'/c)^(-gamma) * R_i] = 1.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic synthetic asset pricing panel instance.

    Parameters:
        seed: integer pseudo-random seed in range [0, 49].

    Returns:
        dict containing:
            seed: integer seed
            T: sample size
            N: number of test assets
            L: number of instruments
            c_growth: (T,) ndarray of float64 consumption growth ratios c_{t+1}/c_t
            gross_returns: (T, N) ndarray of float64 gross asset returns
            instruments: (T, L) ndarray of float64 instrument matrix
            nu_grid: (K,) ndarray of float64 candidate SDF means for HJ bound
            beta_true: float true discount factor
            gamma_true: float true risk aversion parameter
    """
    rng = np.random.default_rng(seed)

    # Vary dimensions deterministically across seeds
    t_periods = 160 + int((seed * 7) % 40)  # [160, 199]
    n_assets = 2 + int(seed % 2)  # 2 or 3 assets
    l_instruments = 2  # constant + lagged consumption growth

    beta_true = 0.98
    gamma_true = 2.0 + float(seed % 5) * 0.1  # [2.0, 2.4]

    # Consumption growth log(c_{t+1}/c_t) ~ N(mu_c, sigma_c^2)
    mu_c = 0.018
    sigma_c = 0.022
    log_gc = rng.normal(mu_c, sigma_c, size=t_periods)
    c_growth = np.exp(log_gc)
    standardized_c = (log_gc - mu_c) / sigma_c

    # Risk-free log return in population: ln R_f = -ln(beta) + gamma*mu_c - 0.5*gamma^2*sigma_c^2
    rf_log = -np.log(beta_true) + gamma_true * mu_c - 0.5 * (gamma_true * sigma_c) ** 2

    # Asset return configurations: (volatility sigma_i, consumption correlation rho_i)
    specs = [
        (0.006, 0.00),  # Asset 0: low-volatility bond proxy
        (0.080, 0.65),  # Asset 1: equity proxy
        (0.035, 0.40),  # Asset 2: intermediate duration asset
    ]

    gross_returns = np.empty((t_periods, n_assets), dtype=np.float64)
    for i in range(n_assets):
        sigma_i, rho_i = specs[i]
        # In population: mu_i = rf_log - 0.5 * sigma_i^2 + gamma * rho_i * sigma_c * sigma_i
        cov_ic = gamma_true * rho_i * sigma_c * sigma_i
        mu_i = rf_log - 0.5 * (sigma_i**2) + cov_ic

        idiosyncratic = rng.normal(0.0, 1.0, size=t_periods)
        z_i = rho_i * standardized_c + np.sqrt(max(0.0, 1.0 - rho_i**2)) * idiosyncratic
        log_r = mu_i + sigma_i * z_i
        gross_returns[:, i] = np.exp(log_r)

    # Instruments: constant (1.0) and lagged consumption growth
    instruments = np.empty((t_periods, l_instruments), dtype=np.float64)
    instruments[:, 0] = 1.0
    instruments[0, 1] = np.exp(mu_c)
    instruments[1:, 1] = c_growth[:-1]

    # Grid of candidate SDF expectations for Hansen-Jagannathan bound
    nu_grid = np.linspace(0.90, 1.05, 16)

    return {
        "seed": seed,
        "T": t_periods,
        "N": n_assets,
        "L": l_instruments,
        "c_growth": c_growth,
        "gross_returns": gross_returns,
        "instruments": instruments,
        "nu_grid": nu_grid,
        "beta_true": beta_true,
        "gamma_true": gamma_true,
    }
