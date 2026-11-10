"""Deterministic instance generator for Atlas A18 Nowcasting & Macro Dashboard.

Generates reproducible macroeconomic panels, ragged-edge vintages, announcement data,
and cross-asset returns parameterized by seed.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a valid, deterministic macro test instance for Atlas A18."""
    rng = np.random.default_rng(seed)

    t_bal = 120
    t_ragged = 36
    n_series = 10
    n_factors = 2
    n_assets = 4

    # 1. Stable VAR(1) transition matrix for factors
    a11 = 0.55 + 0.15 * float(rng.uniform(-0.5, 0.5))
    a22 = 0.45 + 0.15 * float(rng.uniform(-0.5, 0.5))
    a12 = 0.08 * float(rng.uniform(-0.5, 0.5))
    a21 = -0.06 * float(rng.uniform(-0.5, 0.5))
    trans_a = np.array([[a11, a12], [a21, a22]], dtype=np.float64)

    # Simulate true latent factors
    factors_bal = np.zeros((t_bal, n_factors), dtype=np.float64)
    q_cov = np.diag([0.25, 0.20]) + 0.02
    chol_q = np.linalg.cholesky(q_cov)
    for t in range(1, t_bal):
        shocks = chol_q @ rng.standard_normal(n_factors)
        factors_bal[t] = trans_a @ factors_bal[t - 1] + shocks

    # Loadings with structural macro characteristics (first = real activity, second = price/rates)
    loadings = np.zeros((n_series, n_factors), dtype=np.float64)
    loadings[:, 0] = rng.uniform(0.4, 0.9, size=n_series)
    loadings[:, 1] = rng.uniform(-0.6, 0.6, size=n_series)

    # Measurement noise
    noise_std = rng.uniform(0.2, 0.4, size=n_series)
    e_bal = rng.standard_normal((t_bal, n_series)) * noise_std
    x_bal = factors_bal @ loadings.T + e_bal

    # Shift & scale to realistic macro indicator units
    base_means = rng.uniform(1.5, 4.0, size=n_series)
    base_stds = rng.uniform(0.8, 2.5, size=n_series)
    x_bal = x_bal * base_stds + base_means

    # Target series (e.g. GDP quarterly annualized growth)
    target_bal = 1.2 * factors_bal[:, 0] - 0.4 * factors_bal[:, 1] + 0.2 * rng.standard_normal(t_bal)

    # 2. Ragged panel for nowcasting
    factors_rag = np.zeros((t_ragged, n_factors), dtype=np.float64)
    for t in range(1, t_ragged):
        shocks = chol_q @ rng.standard_normal(n_factors)
        factors_rag[t] = trans_a @ factors_rag[t - 1] + shocks
    e_rag = rng.standard_normal((t_ragged, n_series)) * noise_std
    x_rag = (factors_rag @ loadings.T + e_rag) * base_stds + base_means

    # Inject ragged edge at terminal periods:
    # At T-2: 3 indicators unreleased (lagged)
    # At T-1: 6 indicators unreleased
    x_ragged_old = x_rag.copy()
    x_ragged_old[-2, [1, 4, 7]] = np.nan
    x_ragged_old[-1, [0, 1, 3, 4, 6, 7]] = np.nan

    # New vintage: release arrives for indicator 1 at T-2 and indicator 0, 3 at T-1, plus revision to indicator 2 at T-3
    x_ragged_new = x_ragged_old.copy()
    x_ragged_new[-2, 1] = x_rag[-2, 1]
    x_ragged_new[-1, 0] = x_rag[-1, 0]
    x_ragged_new[-1, 3] = x_rag[-1, 3]
    x_ragged_new[-3, 2] += float(rng.uniform(0.1, 0.3))

    # 3. Macro surprises data
    n_surprises = 60
    hist_std = rng.uniform(0.5, 2.0, size=n_series)
    consensus = rng.normal(2.0, 1.0, size=(n_surprises, n_series))
    errors = rng.normal(0.0, 1.0, size=(n_surprises, n_series)) * hist_std
    actuals = consensus + errors
    weights = rng.uniform(0.1, 1.0, size=n_series)
    weights /= float(np.sum(weights))

    # 4. Regime series
    t_regimes = 100
    growth_sig = np.sin(np.linspace(0, 4 * np.pi, t_regimes)) + rng.normal(0, 0.2, t_regimes)
    inflation_sig = np.cos(np.linspace(0, 4 * np.pi, t_regimes)) + rng.normal(0, 0.2, t_regimes)

    # 5. Asset returns (Equities, Bonds, Commodities, FX)
    asset_betas = np.array(
        [
            [0.8, -0.2],  # Equities: pro-growth, anti-inflation
            [-0.3, -0.7],  # Bonds: anti-growth, anti-inflation
            [0.5, 0.9],  # Commodities: pro-growth, pro-inflation
            [0.2, 0.3],  # FX / USD
        ],
        dtype=np.float64,
    )
    macro_sig = np.column_stack([growth_sig, inflation_sig])
    noise_ret = rng.normal(0, 0.01, size=(t_regimes, n_assets))
    asset_returns = macro_sig @ asset_betas.T * 0.01 + noise_ret

    return {
        "seed": seed,
        "n_factors": n_factors,
        "x_balanced": x_bal,
        "target_balanced": target_bal,
        "x_ragged_old": x_ragged_old,
        "x_ragged_new": x_ragged_new,
        "actuals": actuals,
        "consensus": consensus,
        "historical_std": hist_std,
        "surprise_weights": weights,
        "growth_signal": growth_sig,
        "inflation_signal": inflation_sig,
        "asset_returns": asset_returns,
        "macro_signals": macro_sig,
    }
