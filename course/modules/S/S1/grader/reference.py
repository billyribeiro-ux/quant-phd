"""Reference implementation for module S1 project: Power analysis for a strategy.

Computes the sample Sharpe ratio, analytic required years, required periods,
and simulated statistical power for a one-sided test of a strategy's Sharpe ratio.
All inputs and simulations are SIMULATED.
"""

from __future__ import annotations

import math
import random
import statistics


def sharpe_hat(returns: list[float]) -> float:
    """Compute the per-period sample Sharpe ratio.

    Uses the sample mean divided by the sample standard deviation with divisor n - 1.

    Args:
        returns: list of per-period returns.

    Returns:
        Per-period sample Sharpe ratio as float.

    Raises:
        ValueError: If len(returns) < 2 or the sample standard deviation is zero.
    """
    n = len(returns)
    if n < 2:
        raise ValueError("fewer than two returns provided")

    mean = math.fsum(returns) / n
    var = math.fsum((r - mean) ** 2 for r in returns) / (n - 1)
    if var <= 0.0:
        raise ValueError("sample standard deviation is zero")

    return mean / math.sqrt(var)


def analytic_years(sr_ann: float, periods_per_year: int, alpha: float, power: float) -> float:
    """Compute the analytic number of years required to achieve a target power.

    Uses the normal asymptotic distribution of the sample Sharpe ratio under i.i.d. returns,
    accounting for the alternative variance inflation factor 1 + SR^2 / 2:
        y = (Phi^{-1}(1 - alpha) + Phi^{-1}(power) * sqrt(1 + sr_ann^2 / (2 * k)))^2 / sr_ann^2

    Args:
        sr_ann: True annualized Sharpe ratio (> 0).
        periods_per_year: Observations per year (k >= 1).
        alpha: One-sided significance level in (0, 1).
        power: Target statistical power (1 - beta) in (0, 1).

    Returns:
        Required years of data as float.

    Raises:
        ValueError: If sr_ann <= 0, periods_per_year < 1, alpha not in (0, 1),
            or power not in (0, 1).
    """
    if sr_ann <= 0.0:
        raise ValueError("sr_ann must be strictly positive")
    if periods_per_year < 1:
        raise ValueError("periods_per_year must be at least 1")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must lie strictly in (0, 1)")
    if not (0.0 < power < 1.0):
        raise ValueError("power must lie strictly in (0, 1)")

    dist = statistics.NormalDist()
    z_alpha = dist.inv_cdf(1.0 - alpha)
    z_power = dist.inv_cdf(power)

    # Alternative variance inflation factor for per-period Sharpe ratio: 1 + SR_per_period^2 / 2
    # Since SR_per_period = sr_ann / sqrt(k), SR_per_period^2 = sr_ann^2 / k.
    inflation = math.sqrt(1.0 + (sr_ann**2) / (2.0 * periods_per_year))

    numerator = (z_alpha + z_power * inflation) ** 2
    return numerator / (sr_ann**2)


def required_periods(sr_ann: float, periods_per_year: int, alpha: float, power: float) -> int:
    """Compute the minimum integer number of periods needed to achieve the target power.

    Defined as the ceiling of analytic_years(...) * periods_per_year.

    Args:
        sr_ann: True annualized Sharpe ratio (> 0).
        periods_per_year: Observations per year (k >= 1).
        alpha: One-sided significance level in (0, 1).
        power: Target statistical power in (0, 1).

    Returns:
        Smallest integer number of periods as int.
    """
    years = analytic_years(sr_ann, periods_per_year, alpha, power)
    return math.ceil(years * periods_per_year)


def simulated_power(periods: int, sr_per_period: float, alpha: float, n_sims: int, seed: int) -> float:
    """Estimate the statistical power of the one-sided test by Monte Carlo simulation.

    Simulates n_sims independent samples of length `periods` from Normal(sr_per_period, 1.0).
    For each sample, computes the sample Sharpe ratio hSR with divisor periods - 1,
    and rejects the null H0: SR = 0 if sqrt(periods) * hSR >= Phi^{-1}(1 - alpha).

    Args:
        periods: Number of return observations per simulation (T >= 2).
        sr_per_period: Population per-period Sharpe ratio.
        alpha: One-sided significance level in (0, 1).
        n_sims: Number of Monte Carlo replications (n_sims >= 1).
        seed: Random seed for reproducibility.

    Returns:
        Rejection rate over n_sims replications as float.

    Raises:
        ValueError: If periods < 2, n_sims < 1, or alpha not in (0, 1).
    """
    if periods < 2:
        raise ValueError("periods must be at least 2")
    if n_sims < 1:
        raise ValueError("n_sims must be at least 1")
    if not (0.0 < alpha < 1.0):
        raise ValueError("alpha must lie strictly in (0, 1)")

    rng = random.Random(seed)
    dist = statistics.NormalDist()
    critical_value = dist.inv_cdf(1.0 - alpha)
    sqrt_t = math.sqrt(periods)

    rejections = 0
    for _ in range(n_sims):
        # Generate sample of iid normal returns with standard deviation 1.0
        sample = [rng.gauss(sr_per_period, 1.0) for _ in range(periods)]
        mean = math.fsum(sample) / periods
        var = math.fsum((x - mean) ** 2 for x in sample) / (periods - 1)
        if var <= 0.0:
            continue
        hsr = mean / math.sqrt(var)
        test_stat = sqrt_t * hsr
        if test_stat >= critical_value:
            rejections += 1

    return rejections / n_sims
