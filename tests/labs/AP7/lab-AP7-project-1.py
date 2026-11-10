"""Lab AP7-project-1 (Rung 1, Worked Example): Sentiment-Index Extraction & Orthogonalization.

SIMULATED: Fully solved instance of the sentiment index construction pipeline,
standardizing 6 proxies, projecting out 4 macroeconomic series via OLS,
extracting the leading principal component with anchor sign normalization on NIPO,
and computing Newey-West HAC inference on subsequent return spreads.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    seed = 42
    rng = np.random.default_rng(seed)
    n_periods = 180

    # 1. Macroeconomic control matrix (T, 4)
    macro = rng.normal([0.002, 0.0015, 0.015, 0.010], [0.008, 0.006, 0.007, 0.005], size=(n_periods, 4))

    # 2. Latent sentiment state
    phi_sentiment = 0.82
    latent_sentiment = np.zeros(n_periods)
    shocks = rng.normal(0.0, 0.60, size=n_periods)
    for t in range(1, n_periods):
        latent_sentiment[t] = phi_sentiment * latent_sentiment[t - 1] + shocks[t]
    latent_sentiment = (latent_sentiment - np.mean(latent_sentiment)) / np.std(latent_sentiment, ddof=1)

    # 3. 6 Sentiment proxies: CEFD (-), TURN (+), NIPO (+), RIPO (+), S (+), PDND (-)
    proxy_loadings = np.array([-0.65, 0.70, 0.85, 0.75, 0.80, -0.60])
    raw_proxies = np.zeros((n_periods, 6))
    for k in range(6):
        macro_effect = macro @ rng.normal(0.20, 0.10, size=4)
        raw_proxies[:, k] = proxy_loadings[k] * latent_sentiment + macro_effect + rng.normal(0.0, 0.40, size=n_periods)

    # 4. Standardize proxies
    mean_proxies = np.mean(raw_proxies, axis=0)
    std_proxies = np.std(raw_proxies, axis=0, ddof=1)
    proxies_std = (raw_proxies - mean_proxies) / std_proxies

    # 5. Orthogonalize against macro controls via OLS projection
    x_matrix = np.column_stack([np.ones(n_periods), macro])
    beta_macro, _, _, _ = np.linalg.lstsq(x_matrix, proxies_std, rcond=None)
    residuals = proxies_std - x_matrix @ beta_macro
    ortho_proxies = residuals / np.std(residuals, axis=0, ddof=1)

    # 6. Principal Component Analysis on correlation matrix
    corr_matrix = np.corrcoef(ortho_proxies, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(corr_matrix)
    sort_order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sort_order]
    eigenvectors = eigenvectors[:, sort_order]

    # Leading eigenvector with sign anchor on NIPO (index 2)
    pc1_loadings = eigenvectors[:, 0].copy()
    if pc1_loadings[2] < 0:
        pc1_loadings = -pc1_loadings

    raw_sentiment_index = ortho_proxies @ pc1_loadings
    sentiment_index = (raw_sentiment_index - np.mean(raw_sentiment_index)) / np.std(raw_sentiment_index, ddof=1)
    variance_explained = float(eigenvalues[0] / np.sum(eigenvalues))

    # 7. Predictive regression on speculative vs safe portfolio spread
    hard_assets = np.zeros((n_periods, 4))
    easy_assets = np.zeros((n_periods, 4))
    for i in range(4):
        sent_component = np.zeros(n_periods)
        sent_component[1:] = -0.021 * sentiment_index[:-1]
        hard_assets[:, i] = 0.010 + sent_component + rng.normal(0.0, 0.04, size=n_periods)
        easy_assets[:, i] = 0.007 + rng.normal(0.0, 0.02, size=n_periods)

    spread = np.mean(hard_assets[1:, :], axis=1) - np.mean(easy_assets[1:, :], axis=1)
    sent_lag = sentiment_index[:-1]

    x_spread = np.column_stack([np.ones(len(sent_lag)), sent_lag])
    beta_spread, _, _, _ = np.linalg.lstsq(x_spread, spread, rcond=None)
    res_spread = spread - x_spread @ beta_spread

    # Newey-West HAC covariance with 2 lags
    u_x = res_spread[:, None] * x_spread
    s_mat = u_x.T @ u_x
    for l_idx in range(1, 3):
        w = 1.0 - l_idx / 3.0
        g = u_x[l_idx:].T @ u_x[:-l_idx]
        s_mat += w * (g + g.T)
    var_beta = np.linalg.inv(x_spread.T @ x_spread) @ s_mat @ np.linalg.inv(x_spread.T @ x_spread)
    se_spread = np.sqrt(np.diag(var_beta))
    t_stat_spread = beta_spread[1] / se_spread[1]

    # High vs low sentiment regime means
    high_mask = sent_lag > 0
    low_mask = ~high_mask
    mean_high = float(np.mean(spread[high_mask]))
    mean_low = float(np.mean(spread[low_mask]))

    print(f"Sample length (months):               {n_periods}")
    print(f"Number of sentiment proxies:          {raw_proxies.shape[1]}")
    print(f"PC1 variance explained:               {variance_explained * 100:.2f}%")
    print(f"NIPO anchor loading:                  {pc1_loadings[2]:+.4f}")
    print(f"Predictive slope on spread (beta):    {beta_spread[1]:+.4f}")
    print(f"Newey-West HAC standard error:        {se_spread[1]:.4f}")
    print(f"Newey-West HAC t-statistic:           {t_stat_spread:.2f}")
    print(f"Mean spread post-high sentiment:      {mean_high * 100:.2f}%")
    print(f"Mean spread post-low sentiment:       {mean_low * 100:.2f}%")
    print(f"Asymmetry spread difference (Low-Hi): {(mean_low - mean_high) * 100:.2f}%")


main()
