"""Instance generator for GM2 project grader.

Generates deterministic, per-seed synthetic macroeconomic panels and asset returns
for real-time regime classification and regime-conditional asset allocation.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic synthetic macroeconomic instance for seed.

    Parameters
    ----------
    seed : int
        RNG seed derived from learner workspace.

    Returns
    -------
    dict[str, Any]
        Instance dictionary containing growth series, inflation series, multi-asset returns,
        and backtesting parameters.
    """
    rng = np.random.default_rng(seed)
    n_months = 240  # 20 years of monthly data
    n_assets = 4
    asset_names = ["US_Equity", "US_Treasury_10Y", "Commodities", "Trend_CTA"]

    # Underlying latent 4-state Markov chain
    # State 0: Goldilocks (Growth High, Inflation Low)
    # State 1: Reflation (Growth High, Inflation High)
    # State 2: Stagflation (Growth Low, Inflation High)
    # State 3: Deflationary Contraction (Growth Low, Inflation Low)
    p_trans = np.array(
        [
            [0.85, 0.10, 0.02, 0.03],
            [0.08, 0.82, 0.07, 0.03],
            [0.02, 0.06, 0.78, 0.14],
            [0.10, 0.02, 0.04, 0.84],
        ]
    )

    latent_states = np.zeros(n_months, dtype=int)
    latent_states[0] = int(rng.choice(4))
    for t in range(1, n_months):
        p_row = p_trans[latent_states[t - 1]]
        latent_states[t] = int(rng.choice(4, p=p_row))

    # Mean macroeconomic values conditional on state:
    # Goldilocks: growth ~ +3.0% ann (+0.25%/mo), inflation ~ +1.8% ann (+0.15%/mo)
    # Reflation:  growth ~ +3.6% ann (+0.30%/mo), inflation ~ +4.8% ann (+0.40%/mo)
    # Stagflation: growth ~ -1.2% ann (-0.10%/mo), inflation ~ +6.0% ann (+0.50%/mo)
    # Deflation:  growth ~ -2.4% ann (-0.20%/mo), inflation ~ +0.6% ann (+0.05%/mo)
    mu_growth = np.array([0.0025, 0.0030, -0.0010, -0.0020])
    mu_infl = np.array([0.0015, 0.0040, 0.0050, 0.0005])

    sigma_g = 0.0035 + 0.0005 * rng.uniform()
    sigma_pi = 0.0025 + 0.0005 * rng.uniform()

    growth = np.zeros(n_months)
    inflation = np.zeros(n_months)
    for t in range(n_months):
        s = latent_states[t]
        growth[t] = rng.normal(mu_growth[s], sigma_g)
        inflation[t] = rng.normal(mu_infl[s], sigma_pi)

    # Asset return parameters conditional on state:
    # 0: Goldilocks -> Eq +12%, Bond +4%, Comm +2%, CTA +6% (ann)
    # 1: Reflation  -> Eq +14%, Bond -2%, Comm +18%, CTA +12%
    # 2: Stagflation-> Eq -8%,  Bond -6%, Comm +22%, CTA +20%
    # 3: Deflation  -> Eq -15%, Bond +10%, Comm -12%, CTA +8%
    mu_assets = np.array(
        [
            [0.0100, 0.0033, 0.0017, 0.0050],  # Goldilocks
            [0.0117, -0.0017, 0.0150, 0.0100],  # Reflation
            [-0.0067, -0.0050, 0.0183, 0.0167],  # Stagflation
            [-0.0125, 0.0083, -0.0100, 0.0067],  # Deflation
        ]
    )

    base_sigmas = np.array([0.15, 0.07, 0.18, 0.12]) / np.sqrt(12.0)

    asset_returns = np.zeros((n_months, n_assets))
    for t in range(n_months):
        s = latent_states[t]
        # Correlation depends on regime (e.g. stock-bond correlation flip)
        rho_sb = 0.40 if s in (1, 2) else -0.35
        corr = np.array(
            [
                [1.0, rho_sb, 0.20, -0.05],
                [rho_sb, 1.0, -0.20, 0.05],
                [0.20, -0.20, 1.0, 0.25],
                [-0.05, 0.05, 0.25, 1.0],
            ]
        )
        cov = np.outer(base_sigmas, base_sigmas) * corr
        asset_returns[t] = rng.multivariate_normal(mu_assets[s], cov)

    return {
        "seed": seed,
        "n_months": n_months,
        "n_assets": n_assets,
        "asset_names": asset_names,
        "growth": growth,
        "inflation": inflation,
        "asset_returns": asset_returns,
        "lookback": 36,
        "burn_in": 24,
        "risk_aversion": 3.0,
        "transaction_cost_bps": 10.0,
    }
