"""Reference solution for AP7 Sentiment-Index Replication.

Implements proxy standardization, macroeconomic orthogonalization, first principal
component sentiment index extraction with anchor sign normalization, multi-horizon
predictive regressions with Newey-West HAC inference, and cross-sectional anomaly
asymmetry tests (Baker & Wurgler 2006).
"""

from __future__ import annotations

from typing import Any

import numpy as np


def standardize_proxies(raw_proxies: np.ndarray) -> np.ndarray:
    """Standardize each sentiment proxy column to mean zero and unit variance.

    Parameters
    ----------
    raw_proxies : np.ndarray
        Array of shape (T, K) containing raw proxy time series.

    Returns
    -------
    np.ndarray
        Standardized array of shape (T, K) with sample ddof=1.
    """
    mean = np.mean(raw_proxies, axis=0)
    std = np.std(raw_proxies, axis=0, ddof=1)
    # Guard against zero variance
    std_safe = np.where(std > 1e-12, std, 1.0)
    return np.asarray((raw_proxies - mean) / std_safe)


def orthogonalize_proxies(proxies_std: np.ndarray, macro_controls: np.ndarray) -> np.ndarray:
    """Orthogonalize standardized proxies with respect to macroeconomic control variables.

    For each proxy k, estimates:
        proxy_{k, t} = c_k + beta_k' macro_t + u_{k, t}
    and extracts the standardized residual series u_{k, t} / std(u_k).

    Parameters
    ----------
    proxies_std : np.ndarray
        Standardized proxy matrix of shape (T, K).
    macro_controls : np.ndarray
        Macroeconomic variable matrix of shape (T, M).

    Returns
    -------
    np.ndarray
        Orthogonalized and standardized residual proxy matrix of shape (T, K).
    """
    n_periods = proxies_std.shape[0]
    x_matrix = np.column_stack([np.ones(n_periods), macro_controls])
    beta_macro, _, _, _ = np.linalg.lstsq(x_matrix, proxies_std, rcond=None)
    residuals = proxies_std - x_matrix @ beta_macro
    res_stds = np.std(residuals, axis=0, ddof=1)
    res_stds_safe = np.where(res_stds > 1e-12, res_stds, 1.0)
    return np.asarray(residuals / res_stds_safe)


def extract_sentiment_index(ortho_proxies: np.ndarray, sign_anchor_idx: int = 2) -> dict[str, Any]:
    """Extract first principal component sentiment index with sign anchor normalization.

    Calculates the correlation matrix of orthogonalized proxies, finds the leading
    eigenvector, normalizes the sign so that loading on sign_anchor_idx is positive,
    and returns the standardized sentiment index series.

    Parameters
    ----------
    ortho_proxies : np.ndarray
        Orthogonalized proxy matrix of shape (T, K).
    sign_anchor_idx : int
        Column index of the anchor proxy that must enter with positive sign.

    Returns
    -------
    dict[str, Any]
        - index: standardized 1D array of shape (T,)
        - loadings: 1D array of shape (K,) with anchor loading > 0
        - var_explained: proportion of total proxy variance explained by PC1
        - eigenvalues: 1D array of descending eigenvalues
    """
    corr_matrix = np.corrcoef(ortho_proxies, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(corr_matrix)

    # Sort descending
    sort_order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sort_order]
    eigenvectors = eigenvectors[:, sort_order]

    leading_loading = eigenvectors[:, 0].copy()

    # Sign normalization: anchor loading must be strictly positive
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
    """Compute OLS coefficients and Newey-West (1987) HAC standard errors.

    Estimates:
        y = X beta + u
        Var(beta) = (X'X)^-1 S_T (X'X)^-1
        S_T = Gamma_0 + sum_{l=1}^L w_l (Gamma_l + Gamma_l')
    with Bartlett triangular kernel weights w_l = 1 - l / (L + 1).

    Parameters
    ----------
    x_matrix : np.ndarray
        Design matrix of shape (T, K).
    y_vector : np.ndarray
        Response vector of shape (T,).
    lags : int
        Number of autocorrelation lags L.

    Returns
    -------
    dict[str, Any]
        - beta: 1D array of shape (K,)
        - se: 1D array of HAC standard errors of shape (K,)
        - t_stats: 1D array of t-statistics of shape (K,)
        - residuals: 1D array of residuals of shape (T,)
        - r2: OLS coefficient of determination R^2
    """
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

    return {
        "beta": beta,
        "se": se,
        "t_stats": t_stats,
        "residuals": residuals,
        "r2": float(r2),
    }


