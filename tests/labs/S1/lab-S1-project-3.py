"""Lab S1-project-3: Rung 3 reference closed-form numbers for strategy cases.

Standard library only. Evaluates the analytic required years and periods across cases.
No random draws used.
"""

from __future__ import annotations

import math
import statistics


def compute_case(sr_ann: float, k: int, alpha: float, power: float) -> tuple[float, int, float]:
    dist = statistics.NormalDist()
    z_alpha = dist.inv_cdf(1.0 - alpha)
    z_power = dist.inv_cdf(power)
    sr_p = sr_ann / math.sqrt(k)
    inflation = math.sqrt(1.0 + (sr_p**2) / 2.0)
    years = ((z_alpha + z_power * inflation) ** 2) / (sr_ann**2)
    periods = math.ceil(years * k)
    z_stat = (z_alpha - math.sqrt(periods) * sr_p) / inflation
    theo_power = 1.0 - dist.cdf(z_stat)
    return years, periods, theo_power


def main() -> None:
    cases = [
        (0.30, 12, 0.05, 0.80),
        (0.50, 12, 0.05, 0.80),
        (0.70, 12, 0.05, 0.80),
        (1.00, 12, 0.05, 0.80),
        (0.50, 252, 0.05, 0.80),
        (0.50, 12, 0.05, 0.90),
    ]

    print("reference cases for memo comparison (alpha = 0.05):")
    for sr_ann, k, alpha, power in cases:
        years, periods, theo_power = compute_case(sr_ann, k, alpha, power)
        freq = "monthly" if k == 12 else "daily"
        print(
            f"SR_ann = {sr_ann:.2f}, {freq} (k = {k}), power = {power:.2f}: "
            f"years = {years:.4f}, periods = {periods}, theoretical power = {theo_power:.4f}"
        )


main()
