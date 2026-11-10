"""Lab S1-project-1: Rung 1 worked example: power analysis for a strategy.

Computes the required years and periods in closed form, checks theoretical power,
and confirms via seeded Monte Carlo simulation.
SIMULATED: all returns are generated with random.Random(20261109).
Standard library only. No external imports.
"""

from __future__ import annotations

import math
import random
import statistics


def main() -> None:
    # Strategy parameters
    sr_ann = 0.60  # Annualized Sharpe ratio
    k = 12  # Monthly observations per year
    alpha = 0.05  # One-sided significance level
    power = 0.80  # Target statistical power

    dist = statistics.NormalDist()
    z_alpha = dist.inv_cdf(1.0 - alpha)
    z_power = dist.inv_cdf(power)

    # Per-period parameters
    sr_period = sr_ann / math.sqrt(k)
    # Alternative variance inflation factor: 1 + SR^2 / 2
    inflation_factor = 1.0 + (sr_period**2) / 2.0
    inflation_sd = math.sqrt(inflation_factor)

    # Analytic required years and required periods
    years = ((z_alpha + z_power * inflation_sd) ** 2) / (sr_ann**2)
    periods = math.ceil(years * k)

    # Theoretical power at integer periods T
    z_stat = (z_alpha - math.sqrt(periods) * sr_period) / inflation_sd
    theoretical_power = 1.0 - dist.cdf(z_stat)

    # Seeded Monte Carlo simulation of power
    seed = 20261109
    rng = random.Random(seed)
    n_sims = 2000
    rejections = 0
    sqrt_t = math.sqrt(periods)

    for _ in range(n_sims):
        sample = [rng.gauss(sr_period, 1.0) for _ in range(periods)]
        m = math.fsum(sample) / periods
        v = math.fsum((x - m) ** 2 for x in sample) / (periods - 1)
        if v > 0.0 and sqrt_t * (m / math.sqrt(v)) >= z_alpha:
            rejections += 1

    sim_power = rejections / n_sims

    print("strategy power analysis (worked example):")
    print(f"annualized Sharpe ratio SR_ann: {sr_ann:.2f}, periods per year k: {k}")
    print(f"one-sided alpha: {alpha:.2f}, target power: {power:.2f}")
    print(f"per-period Sharpe ratio SR: {sr_period:.4f}")
    print(f"variance inflation factor 1 + SR^2 / 2: {inflation_factor:.6f}")
    print(f"analytic required years: {years:.4f}")
    print(f"required integer periods T = ceil(y * k): {periods}")
    print(f"theoretical power achieved at T = {periods}: {theoretical_power:.4f}")
    print(f"simulated power (N = {n_sims}, seed = {seed}): {sim_power:.4f}")


main()