def estimate_predictive_regression(
    returns: np.ndarray, sentiment: np.ndarray, horizon: int = 1, lags: int = 1
) -> dict[str, Any]:
    """Estimate multi-period predictive regression of returns on lagged sentiment.

    Estimates:
        R_{t+1:t+h} = alpha + beta * sentiment_t + u_{t+h}
    where R_{t+1:t+h} = sum_{k=1}^h returns_{t+k}.

    Parameters
    ----------
    returns : np.ndarray
        1D array of monthly returns of length T.
    sentiment : np.ndarray
        1D array of standardized sentiment index of length T.
    horizon : int
        Forecasting horizon h in months.
    lags : int
        HAC lag truncation parameter (recommended: at least horizon).

    Returns
    -------
    dict[str, Any]
        Regression summary with beta, alpha, se_hac, t_stat, and r2.
    """
    n_periods = len(returns)
    valid_length = n_periods - horizon
    if valid_length <= 0:
        raise ValueError(f"Sample length {n_periods} insufficient for horizon {horizon}")

    # Cumulative forward returns
    forward_cum_ret = np.zeros(valid_length)
    for t in range(valid_length):
        forward_cum_ret[t] = np.sum(returns[t + 1 : t + 1 + horizon])

    sent_predictor = sentiment[:valid_length]
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
    """Test Baker & Wurgler (2006) cross-sectional sentiment asymmetry hypothesis.

    Tests whether the long-short return spread between speculative (hard-to-value,
    columns 0-3) and safe (easy-to-value, columns 4-7) portfolios is negatively
    predicted by lagged investor sentiment, and compares conditional means across
    high-sentiment (SENT > 0) and low-sentiment (SENT <= 0) regimes.

    Parameters
    ----------
    test_assets_returns : np.ndarray
        Matrix of asset returns of shape (T, 8).
    sentiment : np.ndarray
        Standardized sentiment index of shape (T,).

    Returns
    -------
    dict[str, Any]
        Summary containing:
        - spread: 1D array of monthly long-short spread returns
        - beta_spread: OLS predictive slope on lagged sentiment (must be negative)
        - t_stat_spread: Newey-West HAC t-statistic
        - mean_spread_high: average spread return following high sentiment
        - mean_spread_low: average spread return following low sentiment
        - asymmetry_diff: mean_spread_low - mean_spread_high (must be positive)
        - r2: predictive regression R^2
    """
    # Forward 1-month returns
    sent_lag = sentiment[:-1]
    hard_to_value_ret = np.mean(test_assets_returns[1:, :4], axis=1)
    easy_to_value_ret = np.mean(test_assets_returns[1:, 4:], axis=1)
    spread = hard_to_value_ret - easy_to_value_ret

    high_sentiment_mask = sent_lag > 0.0
    low_sentiment_mask = ~high_sentiment_mask

    mean_spread_high = float(np.mean(spread[high_sentiment_mask])) if np.any(high_sentiment_mask) else 0.0
    mean_spread_low = float(np.mean(spread[low_sentiment_mask])) if np.any(low_sentiment_mask) else 0.0
    asymmetry_diff = mean_spread_low - mean_spread_high

    x_matrix = np.column_stack([np.ones(len(sent_lag)), sent_lag])
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
