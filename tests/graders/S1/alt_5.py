"""Alternative implementation 5: required_periods by integer discrete search."""

from __future__ import annotations

import math
import random
import statistics


def sharpe_hat(returns: list[float]) -> float:
    n = len(returns)
    if n < 2:
        raise ValueError("fewer than two returns provided")
    mean = math.fsum(returns) / n
    var = math.fsum((r - mean) ** 2 for r in returns) / (n - 1)
    if var <= 0.0:
        raise ValueError("sample standard deviation is zero")
    return mean / math.sqrt(var)


def analytic_years(sr_ann: float, periods_per_year: int, alpha: float, power: float) -> float:
    if sr_ann <= 0.0 or periods_per_year < 1 or not (0.0 < alpha < 1.0) or not (0.0 < power < 1.0):
        raise ValueError("invalid parameter value")
    dist = statistics.NormalDist()
    z_alpha = dist.inv_cdf(1.0 - alpha)
    z_power = dist.inv_cdf(power)
    inflation = math.sqrt(1.0 + (sr_ann**2) / (2.0 * periods_per_year))
    return ((z_alpha + z_power * inflation) ** 2) / (sr_ann**2)


def _power_at_t(t: int, sr_ann: float, k: int, alpha: float) -> float:
    dist = statistics.NormalDist()
    z_alpha = dist.inv_cdf(1.0 - alpha)
    sr_p = sr_ann / math.sqrt(k)
    inflation = math.sqrt(1.0 + (sr_p**2) / 2.0)
    z_stat = (z_alpha - math.sqrt(t) * sr_p) / inflation
    return 1.0 - dist.cdf(z_stat)


def required_periods(sr_ann: float, periods_per_year: int, alpha: float, power: float) -> int:
    # First compute analytic continuous estimate
    years = analytic_years(sr_ann, periods_per_year, alpha, power)
    guess = max(1, int(years * periods_per_year))

    # Verify and step if needed
    t = guess
    while _power_at_t(t, sr_ann, periods_per_year, alpha) < power - 1e-12:
        t += 1
    while t > 1 and _power_at_t(t - 1, sr_ann, periods_per_year, alpha) >= power - 1e-12:
        t -= 1
    return t


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
