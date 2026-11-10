"""Lab AP7-project-3 (Rung 3, Baseline): Full Sentiment Engine Verification.

SIMULATED: Runs the complete reference sentiment extraction, Newey-West HAC inference,
and cross-sectional anomaly regime asymmetry pipeline on seed 42.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    seed = 42
    rng = np.random.default_rng(seed)
    n_periods = 180

    # 1. Macroeconomic controls (T, 4)
    macro = rng.normal([0.002, 0.0015, 0.015, 0.010], [0.008, 0.006, 0.007, 0.005], size=(n_periods, 4))

    # 2. Latent sentiment AR(1) state
    phi_s = 0.82
    latent_s = np.zeros(n_periods)
    shocks = rng.normal(0.0, 0.60, size=n_periods)
    for t in range(1, n_periods):
        latent_s[t] = phi_s * latent_s[t - 1] + shocks[t]
    latent_s = (latent_s - np.mean(latent_s)) / np.std(latent_s, ddof=1)

    # 3. 6 Sentiment proxies
    proxy_loadings = np.array([-0.65, 0.70, 0.85, 0.75, 0.80, -0.60])
    raw_proxies = np.zeros((n_periods, 6))
    for k in range(6):
        macro_effect = macro @ rng.normal(0.20, 0.10, size=4)
        raw_proxies[:, k] = proxy_loadings[k] * latent_s + macro_effect + rng.normal(0.0, 0.40, size=n_periods)

    # Standardize proxies
    mean_prox = np.mean(raw_proxies, axis=0)
    std_prox = np.std(raw_proxies, axis=0, ddof=1)
    proxies_std = (raw_proxies - mean_prox) / std_prox

    # Orthogonalize against macro controls
    x_macro = np.column_stack([np.ones(n_periods), macro])
    beta_macro, _, _, _ = np.linalg.lstsq(x_macro, proxies_std, rcond=None)
    residuals = proxies_std - x_macro @ beta_macro
    ortho_proxies = residuals / np.std(residuals, axis=0, ddof=1)

    # Leading PC extraction with NIPO anchor (idx 2)
    corr_mat = np.corrcoef(ortho_proxies, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(corr_mat)
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]

    pc1_loadings = eigvecs[:, 0].copy()
    if pc1_loadings[2] < 0:
        pc1_loadings = -pc1_loadings

    raw_sentiment = ortho_proxies @ pc1_loadings
    sentiment_index = (raw_sentiment - np.mean(raw_sentiment)) / np.std(raw_sentiment, ddof=1)
    var_explained = float(eigvals[0] / np.sum(eigvals))

    # Cross-sectional asymmetry test
    sent_lag = sentiment_index[:-1]
    hard_assets = np.zeros((n_periods - 1, 4))
    easy_assets = np.zeros((n_periods - 1, 4))
    for i in range(4):
        hard_assets[:, i] = 0.010 - 0.021 * sent_lag + rng.normal(0.0, 0.04, size=n_periods - 1)
        easy_assets[:, i] = 0.007 + 0.002 * sent_lag + rng.normal(0.0, 0.02, size=n_periods - 1)

    spread = np.mean(hard_assets, axis=1) - np.mean(easy_assets, axis=1)
    x_spread = np.column_stack([np.ones(len(sent_lag)), sent_lag])
    beta_spread, _, _, _ = np.linalg.lstsq(x_spread, spread, rcond=None)
    res_spread = spread - x_spread @ beta_spread

    # Newey-West HAC
    u_x = res_spread[:, None] * x_spread
    s_mat = u_x.T @ u_x
    for l_idx in range(1, 3):
        w = 1.0 - l_idx / 3.0
        g = u_x[l_idx:].T @ u_x[:-l_idx]
        s_mat += w * (g + g.T)
    var_beta = np.linalg.inv(x_spread.T @ x_spread) @ s_mat @ np.linalg.inv(x_spread.T @ x_spread)
    se_spread = np.sqrt(np.diag(var_beta))
    t_stat_spread = beta_spread[1] / se_spread[1]

    high_mask = sent_lag > 0
    low_mask = ~high_mask
    mean_high = float(np.mean(spread[high_mask]))
    mean_low = float(np.mean(spread[low_mask]))
    asymmetry_diff = mean_low - mean_high

    print(f"Random seed:                          {seed}")
    print(f"Sample length (T):                    {len(sentiment_index)}")
    print(f"Leading PC1 variance explained:       {var_explained * 100:.2f}%")
    print(f"Anchor proxy (NIPO) loading:          {pc1_loadings[2]:+.4f}")
    print(f"Spread predictive slope (beta):       {beta_spread[1]:+.4f}")
    print(f"Newey-West HAC t-statistic:           {t_stat_spread:.2f}")
    print(f"Mean spread post-high sentiment:      {mean_high * 100:.2f}%")
    print(f"Mean spread post-low sentiment:       {mean_low * 100:.2f}%")
    print(f"Regime asymmetry difference (Low-Hi): {asymmetry_diff * 100:.2f}%")
    print(f"Hypothesis confirmed (beta < 0):      {bool(beta_spread[1] < 0)}")


main()
