"""Lab S1-project-2: Rung 2 completion problem completed solution.

Standard library only. Computes the alternative variance inflation factor
and the integer required periods ceil(years * periods_per_year).
"""

from __future__ import annotations

import math
import statistics


def variance_inflation(sr_per_period: float) -> float:
    """Compute the alternative variance inflation factor 1 + SR^2 / 2."""
    return 1.0 + (sr_per_period**2) / 2.0


def ceiling_periods(years: float, periods_per_year: int) -> int:
    """Compute the smallest integer number of periods ceil(years * periods_per_year)."""
    return math.ceil(years * periods_per_year)


def main() -> None:
    sr_ann = 0.80
    k = 12
    alpha = 0.05
    power = 0.90

    dist = statistics.NormalDist()
    z_alpha = dist.inv_cdf(1.0 - alpha)
    z_power = dist.inv_cdf(power)

    sr_p = sr_ann / math.sqrt(k)
    inflation = variance_inflation(sr_p)
    years = ((z_alpha + z_power * math.sqrt(inflation)) ** 2) / (sr_ann**2)
    periods = ceiling_periods(years, k)

    print(f"annualized Sharpe ratio: {sr_ann:.2f}, k: {k}")
    print(f"per-period Sharpe ratio: {sr_p:.4f}")
    print(f"variance inflation factor: {inflation:.6f}")
    print(f"analytic required years: {years:.4f}")
    print(f"required periods: {periods}")


main()
