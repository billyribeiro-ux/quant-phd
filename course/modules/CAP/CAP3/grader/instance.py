"""Instance generator for CAP3: Qualifying Examination Capstone Grader.

Generates deterministic problem instances for the three doctoral field examinations:
1. Field Prelim I: Asset Pricing & Continuous-Time Valuation
2. Field Prelim II: Cross-Sectional & Time-Series Econometrics
3. Field Prelim III: Dynamic General Equilibrium & Monetary Macro
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a reproducible, seed-dependent qualifying examination instance.

    Args:
        seed: Integer seed for reproducible pseudo-random generation.

    Returns:
        Dictionary containing problem instances across the three field prelims with flat keys.
    """
    rng = np.random.default_rng(seed)

    # -------------------------------------------------------------
    # 1. Field Prelim I: Asset Pricing & Continuous-Time Valuation
    # -------------------------------------------------------------
    n_assets = 4
    base_mu = np.array([0.06, 0.08, 0.05, 0.09])
    mu = base_mu + rng.uniform(-0.01, 0.01, size=n_assets)

    # Positive-definite covariance matrix
    a_mat = rng.normal(0.0, 0.03, size=(n_assets, n_assets))
    diag_vars = np.array([0.035, 0.045, 0.025, 0.055]) + rng.uniform(0.001, 0.005, size=n_assets)
    sigma_ap = a_mat @ a_mat.T + np.diag(diag_vars)

    rf = float(0.025 + rng.uniform(-0.005, 0.005))
    gamma = float(3.5 + rng.uniform(-0.5, 1.5))
    mu_stock = float(0.08 + rng.uniform(-0.01, 0.02))
    sigma_stock = float(0.18 + rng.uniform(-0.02, 0.04))
    rho = float(0.03 + rng.uniform(-0.005, 0.01))

    # -------------------------------------------------------------
    # 2. Field Prelim II: Cross-Sectional & Time-Series Econometrics
    # -------------------------------------------------------------
    t_obs = 120
    n_test_assets = 5
    n_factors = 2

    # Factor returns series (e.g. Market and Value factors)
    f_means = np.array([0.006, 0.003]) + rng.uniform(-0.001, 0.001, size=2)
    f_chol = np.array([[0.045, 0.0], [0.015, 0.035]])
    factors = rng.normal(size=(t_obs, n_factors)) @ f_chol.T + f_means

    # True factor loadings (betas) and intercepts (alphas)
    true_betas = np.array(
        [
            [0.8, -0.2],
            [1.1, 0.4],
            [0.9, 0.1],
            [1.3, -0.3],
            [0.7, 0.5],
        ]
    ) + rng.uniform(-0.05, 0.05, size=(n_test_assets, n_factors))
    true_alphas = np.array([0.001, -0.002, 0.0005, 0.0015, -0.001]) + rng.uniform(-0.0002, 0.0002, size=n_test_assets)

    # Asset returns with idiosyncratic noise
    residuals = rng.normal(0.0, 0.02, size=(t_obs, n_test_assets))
    returns = np.zeros((t_obs, n_test_assets))
    for t in range(t_obs):
        returns[t] = true_alphas + true_betas @ factors[t] + residuals[t]

    # GMM Euler equation moment diagnostics
    gmm_n_obs = 200
    gmm_moments = 4
    gmm_params = 2
    sample_g = np.array([0.008, -0.004, 0.006, -0.002]) + rng.uniform(-0.001, 0.001, size=gmm_moments)
    w_raw = rng.normal(0.0, 0.1, size=(gmm_moments, gmm_moments))
    weighting_matrix = w_raw @ w_raw.T + np.eye(gmm_moments) * 2.0

    # -------------------------------------------------------------
    # 3. Field Prelim III: Dynamic General Equilibrium & Monetary Macro
    # -------------------------------------------------------------
    futures_price_change = float(-0.015 + rng.uniform(-0.008, 0.012))
    announcement_day = int(rng.integers(8, 22))
    days_in_month = 30 if (seed % 2 == 0) else 31

    # 3-equation New Keynesian parameters
    beta_discount = 0.99
    sigma_crra = float(1.0 + rng.uniform(-0.1, 0.2))
    kappa_slope = float(0.12 + rng.uniform(-0.02, 0.04))
    phi_pi = float(1.5 + rng.uniform(-0.2, 0.4))
    phi_y = float(0.5 + rng.uniform(-0.1, 0.2))

    # Local projections time series
    lp_t = 80
    shocks = rng.normal(0.0, 0.25, size=lp_t)
    outcomes = np.zeros(lp_t)
    # Generate dynamic AR(1) macroeconomic response to monetary shocks
    for t in range(1, lp_t):
        outcomes[t] = 0.65 * outcomes[t - 1] - 0.45 * shocks[t] + rng.normal(0.0, 0.15)

    return {
        "seed": seed,
        # Field Prelim I: Asset Pricing & Continuous-Time Valuation
        "mu": mu,
        "sigma": sigma_ap,
        "rf": rf,
        "gamma": gamma,
        "mu_stock": mu_stock,
        "sigma_stock": sigma_stock,
        "rho": rho,
        # Field Prelim II: Cross-Sectional & Time-Series Econometrics
        "t_obs": t_obs,
        "returns": returns,
        "factors": factors,
        "gmm_n_obs": gmm_n_obs,
        "gmm_moments": gmm_moments,
        "gmm_params": gmm_params,
        "sample_g": sample_g,
        "weighting_matrix": weighting_matrix,
        # Field Prelim III: Dynamic General Equilibrium & Monetary Macro
        "futures_price_change": futures_price_change,
        "announcement_day": announcement_day,
        "days_in_month": days_in_month,
        "beta_discount": beta_discount,
        "sigma_crra": sigma_crra,
        "kappa_slope": kappa_slope,
        "phi_pi": phi_pi,
        "phi_y": phi_y,
        "shocks": shocks,
        "outcomes": outcomes,
        "max_horizon": 4,
    }
