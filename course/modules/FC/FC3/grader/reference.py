"""Reference solution for the FC3 project: Fund-skill test.

Implements OLS alpha and t-statistic estimation, naive chance counting,
and cross-sectional bootstrap skill recovery.
"""

from __future__ import annotations

import math
import random


def alpha_and_t(returns: list[float], factor: list[float]) -> tuple[float, float]:
    """Compute OLS alpha (monthly intercept) and its t-statistic.

    Model: returns[t] = alpha + beta * factor[t] + eps[t].

    Parameters
    ----------
    returns : list[float]
        T monthly excess returns of the fund (decimal).
    factor : list[float]
        T monthly excess returns of the benchmark factor (decimal).

    Returns
    -------
    tuple[float, float]
        (alpha, t_stat) where alpha is monthly decimal and t_stat is alpha / se(alpha).

    Raises
    ------
    ValueError
        If lengths differ, T < 3, factor is constant, or residuals are exactly zero.
    """
    if len(returns) != len(factor) or len(returns) < 3:
        raise ValueError("need at least 3 months and equal lengths")

    n_months = len(returns)
    mean_f = sum(factor) / n_months
    mean_r = sum(returns) / n_months

    s_ff = sum((f - mean_f) ** 2 for f in factor)
    if s_ff <= 1e-15:
        raise ValueError("the factor must vary")

    s_fr = sum((factor[t] - mean_f) * (returns[t] - mean_r) for t in range(n_months))
    beta = s_fr / s_ff
    alpha = mean_r - beta * mean_f

    rss = sum((returns[t] - (alpha + beta * factor[t])) ** 2 for t in range(n_months))
    if rss <= 1e-15:
        raise ValueError("residuals are zero; the t-statistic is undefined")

    s2 = rss / (n_months - 2)
    var_a = s2 * (1.0 / n_months + (mean_f**2) / s_ff)
    se_a = math.sqrt(var_a)
    t_stat = alpha / se_a

    return alpha, t_stat


def chance_count(t_stats: list[float], critical: float) -> int:
    """Count the number of funds with t-statistic strictly greater than the critical value.

    Parameters
    ----------
    t_stats : list[float]
        Estimated t-statistics for a universe of funds.
    critical : float
        Critical threshold value.

    Returns
    -------
    int
        Count of funds satisfying t > critical.
    """
    return sum(1 for t in t_stats if t > critical)


def bootstrap_skilled_set(
    returns: list[list[float]],
    factor: list[float],
    level: float,
    n_boot: int,
    seed: int,
) -> list[int]:
    """Identify skilled funds via bootstrap maximum-t threshold.

    Imposes the null of zero alpha by resampling residuals, preserving
    cross-fund dependence via shared month draws, and evaluates the
    ceiling-rank (1 - level) quantile of max-t.

    Parameters
    ----------
    returns : list[list[float]]
        N lists of T monthly excess returns.
    factor : list[float]
        T monthly excess returns of the benchmark factor.
    level : float
        Significance level in (0, 1), e.g., 0.05.
    n_boot : int
        Number of bootstrap replications (>= 1).
    seed : int
        RNG seed for reproducible residual resampling.

    Returns
    -------
    list[int]
        Ascending list of fund indices whose observed t-statistic
        exceeds the bootstrap maximum-t critical threshold.

    Raises
    ------
    ValueError
        If level is outside (0, 1) or n_boot < 1.
    """
    if not (0.0 < level < 1.0):
        raise ValueError("level must lie strictly between 0 and 1")
    if n_boot < 1:
        raise ValueError("n_boot must be at least 1")

    n_funds = len(returns)
    if n_funds == 0:
        return []

    n_months = len(factor)
    mean_f = sum(factor) / n_months
    s_ff = sum((f - mean_f) ** 2 for f in factor)
    if s_ff <= 1e-15:
        raise ValueError("the factor must vary")

    slopes: list[float] = [0.0] * n_funds
    residuals: list[list[float]] = []
    observed_t: list[float] = [0.0] * n_funds

    for i in range(n_funds):
        alpha_i, t_i = alpha_and_t(returns[i], factor)
        mean_r_i = sum(returns[i]) / n_months
        s_fr_i = sum((factor[t] - mean_f) * (returns[i][t] - mean_r_i) for t in range(n_months))
        beta_i = s_fr_i / s_ff
        e_i = [returns[i][t] - (alpha_i + beta_i * factor[t]) for t in range(n_months)]

        slopes[i] = beta_i
        residuals.append(e_i)
        observed_t[i] = t_i

    rng = random.Random(seed)
    max_t_boot: list[float] = [0.0] * n_boot

    for k in range(n_boot):
        tau = [rng.randrange(n_months) for _ in range(n_months)]
        m_k = -1e9
        for i in range(n_funds):
            beta_i = slopes[i]
            e_i = residuals[i]
            # Impose null of zero alpha: r*_it = beta_i * f_t + e_{i, tau_t}
            r_null = [beta_i * factor[t] + e_i[tau[t]] for t in range(n_months)]
            _, t_boot = alpha_and_t(r_null, factor)
            if t_boot > m_k:
                m_k = t_boot
        max_t_boot[k] = m_k

    max_t_boot.sort()
    idx = math.ceil((1.0 - level) * n_boot) - 1
    idx = max(0, min(n_boot - 1, idx))
    threshold = max_t_boot[idx]

    return [i for i in range(n_funds) if observed_t[i] > threshold]
