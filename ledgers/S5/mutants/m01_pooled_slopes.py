"""Pools all test months into one pooled OLS regression and reports pooled standard errors.

Student mutant m01 for S5.
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
    _validate_inputs(excess, factors, train)
    n_assets = excess.shape[1]
    k_factors = factors.shape[1]
    x_ts = np.column_stack([np.ones(train, dtype=np.float64), factors[:train]])
    x_ts_t_x = x_ts.T @ x_ts
    out = np.empty((n_assets, k_factors + 1), dtype=np.float64)
    for i in range(n_assets):
        y_i = excess[:train, i]
        out[i] = np.linalg.solve(x_ts_t_x, x_ts.T @ y_i)
    return out


def monthly_slopes(excess_t: np.ndarray, loadings: np.ndarray) -> np.ndarray:
    if not (np.all(np.isfinite(excess_t)) and np.all(np.isfinite(loadings))):
        raise ValueError("inputs must contain only finite numbers")
    if excess_t.ndim != 1 or loadings.ndim != 2:
        raise ValueError("excess_t must be 1D and loadings must be 2D")
    n_assets = len(excess_t)
    if loadings.shape[0] != n_assets:
        raise ValueError("loadings rows must match length of excess_t")
    if n_assets <= loadings.shape[1] - 1:
        raise ValueError("insufficient assets for cross-sectional regression")
    z = np.column_stack([np.ones(n_assets, dtype=np.float64), loadings[:, 1:]])
    return np.linalg.solve(z.T @ z, z.T @ excess_t)


def shanken_factor(premium_slopes: np.ndarray, factor_cov: np.ndarray) -> float:
    if not (np.all(np.isfinite(premium_slopes)) and np.all(np.isfinite(factor_cov))):
        raise ValueError("inputs must contain only finite numbers")
    if factor_cov.ndim != 2 or factor_cov.shape[0] != factor_cov.shape[1]:
        raise ValueError("factor_cov must be a square 2D matrix")
    try:
        np.linalg.cholesky(factor_cov)
    except np.linalg.LinAlgError as err:
        raise ValueError("factor_cov must be positive definite") from err
    k = factor_cov.shape[0]
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
    _validate_inputs(excess, factors, train)
    t_months = excess.shape[0]
    n_assets = excess.shape[1]
    k_factors = factors.shape[1]
    t2 = t_months - train

    betas = loadings(excess, factors, train)

    # BUG m01: Pools all test months and reports pooled OLS standard errors
    z_single = np.column_stack([np.ones(n_assets, dtype=np.float64), betas[:, 1:]])
    z_stacked = np.tile(z_single, (t2, 1))
    y_stacked = excess[train:].ravel()
    inv_ztz = np.linalg.inv(z_stacked.T @ z_stacked)
    pooled_premia = inv_ztz @ (z_stacked.T @ y_stacked)

    # Pooled standard error instead of time-series standard error of monthly slopes
    resid_stacked = y_stacked - z_stacked @ pooled_premia
    s2 = np.sum(resid_stacked**2) / (len(y_stacked) - (k_factors + 1))
    pooled_se = np.sqrt(np.diag(s2 * inv_ztz))

    test_factors = factors[train:]
    factor_cov = np.cov(test_factors, rowvar=False, ddof=1).reshape((k_factors, k_factors))
    c = shanken_factor(pooled_premia[1:], factor_cov)
    shanken_se = pooled_se * np.sqrt(c)
    gmm_se = pooled_se * np.sqrt(c)
    return FMResult(premia=pooled_premia, naive_se=pooled_se, shanken_se=shanken_se, gmm_se=gmm_se)


def conclusion_changes(estimate: float, naive_se: float, shanken_se: float, critical: float) -> bool:
    if not all(np.isfinite([estimate, naive_se, shanken_se, critical])):
        raise ValueError("inputs must be finite")
    if naive_se <= 0.0 or shanken_se <= 0.0 or critical <= 0.0:
        raise ValueError("standard errors and critical values must be strictly positive")
    sig_naive = abs(estimate) / naive_se > critical
    sig_shanken = abs(estimate) / shanken_se > critical
    return bool(sig_naive != sig_shanken)
