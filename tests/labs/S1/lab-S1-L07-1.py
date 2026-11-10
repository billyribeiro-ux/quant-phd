"""Lab S1-L07-1: Exact coverage probability of Wald and Wilson confidence intervals.

Evaluates exact coverage probability across a grid of parameter values p for n = 20.
Nominal 95% confidence level.
Standard library only. No external imports.
"""

from __future__ import annotations

import math
import statistics


def main() -> None:
    n = 20
    conf_level = 0.95
    # Standard normal quantile for 95% two-sided interval
    z = statistics.NormalDist().inv_cdf(0.5 + conf_level / 2.0)

    p_grid = [0.05, 0.10, 0.20, 0.50, 0.80, 0.90, 0.95]

    print(f"sample size n: {n}, nominal coverage: {conf_level:.2%}")
    print(f"critical value z: {z:.6f}")
    print("exact coverage probabilities C(p) = sum P(k | p) * I(p in CI(k)):")

    for p in p_grid:
        cov_wald = 0.0
        cov_wilson = 0.0

        for k in range(n + 1):
            prob = math.comb(n, k) * (p**k) * ((1.0 - p) ** (n - k))
            p_hat = k / n

            # 1. Wald interval: p_hat +/- z * sqrt(p_hat * (1 - p_hat) / n)
            se_wald = math.sqrt(p_hat * (1.0 - p_hat) / n)
            wald_lo = p_hat - z * se_wald
            wald_hi = p_hat + z * se_wald
            if wald_lo <= p <= wald_hi:
                cov_wald += prob

            # 2. Wilson score interval
            denom = 1.0 + (z**2) / n
            center = (p_hat + (z**2) / (2.0 * n)) / denom
            radius = (z / denom) * math.sqrt(p_hat * (1.0 - p_hat) / n + (z**2) / (4.0 * n * n))
            wilson_lo = center - radius
            wilson_hi = center + radius
            if wilson_lo <= p <= wilson_hi:
                cov_wilson += prob

        print(f"p = {p:.2f}: Wald coverage = {cov_wald:.4f}, Wilson coverage = {cov_wilson:.4f}")


main()
