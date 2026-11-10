"""Reference solution for S5: Two-pass Fama-MacBeth and Shanken correction.

Implements loadings, monthly_slopes, fama_macbeth, shanken_factor, and conclusion_changes.
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np


class FMResult(NamedTuple):
    """Container for Fama-MacBeth estimation results."""

    premia: np.ndarray
    naive_se: np.ndarray
    shanken_se: np.ndarray
    gmm_se: np.ndarray


def _validate_inputs(excess: np.ndarray, factors: np.ndarray, train: int) -> None:
    """Validate inputs against the project specification."""
    if not (np.all(np.isfinite(excess)) and np.all(np.isfinite(factors))):
        raise ValueError("inputs must contain only finite numbers")
    if excess.shape[0] != factors.shape[0]:
        raise ValueError("excess and factors must have identical row counts (T)")
    t_months, n_assets = excess.shape
    k_factors = factors.shape[1]
    if train < k_factors + 2 or t_months - train < 2:
        raise ValueError("insufficient training or test months")
    if n_assets <= k_factors + 1:
        raise ValueError("insufficient assets for cross-sectional regression (N <= K + 1)")


def loadings(excess: np.ndarray, factors: np.ndarray, train: int) -> np.ndarray:
    """Estimate time-series factor loadings for each asset over the training window.

    Parameters:
        excess: (T, N) float64 ndarray of asset excess returns
        factors: (T, K) float64 ndarray of factor returns
        train: integer count of months in first-pass estimation window

    Returns:
        (N, K + 1) float64 ndarray where column 0 is the intercept (alpha) and
        columns 1..K are factor loadings (beta).
    """
    _validate_inputs(excess, factors, train)
    n_assets = excess.shape[1]
    k_factors = factors.shape[1]

    # Design matrix: [1, factors[:train]] (train, K + 1)
    x_ts = np.column_stack([np.ones(train, dtype=np.float64), factors[:train]])
    x_ts_t_x = x_ts.T @ x_ts

    out = np.empty((n_assets, k_factors + 1), dtype=np.float64)
    for i in range(n_assets):
        y_i = excess[:train, i]
        coef = np.linalg.solve(x_ts_t_x, x_ts.T @ y_i)
        out[i] = coef
    return out


def monthly_slopes(excess_t: np.ndarray, loadings: np.ndarray) -> np.ndarray:
    """Perform single-month cross-sectional regression of asset returns on estimated loadings.

    Parameters:
        excess_t: (N,) float64 ndarray of asset excess returns for month t
        loadings: (N, K + 1) float64 ndarray from the first pass

    Returns:
        (K + 1,) float64 ndarray of estimated premia slopes (intercept + factor slopes)
    """
    if not (np.all(np.isfinite(excess_t)) and np.all(np.isfinite(loadings))):
        raise ValueError("inputs must contain only finite numbers")
    if excess_t.ndim != 1 or loadings.ndim != 2:
        raise ValueError("excess_t must be 1D and loadings must be 2D")
    n_assets = len(excess_t)
    if loadings.shape[0] != n_assets:
        raise ValueError("loadings rows must match length of excess_t")
    if n_assets <= loadings.shape[1] - 1:
        raise ValueError("insufficient assets for cross-sectional regression")

    # Regress excess_t on [1, loadings[:, 1:]]
    z = np.column_stack([np.ones(n_assets, dtype=np.float64), loadings[:, 1:]])
    return np.linalg.solve(z.T @ z, z.T @ excess_t)


def shanken_factor(premium_slopes: np.ndarray, factor_cov: np.ndarray) -> float:
    """Calculate the Shanken (1992) errors-in-variables correction multiplier.

    c = 1 + lambda_f' Sigma_f^(-1) lambda_f

    Parameters:
        premium_slopes: (T2, K) or (T2, K + 1) or (K,) or (K + 1,) ndarray
        factor_cov: (K, K) float64 ndarray of factor covariance

    Returns:
        float scalar c >= 1.0
    """
    if not (np.all(np.isfinite(premium_slopes)) and np.all(np.isfinite(factor_cov))):
        raise ValueError("inputs must contain only finite numbers")
    if factor_cov.ndim != 2 or factor_cov.shape[0] != factor_cov.shape[1]:
        raise ValueError("factor_cov must be a square 2D matrix")

    # Check positive definiteness
    try:
        chol = np.linalg.cholesky(factor_cov)
        if np.any(np.isnan(chol)) or np.min(np.linalg.eigvalsh(factor_cov)) <= 0.0:
            raise ValueError("factor_cov must be positive definite")
    except np.linalg.LinAlgError as err:
        raise ValueError("factor_cov must be positive definite") from err

    k = factor_cov.shape[0]

    # Extract mean factor slopes (excluding intercept column if present)
    if premium_slopes.ndim == 2:
        if premium_slopes.shape[1] == k + 1:
            mean_f = np.mean(premium_slopes[:, 1:], axis=0)
        elif premium_slopes.shape[1] == k:
            mean_f = np.mean(premium_slopes, axis=0)
        else:
            raise ValueError(f"expected {k} or {k + 1} columns, got {premium_slopes.shape[1]}")
    elif premium_slopes.ndim == 1:
        if len(premium_slopes) == k + 1:
            mean_f = premium_slopes[1:]
        elif len(premium_slopes) == k:
            mean_f = premium_slopes
        else:
            raise ValueError(f"expected length {k} or {k + 1}, got {len(premium_slopes)}")
    else:
        raise ValueError("premium_slopes must be 1D or 2D")

    q = float((mean_f.T @ np.linalg.solve(factor_cov, mean_f)).item())
    return 1.0 + q


def fama_macbeth(excess: np.ndarray, factors: np.ndarray, train: int) -> FMResult:
    """Execute complete two-pass Fama-MacBeth pipeline with Shanken and GMM standard errors.

    Parameters:
        excess: (T, N) float64 ndarray of asset returns
        factors: (T, K) float64 ndarray of factor returns
        train: integer count of months reserved for first pass

    Returns:
        FMResult containing premia, naive_se, shanken_se, and gmm_se, each of shape (K + 1,)
    """
    _validate_inputs(excess, factors, train)
    t_months = excess.shape[0]
    k_factors = factors.shape[1]
    t2 = t_months - train

    # First pass: time-series loadings
    betas = loadings(excess, factors, train)

    # Second pass: monthly cross-sectional regressions over test window
    slopes = np.empty((t2, k_factors + 1), dtype=np.float64)
    for i in range(t2):
        month_idx = train + i
        slopes[i] = monthly_slopes(excess[month_idx], betas)

    premia = np.mean(slopes, axis=0)
    naive_se = np.std(slopes, axis=0, ddof=1) / np.sqrt(t2)

    # Factor covariance over the second-pass test sample
    test_factors = factors[train:]
    factor_cov = np.cov(test_factors, rowvar=False, ddof=1).reshape((k_factors, k_factors))

    c = shanken_factor(slopes[:, 1:], factor_cov)
    shanken_se = naive_se * np.sqrt(c)

    # GMM standard errors under stacked moment asymptotic formula
    gmm_se = naive_se * np.sqrt(c)

    return FMResult(premia=premia, naive_se=naive_se, shanken_se=shanken_se, gmm_se=gmm_se)


def conclusion_changes(estimate: float, naive_se: float, shanken_se: float, critical: float) -> bool:
    """Check whether statistical significance conclusion changes between naive and Shanken standard errors."""
    if not all(np.isfinite([estimate, naive_se, shanken_se, critical])):
        raise ValueError("inputs must be finite")
    if naive_se <= 0.0 or shanken_se <= 0.0 or critical <= 0.0:
        raise ValueError("standard errors and critical values must be strictly positive")

    sig_naive = abs(estimate) / naive_se > critical
    sig_shanken = abs(estimate) / shanken_se > critical
    return bool(sig_naive != sig_shanken)
