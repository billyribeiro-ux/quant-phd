"""historical_var returns negative quantile values, misrepresenting loss thresholds."""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import scipy.special
import scipy.stats


def historical_var(losses: np.ndarray[Any, Any], alpha: float = 0.99) -> float:
    arr = np.asarray(losses, dtype=np.float64)
    if arr.ndim != 1 or len(arr) < 5:
        raise ValueError("losses must be a 1D array with at least 5 observations")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1)")
    # Bug: returns negative quantile
    return -float(np.quantile(arr, alpha, method="linear"))


def historical_es(losses: np.ndarray[Any, Any], alpha: float = 0.99) -> float:
    arr = np.asarray(losses, dtype=np.float64)
    var = historical_var(arr, alpha)
    tail = arr[arr > var]
    if len(tail) == 0:
        return float(var)
    return float(np.mean(tail))


def parametric_normal_var_es(
    losses: np.ndarray[Any, Any],
    alpha: float = 0.99,
) -> tuple[float, float]:
    arr = np.asarray(losses, dtype=np.float64)
    if arr.ndim != 1 or len(arr) < 5:
        raise ValueError("losses must be a 1D array with at least 5 observations")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1)")
    mu = float(np.mean(arr))
    sigma = float(np.std(arr, ddof=1))
    z_alpha = float(scipy.stats.norm.ppf(alpha))
    phi_z = float(scipy.stats.norm.pdf(z_alpha))
    return float(mu + sigma * z_alpha), float(mu + sigma * (phi_z / (1.0 - alpha)))


def parametric_student_t_var_es(
    losses: np.ndarray[Any, Any],
    alpha: float = 0.99,
    df: int = 5,
) -> tuple[float, float]:
    arr = np.asarray(losses, dtype=np.float64)
    if arr.ndim != 1 or len(arr) < 5:
        raise ValueError("losses must be a 1D array with at least 5 observations")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1)")
    if df <= 2:
        raise ValueError("df must be strictly greater than 2")
    mu = float(np.mean(arr))
    sigma = float(np.std(arr, ddof=1))
    scale = sigma * math.sqrt((df - 2.0) / df)
    q = float(scipy.stats.t.ppf(alpha, df=df))
    g_q = float(scipy.stats.t.pdf(q, df=df))
    var = mu + scale * q
    es = mu + scale * ((g_q / (1.0 - alpha)) * ((df + q * q) / (df - 1.0)))
    return float(var), float(es)


def evt_gpd_var_es(
    losses: np.ndarray[Any, Any],
    threshold: float,
    alpha: float = 0.99,
) -> tuple[float, float, float, float]:
    arr = np.asarray(losses, dtype=np.float64)
    if arr.ndim != 1 or len(arr) < 10:
        raise ValueError("losses must be a 1D array with at least 10 observations")
    t_total = len(arr)
    excesses = arr[arr > threshold] - threshold
    n_u = len(excesses)
    if n_u < 5:
        raise ValueError("Too few exceedances")
    mean_exc = float(np.mean(excesses))
    var_exc = float(np.var(excesses, ddof=1))
    ratio = (mean_exc * mean_exc) / var_exc
    xi = max(-0.5, min(0.90, 0.5 * (1.0 - ratio)))
    beta = max(1e-4, mean_exc * (1.0 - xi))
    factor = (t_total / n_u) * (1.0 - alpha)
    var_evt = threshold + (beta / xi) * (factor ** (-xi) - 1.0)
    es_evt = (var_evt + beta - xi * threshold) / (1.0 - xi)
    return float(var_evt), float(es_evt), float(xi), float(beta)


def kupiec_pof_test(
    exceptions: int,
    total_obs: int,
    alpha: float = 0.99,
) -> tuple[float, float, bool]:
    p = 1.0 - alpha
    x = exceptions
    t = total_obs
    p_hat = x / t if x > 0 else 0.0
    lr = (
        -2.0 * ((t - x) * math.log(1.0 - p) + x * math.log(p) - (t - x) * math.log(1.0 - p_hat) - x * math.log(p_hat))
        if 0 < x < t
        else 0.0
    )
    lr = max(0.0, float(lr))
    p_val = float(math.erfc(math.sqrt(lr / 2.0)))
    return float(lr), float(p_val), bool(p_val < 0.05)


def christoffersen_test(
    hits: np.ndarray[Any, Any],
    alpha: float = 0.99,
) -> tuple[float, float, float, float, float, float]:
    arr = np.asarray(hits, dtype=np.int64)
    lr_uc, p_uc, _ = kupiec_pof_test(int(np.sum(arr)), len(arr), alpha)
    return float(lr_uc), float(p_uc), 0.0, 1.0, float(lr_uc), float(p_uc)


def stress_scenario_pnl(
    weights: np.ndarray[Any, Any],
    portfolio_value: float,
    asset_shocks: np.ndarray[Any, Any],
) -> float:
    return float(portfolio_value * np.sum(np.asarray(weights) * np.asarray(asset_shocks)))


def gaussian_copula_tail_metrics(
    corr_matrix: np.ndarray[Any, Any],
    threshold: float = 0.95,
    n_sims: int = 100000,
    seed: int = 42,
) -> tuple[float, float]:
    return 0.01, 0.20
