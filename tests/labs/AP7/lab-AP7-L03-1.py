"""Lab AP7-L03-1: Baker & Wurgler (2006) Investor Sentiment Index & Cross-Sectional Predictability.

SIMULATED: Replicates the construction of an orthogonalized investor sentiment index
from multiple market proxies and tests its conditional cross-sectional return predictions
on high-volatility vs low-volatility portfolios (Baker & Wurgler 2006).
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    seed = 42
    rng = np.random.default_rng(seed)
    n_periods = 180  # 15 years monthly

    # 1. Macroeconomic control variables (IP growth, consumption, term spread, credit spread)
    macro = rng.normal([0.002, 0.0015, 0.015, 0.010], [0.008, 0.006, 0.007, 0.005], size=(n_periods, 4))

    # 2. Latent sentiment state
    phi_s = 0.80
    latent_s = np.zeros(n_periods)
    shocks = rng.normal(0.0, 0.6, size=n_periods)
    for t in range(1, n_periods):
        latent_s[t] = phi_s * latent_s[t - 1] + shocks[t]
    latent_s = (latent_s - np.mean(latent_s)) / np.std(latent_s, ddof=1)

    # 3. 6 Raw sentiment proxies: CEFD (-), TURN (+), NIPO (+), RIPO (+), S (+), PDND (-)
    proxy_loadings = np.array([-0.65, 0.70, 0.85, 0.75, 0.80, -0.60])
    raw_proxies = np.zeros((n_periods, 6))
    for k in range(6):
        macro_effect = macro @ rng.normal(0.15, 0.05, size=4)
        raw_proxies[:, k] = proxy_loadings[k] * latent_s + macro_effect + rng.normal(0.0, 0.4, size=n_periods)

    # Standardize proxies
    std_proxies = (raw_proxies - np.mean(raw_proxies, axis=0)) / np.std(raw_proxies, axis=0, ddof=1)

    # Orthogonalize against macro controls via OLS
    x_mat = np.column_stack([np.ones(n_periods), macro])
    beta_macro, _, _, _ = np.linalg.lstsq(x_mat, std_proxies, rcond=None)
    ortho_residuals = std_proxies - x_mat @ beta_macro
    ortho_proxies = ortho_residuals / np.std(ortho_residuals, axis=0, ddof=1)

    # Principal Component Analysis
    corr_mat = np.corrcoef(ortho_proxies, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(corr_mat)
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]

    pc1_loadings = eigvecs[:, 0].copy()
    # Sign normalization: NIPO (index 2) must have positive loading
    if pc1_loadings[2] < 0:
        pc1_loadings = -pc1_loadings

    sentiment_index = ortho_proxies @ pc1_loadings
    sentiment_index = (sentiment_index - np.mean(sentiment_index)) / np.std(sentiment_index, ddof=1)
    variance_explained = float(eigvals[0] / np.sum(eigvals))

    # Cross-sectional test: High-Volatility (hard to value) vs Low-Volatility (safe) assets
    # High-volatility assets: strong negative sensitivity to lagged sentiment
    # Low-volatility assets: near zero or slight positive sensitivity
    high_vol_ret = 0.010 - 0.024 * sentiment_index[:-1] + rng.normal(0.0, 0.05, size=n_periods - 1)
    low_vol_ret = 0.007 + 0.002 * sentiment_index[:-1] + rng.normal(0.0, 0.025, size=n_periods - 1)
    spread = high_vol_ret - low_vol_ret
    sent_lag = sentiment_index[:-1]

    # Regress spread on lagged sentiment with HAC standard errors
    x_spread = np.column_stack([np.ones(len(sent_lag)), sent_lag])
    beta_spread, _, _, _ = np.linalg.lstsq(x_spread, spread, rcond=None)
    residuals_spread = spread - x_spread @ beta_spread
    u_x = residuals_spread[:, None] * x_spread
    s_mat = u_x.T @ u_x
    for l_idx in range(1, 3):
        w = 1.0 - l_idx / 3.0
        g = u_x[l_idx:].T @ u_x[:-l_idx]
        s_mat += w * (g + g.T)
    var_beta = np.linalg.inv(x_spread.T @ x_spread) @ s_mat @ np.linalg.inv(x_spread.T @ x_spread)
    se_spread = np.sqrt(np.diag(var_beta))
    t_stat_spread = beta_spread[1] / se_spread[1]

    # Conditional returns in high vs low sentiment regimes
    high_mask = sent_lag > 0
    low_mask = ~high_mask
    mean_spread_high = float(np.mean(spread[high_mask]))
    mean_spread_low = float(np.mean(spread[low_mask]))

    print(f"Leading PC1 variance explained:       {variance_explained * 100:.2f}%")
    print(f"Anchor proxy (NIPO) loading:          {pc1_loadings[2]:+.4f}")
    print(f"Spread predictive slope (beta):       {beta_spread[1]:+.4f}")
    print(f"Newey-West HAC t-statistic:           {t_stat_spread:.2f}")
    print(f"Mean spread post-high sentiment:      {mean_spread_high * 100:.2f}%")
    print(f"Mean spread post-low sentiment:       {mean_spread_low * 100:.2f}%")
    print(f"Regime asymmetry difference (Low-Hi): {(mean_spread_low - mean_spread_high) * 100:.2f}%")


main()
