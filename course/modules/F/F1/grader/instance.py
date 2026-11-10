"""Instance generator for F1: Data & Methodology (Atlas A7).

Produces deterministic cross-sectional panels, delisting records, characteristics,
and factor time series for seeds 0-49.
"""

from __future__ import annotations

import numpy as np


def make_instance(seed: int) -> dict[str, object]:
    """Generate a deterministic cross-sectional testing instance.

    Parameters:
        seed: non-negative integer seed.

    Returns:
        dict containing:
            - n_stocks: int
            - n_months: int
            - exchange_codes: (N,) int32 ndarray (1=NYSE, 2=AMEX, 3=NASDAQ)
            - market_caps: (N,) float64 ndarray (positive firm market equities)
            - signal1 (book_to_market): (N,) float64 ndarray
            - signal2 (momentum): (N,) float64 ndarray
            - raw_returns: (N,) float64 ndarray
            - delist_codes: (N,) int32 ndarray (100=active, 200=merger, 500-584=performance)
            - delist_returns: (N,) float64 ndarray (with np.nan for missing/active)
            - panel_excess: (T, N_assets) float64 ndarray of asset excess returns
            - panel_factors: (T, K) float64 ndarray of benchmark factor excess returns
            - true_betas: (N_assets, K) float64 ndarray of asset factor loadings
    """
    rng = np.random.default_rng(seed)

    n_stocks = 120 + (seed % 11) * 2  # 120 to 140 stocks
    n_months = 72  # 6 years of monthly observations
    n_assets = 25  # 25 test portfolios / assets
    k_factors = 3  # 3 factors (Market, SMB, HML)

    # 1. Exchange allocation: ~35% NYSE (1), ~15% AMEX (2), ~50% NASDAQ (3)
    ex_probs = np.array([0.35, 0.15, 0.50])
    exchange_codes = rng.choice(np.array([1, 2, 3], dtype=np.int32), size=n_stocks, p=ex_probs)
    # Ensure at least 15 NYSE stocks for reliable breakpoint computation
    nyse_idx = np.where(exchange_codes == 1)[0]
    if len(nyse_idx) < 15:
        exchange_codes[:15] = 1

    # 2. Market capitalization: Log-normal, NYSE systematically larger
    base_size = rng.lognormal(mean=4.0, sigma=1.2, size=n_stocks)
    # Scale NYSE up, NASDAQ down to reproduce empirical microcap concentration
    size_mult = np.where(exchange_codes == 1, 4.0, np.where(exchange_codes == 2, 1.2, 0.6))
    market_caps = np.round(base_size * size_mult * 100.0 + 10.0, 2)

    # 3. Signals: Book-to-market (log-normal) and 12-2 Momentum (normal)
    signal1 = np.round(np.exp(rng.normal(loc=-0.5, scale=0.6, size=n_stocks)), 4)
    signal2 = np.round(rng.normal(loc=0.08, scale=0.18, size=n_stocks), 4)

    # 4. Monthly raw returns before delisting
    raw_returns = np.round(rng.normal(loc=0.01, scale=0.07, size=n_stocks), 4)

    # 5. Delisting events: ~88% active (100), ~4% merger (200), ~8% distress (500-584)
    delist_codes = np.full(n_stocks, 100, dtype=np.int32)
    delist_returns = np.full(n_stocks, np.nan, dtype=np.float64)

    # Pick ~6-10 stocks for delisting
    delist_indices = rng.choice(n_stocks, size=min(8, n_stocks // 15), replace=False)
    for idx in delist_indices:
        code_type = rng.choice(["merger", "distress_with_ret", "distress_missing"])
        if code_type == "merger":
            delist_codes[idx] = 200
            delist_returns[idx] = round(rng.normal(0.10, 0.05), 4)  # positive takeover premium
        elif code_type == "distress_with_ret":
            delist_codes[idx] = int(rng.choice([500, 520, 552, 580]))
            delist_returns[idx] = round(rng.uniform(-0.60, -0.15), 4)
        else:  # distress with missing return (requires Shumway replacement)
            delist_codes[idx] = int(rng.choice([500, 560, 584]))
            delist_returns[idx] = np.nan

    # 6. Panel data for Fama-MacBeth & GRS testing
    # Factor excess returns: F_t ~ N(mu_f, Sigma_f)
    mu_factors = np.array([0.0065, 0.0025, 0.0035], dtype=np.float64)
    vol_factors = np.array([0.045, 0.030, 0.028], dtype=np.float64)
    corr_f = np.array(
        [
            [1.00, 0.15, -0.25],
            [0.15, 1.00, -0.10],
            [-0.25, -0.10, 1.00],
        ],
        dtype=np.float64,
    )
    cov_factors = np.diag(vol_factors) @ corr_f @ np.diag(vol_factors)
    l_f = np.linalg.cholesky(cov_factors)
    z_f = rng.normal(size=(n_months, k_factors))
    panel_factors = np.round(z_f @ l_f.T + mu_factors, 6)

    # True factor loadings for 25 assets
    # Betas spread systematically across size and value
    true_betas = np.empty((n_assets, k_factors), dtype=np.float64)
    for i in range(n_assets):
        b_mkt = 0.70 + 0.60 * (i / n_assets) + rng.normal(0.0, 0.05)
        b_smb = -0.50 + 1.00 * ((i % 5) / 4.0) + rng.normal(0.0, 0.05)
        b_hml = -0.40 + 0.90 * ((i // 5) / 4.0) + rng.normal(0.0, 0.05)
        true_betas[i] = [b_mkt, b_smb, b_hml]
    true_betas = np.round(true_betas, 4)

    # Asset alphas (some non-zero for testing GRS rejection)
    alphas = np.round(rng.normal(loc=0.001, scale=0.002, size=n_assets), 5)
    idiosyncratic_vols = np.round(rng.uniform(0.025, 0.055, size=n_assets), 4)

    # Generate asset excess returns: R_{i,t} = alpha_i + beta_i' F_t + eps_{i,t}
    panel_excess = np.empty((n_months, n_assets), dtype=np.float64)
    for t in range(n_months):
        eps_t = rng.normal(loc=0.0, scale=idiosyncratic_vols)
        panel_excess[t] = alphas + true_betas @ panel_factors[t] + eps_t
    panel_excess = np.round(panel_excess, 6)

    return {
        "seed": seed,
        "n_stocks": n_stocks,
        "n_months": n_months,
        "n_assets": n_assets,
        "k_factors": k_factors,
        "exchange_codes": exchange_codes,
        "market_caps": market_caps,
        "signal1": signal1,
        "signal2": signal2,
        "raw_returns": raw_returns,
        "delist_codes": delist_codes,
        "delist_returns": delist_returns,
        "panel_excess": panel_excess,
        "panel_factors": panel_factors,
        "true_betas": true_betas,
        "alphas": alphas,
    }
