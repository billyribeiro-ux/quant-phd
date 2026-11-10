"""christoffersen_test sets lr_ind to zero, failing to detect volatility clustering in exceptions."""

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
    return float(np.quantile(arr, alpha, method="linear"))


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
    t_total = len(arr)
    excesses = arr[arr > threshold] - threshold
    n_u = len(excesses)
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
    p_hat = x / t
    lr = -2.0 * ((t - x) * math.log(1.0 - p) + x * math.log(p) - (t - x) * math.log(1.0 - p_hat) - x * math.log(p_hat))
    lr = max(0.0, float(lr))
    p_val = float(math.erfc(math.sqrt(lr / 2.0)))
    return float(lr), float(p_val), bool(p_val < 0.05)


def christoffersen_test(
    hits: np.ndarray[Any, Any],
    alpha: float = 0.99,
) -> tuple[float, float, float, float, float, float]:
    arr = np.asarray(hits, dtype=np.int64)
    t = len(arr)
    x = int(np.sum(arr))
    lr_uc, p_uc, _ = kupiec_pof_test(x, t, alpha)
    # Bug: sets lr_ind to 0 and lr_cc to lr_uc
    lr_ind = 0.0
    p_ind = 1.0
    lr_cc = lr_uc
    p_cc = p_uc
    return (
        float(lr_uc),
        float(p_uc),
        float(lr_ind),
        float(p_ind),
        float(lr_cc),
        float(p_cc),
    )


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
    chol = np.linalg.cholesky(np.asarray(corr_matrix, dtype=np.float64))
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((n_sims, 2))
    x = z @ chol.T
    u1 = 0.5 * (1.0 + scipy.special.erf(x[:, 0] / math.sqrt(2.0)))
    u2 = 0.5 * (1.0 + scipy.special.erf(x[:, 1] / math.sqrt(2.0)))
    jp = float(np.mean((u1 > threshold) & (u2 > threshold)))
    return jp, float(jp / (1.0 - threshold))
