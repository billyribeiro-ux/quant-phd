"""Instance generator for Module F2 Project: Factor-Model Horse Race.

Generates reproducible synthetic 30-year monthly return histories (T=360 months)
for CAPM, Fama-French 3, Carhart 4, Fama-French 5, and the Hou-Xue-Zhang q-factor
models alongside 25 test assets (mimicking 5x5 Size-BM portfolios).
"""

from __future__ import annotations

import numpy as np


def make_instance(seed: int) -> dict[str, object]:
    """Generate a deterministic factor horse race dataset from a single seed.

    Parameters
    ----------
    seed : int
        RNG seed for reproducibility.

    Returns
    -------
    dict[str, object]
        Contains test asset returns (360 x 25), individual factor arrays, and metadata.
    """
    rng = np.random.default_rng(seed)
    n_months = 360  # 30 years
    n_assets = 25  # 25 test portfolios
    train_len = 240  # 20 years in-sample, 10 years out-of-sample

    # 1. Base factor simulation with realistic empirical moments
    # Market excess return: ~6.5% mean, 15.5% annual vol
    mkt = rng.normal(0.065 / 12, 0.155 / np.sqrt(12), size=n_months)

    # Size factor (SMB): ~2.5% mean, 10.0% vol
    smb = rng.normal(0.025 / 12, 0.100 / np.sqrt(12), size=n_months)

    # Profitability (RMW): ~3.8% mean, 8.0% vol
    rmw = rng.normal(0.038 / 12, 0.080 / np.sqrt(12), size=n_months)

    # Investment (CMA): ~3.2% mean, 7.0% vol
    cma = rng.normal(0.032 / 12, 0.070 / np.sqrt(12), size=n_months)

    # Value (HML): Partially spanned by CMA and RMW + orthogonal component
    e_hml = rng.normal(0.0, 0.045 / np.sqrt(12), size=n_months)
    hml = (0.015 / 12) + 0.08 * mkt + 0.05 * smb - 0.28 * rmw + 0.88 * cma + e_hml

    # Momentum (WML): ~7.5% mean, 13.5% vol, largely unspanned by fundamentals
    wml_raw = rng.normal(0.075 / 12, 0.135 / np.sqrt(12), size=n_months)
    wml = wml_raw + (0.075 / 12 - float(np.mean(wml_raw)))

    # q-factor model components:
    # ME tracks SMB with slight noise
    q_me = smb + rng.normal(0.0, 0.015 / np.sqrt(12), size=n_months)
    # I/A tracks CMA
    q_ia = cma + rng.normal(0.0, 0.015 / np.sqrt(12), size=n_months)
    # ROE tracks RMW
    q_roe = rmw + rng.normal(0.0, 0.018 / np.sqrt(12), size=n_months)

    # Organize factor models as 2D float64 arrays (T x K)
    factors_capm = np.column_stack([mkt]).astype(np.float64)
    factors_ff3 = np.column_stack([mkt, smb, hml]).astype(np.float64)
    factors_carhart = np.column_stack([mkt, smb, hml, wml]).astype(np.float64)
    factors_ff5 = np.column_stack([mkt, smb, hml, rmw, cma]).astype(np.float64)
    factors_q_factor = np.column_stack([mkt, q_me, q_ia, q_roe]).astype(np.float64)

    # 2. Simulate 25 test assets (5x5 Size-BM grid)
    # Beta loadings dispersion across the grid
    b_mkt = rng.uniform(0.75, 1.25, size=n_assets)
    b_smb = np.repeat(np.linspace(0.8, -0.3, 5), 5) + rng.normal(0.0, 0.05, size=n_assets)
    b_hml = np.tile(np.linspace(-0.4, 0.7, 5), 5) + rng.normal(0.0, 0.05, size=n_assets)
    b_rmw = rng.uniform(-0.3, 0.4, size=n_assets)
    b_cma = rng.uniform(-0.3, 0.5, size=n_assets)

    # Asset pricing alphas (small residual cross-sectional pricing error)
    true_alphas = rng.normal(0.0, 0.012 / 12, size=n_assets)

    test_returns = np.zeros((n_months, n_assets), dtype=np.float64)
    for t in range(n_months):
        idio = rng.normal(0.0, 0.16 / np.sqrt(12), size=n_assets)
        test_returns[t, :] = (
            true_alphas + b_mkt * mkt[t] + b_smb * smb[t] + b_hml * hml[t] + b_rmw * rmw[t] + b_cma * cma[t] + idio
        )

    return {
        "seed": int(seed),
        "n_months": int(n_months),
        "n_assets": int(n_assets),
        "train_len": int(train_len),
        "test_returns": test_returns,
        "factors_capm": factors_capm,
        "factors_ff3": factors_ff3,
        "factors_carhart": factors_carhart,
        "factors_ff5": factors_ff5,
        "factors_q_factor": factors_q_factor,
    }
