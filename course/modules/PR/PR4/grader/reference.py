"""Reference implementation for PR4: Atlas A12 Quantitative Risk Engine.

Provides historical, parametric (Gaussian and Student-t), and EVT Peaks-Over-Threshold
Value-at-Risk and Expected Shortfall, Kupiec and Christoffersen backtesting engines,
multivariate stress testing, and Gaussian copula tail metrics.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import scipy.special
import scipy.stats


def historical_var(losses: np.ndarray[Any, Any], alpha: float = 0.99) -> float:
    """Compute empirical Historical Simulation Value-at-Risk at confidence level alpha.

    Parameters
    ----------
    losses : np.ndarray
        1D array of portfolio losses (positive values represent losses).
    alpha : float, default=0.99
        Confidence level in (0, 1).

    Returns
    -------
    float
        Historical VaR estimate.
    """
    arr = np.asarray(losses, dtype=np.float64)
    if arr.ndim != 1 or len(arr) < 5:
        raise ValueError("losses must be a 1D array with at least 5 observations")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1)")
    return float(np.quantile(arr, alpha, method="linear"))


def historical_es(losses: np.ndarray[Any, Any], alpha: float = 0.99) -> float:
    """Compute empirical Historical Simulation Expected Shortfall at confidence level alpha.

    Parameters
    ----------
    losses : np.ndarray
        1D array of portfolio losses.
    alpha : float, default=0.99
        Confidence level in (0, 1).

    Returns
    -------
    float
        Historical ES estimate (mean of losses exceeding VaR).
    """
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
    """Compute parametric Gaussian Value-at-Risk and Expected Shortfall.

    Parameters
    ----------
    losses : np.ndarray
        1D array of portfolio losses.
    alpha : float, default=0.99
        Confidence level in (0, 1).

    Returns
    -------
    tuple[float, float]
        (VaR, ES) under the Gaussian distribution assumption.
    """
    arr = np.asarray(losses, dtype=np.float64)
    if arr.ndim != 1 or len(arr) < 5:
        raise ValueError("losses must be a 1D array with at least 5 observations")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1)")

    mu = float(np.mean(arr))
    sigma = float(np.std(arr, ddof=1))
    z_alpha = float(scipy.stats.norm.ppf(alpha))
    phi_z = float(scipy.stats.norm.pdf(z_alpha))

    var = mu + sigma * z_alpha
    es = mu + sigma * (phi_z / (1.0 - alpha))
    return float(var), float(es)


def parametric_student_t_var_es(
    losses: np.ndarray[Any, Any],
    alpha: float = 0.99,
    df: int = 5,
) -> tuple[float, float]:
    """Compute parametric Student-t Value-at-Risk and Expected Shortfall.

    Parameters
    ----------
    losses : np.ndarray
        1D array of portfolio losses.
    alpha : float, default=0.99
        Confidence level in (0, 1).
    df : int, default=5
        Degrees of freedom (must be strictly greater than 2).

    Returns
    -------
    tuple[float, float]
        (VaR, ES) under the standardized Student-t distribution assumption.
    """
    arr = np.asarray(losses, dtype=np.float64)
    if arr.ndim != 1 or len(arr) < 5:
        raise ValueError("losses must be a 1D array with at least 5 observations")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1)")
    if df <= 2:
        raise ValueError("df must be strictly greater than 2 for finite variance")

    mu = float(np.mean(arr))
    sigma = float(np.std(arr, ddof=1))
    # Scale parameter s matching sample standard deviation sigma
    scale = sigma * math.sqrt((df - 2.0) / df)

    q = float(scipy.stats.t.ppf(alpha, df=df))
    g_q = float(scipy.stats.t.pdf(q, df=df))

    var = mu + scale * q
    # McNeil, Frey & Embrechts (2015) analytic formula (2.27)
    es = mu + scale * ((g_q / (1.0 - alpha)) * ((df + q * q) / (df - 1.0)))
    return float(var), float(es)


def evt_gpd_var_es(
    losses: np.ndarray[Any, Any],
    threshold: float,
    alpha: float = 0.99,
) -> tuple[float, float, float, float]:
    """Compute Extreme Value Theory Peaks-Over-Threshold (POT) VaR and ES using GPD.

    Parameters
    ----------
    losses : np.ndarray
        1D array of portfolio losses.
    threshold : float
        High threshold u above which excesses are modeled.
    alpha : float, default=0.99
        Target extreme tail quantile level.

    Returns
    -------
    tuple[float, float, float, float]
        (VaR_EVT, ES_EVT, xi, beta) where xi is shape and beta is scale.
    """
    arr = np.asarray(losses, dtype=np.float64)
    if arr.ndim != 1 or len(arr) < 10:
        raise ValueError("losses must be a 1D array with at least 10 observations")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1)")

    t_total = len(arr)
    excesses = arr[arr > threshold] - threshold
    n_u = len(excesses)

    if n_u < 5:
        raise ValueError(f"Too few exceedances ({n_u}) above threshold {threshold}")
    if alpha < 1.0 - (n_u / t_total):
        raise ValueError("alpha must exceed 1 - N_u / T for extreme tail extrapolation")

    mean_exc = float(np.mean(excesses))
    var_exc = float(np.var(excesses, ddof=1))
    if var_exc <= 0.0:
        raise ValueError("Variance of excesses must be strictly positive")

    # Method of Moments GPD estimator (Hosking & Wallis 1987)
    ratio = (mean_exc * mean_exc) / var_exc
    xi = 0.5 * (1.0 - ratio)
    # Bound shape parameter xi < 1 for finite expected shortfall
    xi = max(-0.5, min(0.90, xi))
    beta = mean_exc * (1.0 - xi)
    if beta <= 0.0:
        beta = 1e-4

    factor = (t_total / n_u) * (1.0 - alpha)
    if abs(xi) > 1e-6:
        var_evt = threshold + (beta / xi) * (factor ** (-xi) - 1.0)
    else:
        var_evt = threshold - beta * math.log(factor)

    es_evt = (var_evt + beta - xi * threshold) / (1.0 - xi)
    return float(var_evt), float(es_evt), float(xi), float(beta)


def kupiec_pof_test(
    exceptions: int,
    total_obs: int,
    alpha: float = 0.99,
) -> tuple[float, float, bool]:
    """Execute Kupiec Proportion of Failures (POF) Likelihood Ratio test.

    Parameters
    ----------
    exceptions : int
        Number of observed backtest violations (x).
    total_obs : int
        Total number of out-of-sample observations (T).
    alpha : float, default=0.99
        Nominal confidence level.

    Returns
    -------
    tuple[float, float, bool]
        (LR_stat, p_value, reject_null) where reject_null indicates rejection at 5% significance.
    """
    if total_obs <= 0:
        raise ValueError("total_obs must be strictly positive")
    if not (0 <= exceptions <= total_obs):
        raise ValueError("exceptions must be between 0 and total_obs")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must be in (0, 1)")

    p = 1.0 - alpha
    x = exceptions
    t = total_obs

    if x == 0:
        lr = -2.0 * t * math.log(1.0 - p)
    elif x == t:
        lr = -2.0 * t * math.log(p)
    else:
        p_hat = x / t
        lr = -2.0 * (
            (t - x) * math.log(1.0 - p) + x * math.log(p) - (t - x) * math.log(1.0 - p_hat) - x * math.log(p_hat)
        )

    lr = max(0.0, float(lr))
    # Chi-squared survival function with 1 degree of freedom
    p_val = float(math.erfc(math.sqrt(lr / 2.0)))
    reject_null = bool(p_val < 0.05)
    return float(lr), float(p_val), reject_null


def christoffersen_test(
    hits: np.ndarray[Any, Any],
    alpha: float = 0.99,
) -> tuple[float, float, float, float, float, float]:
    """Execute Christoffersen (1998) unconditional, independence, and conditional coverage tests.

    Parameters
    ----------
    hits : np.ndarray
        1D binary sequence of backtest violations (1 for exception, 0 otherwise).
    alpha : float, default=0.99
        Nominal confidence level.

    Returns
    -------
    tuple[float, float, float, float, float, float]
        (lr_uc, p_uc, lr_ind, p_ind, lr_cc, p_cc).
    """
    arr = np.asarray(hits, dtype=np.int64)
    if arr.ndim != 1 or len(arr) < 10:
        raise ValueError("hits must be a 1D binary array with at least 10 entries")
    if not np.all(np.isin(arr, [0, 1])):
        raise ValueError("hits must contain only binary values 0 and 1")

    t = len(arr)
    x = int(np.sum(arr))
    lr_uc, p_uc, _ = kupiec_pof_test(x, t, alpha)

    # Transition counts for first-order Markov chain
    h_prev = arr[:-1]
    h_next = arr[1:]
    n00 = int(np.sum((h_prev == 0) & (h_next == 0)))
    n01 = int(np.sum((h_prev == 0) & (h_next == 1)))
    n10 = int(np.sum((h_prev == 1) & (h_next == 0)))
    n11 = int(np.sum((h_prev == 1) & (h_next == 1)))

    pi01 = n01 / (n00 + n01) if (n00 + n01) > 0 else 0.0
    pi11 = n11 / (n10 + n11) if (n10 + n11) > 0 else 0.0
    pi = (n01 + n11) / (n00 + n01 + n10 + n11) if (n00 + n01 + n10 + n11) > 0 else 0.0

    def safe_log(val: float) -> float:
        return math.log(val) if val > 1e-12 else 0.0

    log_l0 = (n00 + n10) * safe_log(1.0 - pi) + (n01 + n11) * safe_log(pi)
    log_l1 = n00 * safe_log(1.0 - pi01) + n01 * safe_log(pi01) + n10 * safe_log(1.0 - pi11) + n11 * safe_log(pi11)

    lr_ind = max(0.0, -2.0 * (log_l0 - log_l1))
    p_ind = float(math.erfc(math.sqrt(lr_ind / 2.0)))

    lr_cc = lr_uc + lr_ind
    p_cc = float(math.exp(-lr_cc / 2.0))

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
    """Compute portfolio dollar P&L under a prescribed multi-asset stress scenario.

    Parameters
    ----------
    weights : np.ndarray
        1D array of portfolio weights summing to 1.0.
    portfolio_value : float
        Initial base equity value in currency units.
    asset_shocks : np.ndarray
        1D array of fractional asset price shocks.

    Returns
    -------
    float
        Portfolio dollar P&L.
    """
    w = np.asarray(weights, dtype=np.float64)
    s = np.asarray(asset_shocks, dtype=np.float64)
    if w.ndim != 1 or s.ndim != 1 or len(w) != len(s):
        raise ValueError("weights and asset_shocks must be 1D arrays of equal length")
    if portfolio_value <= 0:
        raise ValueError("portfolio_value must be strictly positive")
    return float(portfolio_value * np.sum(w * s))


def gaussian_copula_tail_metrics(
    corr_matrix: np.ndarray[Any, Any],
    threshold: float = 0.95,
    n_sims: int = 100000,
    seed: int = 42,
) -> tuple[float, float]:
    """Simulate from a bivariate Gaussian copula and compute tail co-movement metrics.

    Parameters
    ----------
    corr_matrix : np.ndarray
        2x2 correlation matrix.
    threshold : float, default=0.95
        Upper quantile threshold q in (0, 1).
    n_sims : int, default=100000
        Number of Monte Carlo simulations.
    seed : int, default=42
        RNG seed.

    Returns
    -------
    tuple[float, float]
        (joint_exceedance_prob, empirical_tail_dependence_proxy).
    """
    cov = np.asarray(corr_matrix, dtype=np.float64)
    if cov.shape != (2, 2):
        raise ValueError("corr_matrix must be a 2x2 matrix")
    if not (0.0 < threshold < 1.0):
        raise ValueError("threshold must be in (0, 1)")
    if n_sims < 1000:
        raise ValueError("n_sims must be at least 1000")

    chol = np.linalg.cholesky(cov)
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((n_sims, 2))
    x = z @ chol.T
    # Marginal probability integral transform
    u1 = 0.5 * (1.0 + scipy.special.erf(x[:, 0] / math.sqrt(2.0)))
    u2 = 0.5 * (1.0 + scipy.special.erf(x[:, 1] / math.sqrt(2.0)))
    joint_hits = (u1 > threshold) & (u2 > threshold)
    joint_prob = float(np.mean(joint_hits))
    tail_proxy = float(joint_prob / (1.0 - threshold))
    return joint_prob, tail_proxy
