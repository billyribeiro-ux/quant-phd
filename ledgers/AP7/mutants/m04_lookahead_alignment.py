"""Mutant m04: Aligns sentiment contemporaneously instead of using strict predictive lags."""

from __future__ import annotations

from typing import Any

import numpy as np


def standardize_proxies(raw_proxies: np.ndarray) -> np.ndarray:
    mean = np.mean(raw_proxies, axis=0)
    std = np.std(raw_proxies, axis=0, ddof=1)
    std_safe = np.where(std > 1e-12, std, 1.0)
    return np.asarray((raw_proxies - mean) / std_safe)


def orthogonalize_proxies(proxies_std: np.ndarray, macro_controls: np.ndarray) -> np.ndarray:
    n_periods = proxies_std.shape[0]
    x_matrix = np.column_stack([np.ones(n_periods), macro_controls])
    beta_macro, _, _, _ = np.linalg.lstsq(x_matrix, proxies_std, rcond=None)
    residuals = proxies_std - x_matrix @ beta_macro
    res_stds = np.std(residuals, axis=0, ddof=1)
    res_stds_safe = np.where(res_stds > 1e-12, res_stds, 1.0)
    return np.asarray(residuals / res_stds_safe)


def extract_sentiment_index(ortho_proxies: np.ndarray, sign_anchor_idx: int = 2) -> dict[str, Any]:
    corr_matrix = np.corrcoef(ortho_proxies, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(corr_matrix)
    sort_order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sort_order]
    eigenvectors = eigenvectors[:, sort_order]
    leading_loading = eigenvectors[:, 0].copy()
    if leading_loading[sign_anchor_idx] < 0:
        leading_loading = -leading_loading
    raw_index = ortho_proxies @ leading_loading
    std_index = (raw_index - np.mean(raw_index)) / np.std(raw_index, ddof=1)
    variance_explained = float(eigenvalues[0] / np.sum(eigenvalues))
    return {
        "index": std_index,
        "loadings": leading_loading,
        "var_explained": variance_explained,
        "eigenvalues": eigenvalues,
    }


def newey_west_hac(x_matrix: np.ndarray, y_vector: np.ndarray, lags: int = 3) -> dict[str, Any]:
    beta, _, _, _ = np.linalg.lstsq(x_matrix, y_vector, rcond=None)
    residuals = y_vector - x_matrix @ beta
    xtx_inv = np.linalg.inv(x_matrix.T @ x_matrix)
    u_x = residuals[:, None] * x_matrix
    s_matrix = u_x.T @ u_x
    for lag in range(1, lags + 1):
        bartlett_weight = 1.0 - (lag / (lags + 1.0))
        gamma_lag = u_x[lag:].T @ u_x[:-lag]
        s_matrix += bartlett_weight * (gamma_lag + gamma_lag.T)
    var_beta = xtx_inv @ s_matrix @ xtx_inv
    se = np.sqrt(np.maximum(0.0, np.diag(var_beta)))
    t_stats = beta / np.where(se > 1e-12, se, 1e-12)
    total_ss = np.sum((y_vector - np.mean(y_vector)) ** 2)
    residual_ss = np.sum(residuals**2)
    r2 = 1.0 - (residual_ss / total_ss) if total_ss > 1e-12 else 0.0
    return {"beta": beta, "se": se, "t_stats": t_stats, "residuals": residuals, "r2": float(r2)}


def estimate_predictive_regression(
    returns: np.ndarray, sentiment: np.ndarray, horizon: int = 1, lags: int = 1
) -> dict[str, Any]:
    n_periods = len(returns)
    valid_length = n_periods - horizon
    forward_cum_ret = np.zeros(valid_length)
    for t in range(valid_length):
        forward_cum_ret[t] = np.sum(returns[t + 1 : t + 1 + horizon])
    # BUG: Aligns contemporaneously (or forward) instead of lagged
    sent_predictor = sentiment[1 : valid_length + 1]
    x_matrix = np.column_stack([np.ones(valid_length), sent_predictor])
    hac_result = newey_west_hac(x_matrix, forward_cum_ret, lags=lags)
    return {
        "alpha": float(hac_result["beta"][0]),
        "beta": float(hac_result["beta"][1]),
        "se_hac": float(hac_result["se"][1]),
        "t_stat": float(hac_result["t_stats"][1]),
        "r2": float(hac_result["r2"]),
    }


def test_cross_sectional_asymmetry(test_assets_returns: np.ndarray, sentiment: np.ndarray) -> dict[str, Any]:
    # BUG: Aligns sentiment contemporaneously (lookahead / contemporaneous alignment)
    sent_contemporaneous = sentiment[1:]
    hard_to_value_ret = np.mean(test_assets_returns[1:, :4], axis=1)
    easy_to_value_ret = np.mean(test_assets_returns[1:, 4:], axis=1)
    spread = hard_to_value_ret - easy_to_value_ret
    high_sentiment_mask = sent_contemporaneous > 0.0
    low_sentiment_mask = ~high_sentiment_mask
    mean_spread_high = float(np.mean(spread[high_sentiment_mask])) if np.any(high_sentiment_mask) else 0.0
    mean_spread_low = float(np.mean(spread[low_sentiment_mask])) if np.any(low_sentiment_mask) else 0.0
    asymmetry_diff = mean_spread_low - mean_spread_high
    x_matrix = np.column_stack([np.ones(len(sent_contemporaneous)), sent_contemporaneous])
    nw_res = newey_west_hac(x_matrix, spread, lags=2)
    return {
        "spread": spread,
        "beta_spread": float(nw_res["beta"][1]),
        "t_stat_spread": float(nw_res["t_stats"][1]),
        "mean_spread_high": mean_spread_high,
        "mean_spread_low": mean_spread_low,
        "asymmetry_diff": asymmetry_diff,
        "r2": float(nw_res["r2"]),
    }
