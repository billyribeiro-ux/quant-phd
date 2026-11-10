"""Instance generator for F5: Replication-Crisis Adjudication Engine.

Generates deterministic empirical factor panels across 10 candidate anomalies,
4 benchmark factors, and 25 test assets from a single random seed.
"""

from __future__ import annotations

import numpy as np


def make_instance(seed: int) -> dict[str, object]:
    """Generate a deterministic factor adjudication instance from an integer seed."""
    rng = np.random.default_rng(seed)
    n_months = 240
    n_candidates = 10
    n_controls = 4
    n_assets = 25

    candidate_names = [
        "Accruals",
        "NetShareIssuance",
        "AssetGrowth",
        "GrossProfitability",
        "Momentum12M",
        "IdiosyncraticVol",
        "CompositeEquity",
        "InvestmentToAssets",
        "OperatingLeverage",
        "OhlsonOScore",
    ]

    # 1. Simulate 4 benchmark control factors: Market, Size, Value, Momentum
    mkt = rng.normal(0.060 / 12, 0.155 / np.sqrt(12), size=n_months)
    smb = rng.normal(0.025 / 12, 0.095 / np.sqrt(12), size=n_months)
    hml = rng.normal(0.035 / 12, 0.110 / np.sqrt(12), size=n_months)
    umd = rng.normal(0.065 / 12, 0.140 / np.sqrt(12), size=n_months)
    controls = np.column_stack([mkt, smb, hml, umd]).astype(np.float64)

    # 2. Simulate 25 test assets (Size-Value portfolios)
    b_assets = rng.uniform(0.6, 1.4, size=(n_assets, n_controls))
    e_assets = rng.normal(0.0, 0.035, size=(n_assets, n_months))
    test_assets = (b_assets @ controls.T + e_assets).astype(np.float64)

    # 3. Simulate 10 candidate anomalies with targeted cross-sectional profiles:
    # Cand 0: Guaranteed ROBUST factor (high large-cap alpha, survives double selection)
    # Cand 1-3: Microcap-skewed candidates (strong in EW, negligible in VW)
    # Cand 4-6: Factor-spanned candidates (strong correlation with HML/UMD/SMB)
    # Cand 7-9: Noise candidates (pure random shocks, data snooping)
    returns_ew = np.zeros((n_candidates, n_months), dtype=np.float64)
    returns_vw = np.zeros((n_candidates, n_months), dtype=np.float64)

    for i in range(n_candidates):
        noise_vw = rng.normal(0.0, 0.015, size=n_months)
        noise_ew = rng.normal(0.0, 0.010, size=n_months)

        if i == 0:  # Guaranteed ROBUST
            true_alpha = 0.0090 + 0.0010 * rng.uniform(-1, 1)  # ~11% ann
            r_c = true_alpha + 0.10 * mkt + noise_vw
            returns_vw[i, :] = r_c
            returns_ew[i, :] = r_c + 0.0030 + noise_ew
        elif i in (1, 2, 3):  # Microcap-skewed candidates
            returns_vw[i, :] = 0.0003 + 0.10 * mkt + noise_vw
            returns_ew[i, :] = returns_vw[i, :] + 0.0070 + noise_ew
        elif i in (4, 5, 6):  # Factor-spanned candidates
            loadings = np.array([0.25, 0.35, 0.70, 0.55])
            spanned_ret = controls @ loadings
            returns_vw[i, :] = spanned_ret + noise_vw
            returns_ew[i, :] = spanned_ret + 0.0030 + noise_ew
        else:  # Noise / data snooping
            returns_vw[i, :] = noise_vw
            returns_ew[i, :] = noise_vw + noise_ew

    return {
        "seed": int(seed),
        "n_months": int(n_months),
        "n_candidates": int(n_candidates),
        "n_controls": int(n_controls),
        "n_assets": int(n_assets),
        "candidate_names": candidate_names,
        "controls": controls,
        "test_assets": test_assets,
        "returns_ew": returns_ew,
        "returns_vw": returns_vw,
    }
