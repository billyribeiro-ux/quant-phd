"""Lab AP7-project-2 (Rung 2, Completion): Sentiment-Index Engine Core.

SIMULATED: Complete reference solution for the Rung 2 completion problem calculating
proxy standardization, macroeconomic orthogonalization, leading principal component
extraction with sign anchor normalization, and Newey-West HAC covariance.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    seed = 42
    rng = np.random.default_rng(seed)
    n_periods = 180

    # Macroeconomic controls and raw proxies
    macro = rng.normal([0.002, 0.0015, 0.015, 0.010], [0.008, 0.006, 0.007, 0.005], size=(n_periods, 4))
    raw_proxies = rng.normal(0.0, 1.0, size=(n_periods, 6))

    # 1. Standardize raw proxies
    mean_vec = np.mean(raw_proxies, axis=0)
    std_vec = np.std(raw_proxies, axis=0, ddof=1)
    proxies_std = (raw_proxies - mean_vec) / std_vec

    # 2. Orthogonalize against macroeconomic controls via OLS projection
    x_mat = np.column_stack([np.ones(n_periods), macro])
    beta_macro, _, _, _ = np.linalg.lstsq(x_mat, proxies_std, rcond=None)
    residuals = proxies_std - x_mat @ beta_macro
    ortho_proxies = residuals / np.std(residuals, axis=0, ddof=1)

    # 3. Principal component extraction on correlation matrix
    corr_mat = np.corrcoef(ortho_proxies, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(corr_mat)
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]

    pc1_weights = eigvecs[:, 0].copy()
    sign_anchor_idx = 2  # NIPO anchor
    if pc1_weights[sign_anchor_idx] < 0:
        pc1_weights = -pc1_weights

    raw_sentiment = ortho_proxies @ pc1_weights
    sentiment_index = (raw_sentiment - np.mean(raw_sentiment)) / np.std(raw_sentiment, ddof=1)
    var_explained = float(eigvals[0] / np.sum(eigvals))

    # 4. Newey-West HAC covariance matrix
    y_test = rng.normal(0.01, 0.04, size=n_periods)
    x_test = np.column_stack([np.ones(n_periods), sentiment_index])
    beta_hat, _, _, _ = np.linalg.lstsq(x_test, y_test, rcond=None)
    u_hat = y_test - x_test @ beta_hat

    xtx_inv = np.linalg.inv(x_test.T @ x_test)
    u_x = u_hat[:, None] * x_test
    s_mat = u_x.T @ u_x
    lags = 3
    for lag in range(1, lags + 1):
        bartlett_w = 1.0 - (lag / (lags + 1.0))
        gamma_l = u_x[lag:].T @ u_x[:-lag]
        s_mat += bartlett_w * (gamma_l + gamma_l.T)
    var_beta = xtx_inv @ s_mat @ xtx_inv
    se_hac = np.sqrt(np.diag(var_beta))

    print(f"Standardized proxy 0 mean:        {float(np.mean(proxies_std[:, 0])):.4f}")
    print(f"Standardized proxy 0 std:         {float(np.std(proxies_std[:, 0], ddof=1)):.4f}")
    max_corr = float(np.max(np.abs(np.corrcoef(ortho_proxies.T, macro.T)[:6, 6:])))
    print(f"Max residual macro correlation:   {max_corr:.2e}")
    print(f"PC1 variance explained:           {var_explained * 100:.2f}%")
    print(f"Anchor proxy weight:              {pc1_weights[sign_anchor_idx]:+.4f}")
    print(f"Sentiment index std:              {float(np.std(sentiment_index, ddof=1)):.4f}")
    print(f"Newey-West HAC standard error:    {se_hac[1]:.4f}")


main()
