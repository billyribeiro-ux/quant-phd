"""Student error: ignores the alternative variance inflation factor in analytic_years."""

from __future__ import annotations

import math
import random
import statistics


def sharpe_hat(returns: list[float]) -> float:
    n = len(returns)
    if n < 2:
        raise ValueError("fewer than two returns")
    mean = math.fsum(returns) / n
    var = math.fsum((r - mean) ** 2 for r in returns) / (n - 1)
    if var <= 0.0:
        raise ValueError("sample variance zero")
    return mean / math.sqrt(var)


def analytic_years(sr_ann: float, periods_per_year: int, alpha: float, power: float) -> float:
    if sr_ann <= 0.0 or periods_per_year < 1 or not (0.0 < alpha < 1.0) or not (0.0 < power < 1.0):
        raise ValueError("invalid parameter value")
    dist = statistics.NormalDist()
    z_alpha = dist.inv_cdf(1.0 - alpha)
    z_power = dist.inv_cdf(power)
    # Error: ignores sqrt(1 + SR^2/2) inflation
    return ((z_alpha + z_power) ** 2) / (sr_ann**2)


def required_periods(sr_ann: float, periods_per_year: int, alpha: float, power: float) -> int:
    years = analytic_years(sr_ann, periods_per_year, alpha, power)
    return math.ceil(years * periods_per_year)


def simulated_power(periods: int, sr_per_period: float, alpha: float, n_sims: int, seed: int) -> float:
    if periods < 2 or n_sims < 1 or not (0.0 < alpha < 1.0):
        raise ValueError("invalid parameter value")
    rng = random.Random(seed)
    dist = statistics.NormalDist()
    critical_value = dist.inv_cdf(1.0 - alpha)
    sqrt_t = math.sqrt(periods)

    rejections = 0
    for _ in range(n_sims):
        sample = [rng.gauss(sr_per_period, 1.0) for _ in range(periods)]
        mean = math.fsum(sample) / periods
        var = math.fsum((x - mean) ** 2 for x in sample) / (periods - 1)
        if var > 0.0 and sqrt_t * (mean / math.sqrt(var)) >= critical_value:
            rejections += 1
    return rejections / n_sims
