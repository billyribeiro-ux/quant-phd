"""Alternative implementation 3: analytic_years by bisection on the power equation."""

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


def _power_at_years(y: float, sr_ann: float, k: int, alpha: float) -> float:
    dist = statistics.NormalDist()
    z_alpha = dist.inv_cdf(1.0 - alpha)
    t = y * k
    sr_p = sr_ann / math.sqrt(k)
    inflation = math.sqrt(1.0 + (sr_p**2) / 2.0)
    z_stat = (z_alpha - math.sqrt(t) * sr_p) / inflation
    return 1.0 - dist.cdf(z_stat)


def analytic_years(sr_ann: float, periods_per_year: int, alpha: float, power: float) -> float:
    if sr_ann <= 0.0 or periods_per_year < 1 or not (0.0 < alpha < 1.0) or not (0.0 < power < 1.0):
        raise ValueError("invalid parameter value")

    # Initial bracket
    lo = 1e-4
    hi = 100.0
    while _power_at_years(hi, sr_ann, periods_per_year, alpha) < power:
        hi *= 2.0

    for _ in range(60):
        mid = 0.5 * (lo + hi)
        p_mid = _power_at_years(mid, sr_ann, periods_per_year, alpha)
        if p_mid < power:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


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
