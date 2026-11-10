"""Instance generator for S5 project: Two-pass Fama-MacBeth and Shanken correction.

SIMULATED: generates deterministic pseudo-random synthetic panels of asset excess returns
and factor series for seeds 0-49.
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
            excess: (T, N) ndarray of float64 asset excess returns
            factors: (T, K) ndarray of float64 factor returns
            train: integer count of months reserved for first-pass time-series regression
            seed: integer seed
            T: total number of months
            N: number of test assets
            K: number of priced factors
    """
    rng = np.random.default_rng(seed)

    # Vary dimensions deterministically across seeds
    t_months = 130 + int((seed * 7) % 50)  # [130, 179]
    n_assets = 14 + int((seed * 3) % 9)  # [14, 22]
    k_factors = 1 + int(seed % 3)  # [1, 3]

    # Ensure train >= K + 2 and T - train >= 2
    train = int(t_months * 0.60)

    # Factor covariance matrix Sigma_f (positive definite, non-identity)
    a = rng.uniform(0.1, 0.4, size=(k_factors, k_factors))
    cov_f = a @ a.T + 0.001 * np.eye(k_factors)
    # Scale diagonal to typical monthly asset variances (~0.0015 to 0.0035)
    scale_vec = np.array([0.0025, 0.0018, 0.0022][:k_factors])
    d_inv_sqrt = np.diag(1.0 / np.sqrt(np.diag(cov_f)))
    corr_f = d_inv_sqrt @ cov_f @ d_inv_sqrt
    sigma_f = np.diag(np.sqrt(scale_vec)) @ corr_f @ np.diag(np.sqrt(scale_vec))

    # Factor expected returns (monthly risk premia ~40 to 80 bps)
    mu_f = np.array([0.008, 0.005, 0.006][:k_factors])
    factors = rng.multivariate_normal(mu_f, sigma_f, size=t_months)

    # True factor loadings (N, K)
    true_loadings = rng.uniform(0.5, 1.5, size=(n_assets, k_factors))
    # True alphas (near zero with small dispersion)
    true_alphas = rng.normal(0.0, 0.001, size=n_assets)

    # Idiosyncratic variance matrix (diagonal, 2% - 5% monthly volatility)
    resid_sd = rng.uniform(0.02, 0.05, size=n_assets)

    # Generate excess returns: R_it = alpha_i + beta_i' f_t + e_it
    excess = np.empty((t_months, n_assets), dtype=np.float64)
    for t in range(t_months):
        e_t = rng.normal(0.0, resid_sd, size=n_assets)
        excess[t] = true_alphas + true_loadings @ factors[t] + e_t

    return {
        "excess": excess,
        "factors": factors,
        "train": train,
        "seed": seed,
        "T": t_months,
        "N": n_assets,
        "K": k_factors,
    }
