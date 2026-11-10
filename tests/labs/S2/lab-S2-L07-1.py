"""Lab S2-L07-1: Asymptotic distribution and coverage of OLS under non-normal errors.

Evaluates coverage of asymptotic t-intervals across sample sizes n = 20, 80, 320
under centered exponential errors. Standard library only.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    rng = random.Random(42)
    sample_sizes = [20, 80, 320]
    replications = 3000

    beta_0 = 1.00
    beta_1 = 2.00

    # Exponential parameter: scale = 1.0, mean = 1.0, var = 1.0
    # Centered exponential error: e = Exp(1) - 1.0 (mean = 0, var = 1, skewness = 2, kurtosis = 9)

    print("Sample Size n | Nominal | Empirical Coverage | Binomial SE")
    print("-" * 55)

    for n in sample_sizes:
        covered = 0
        df = n - 2
        # Student-t critical value approximation for df degrees of freedom
        # For df >= 18, t_0.975 is close to 1.96 + 2.4 / df
        # Let's compute accurate t critical value using continued fraction / standard series or known values:
        if n == 20:
            t_crit = 2.1009  # df = 18
        elif n == 80:
            t_crit = 1.9908  # df = 78
        else:
            t_crit = 1.9675  # df = 318

        for _ in range(replications):
            # Uniform regressor x in [1, 5]
            x = [rng.uniform(1.0, 5.0) for _ in range(n)]
            # Centered exponential disturbance: -log(U) - 1.0
            errors = [-math.log(rng.random()) - 1.0 for _ in range(n)]
            y = [beta_0 + beta_1 * xi + ei for xi, ei in zip(x, errors, strict=True)]

            x_bar = sum(x) / n
            y_bar = sum(y) / n
            sxx = sum((xi - x_bar) ** 2 for xi in x)
            sxy = sum((xi - x_bar) * (yi - y_bar) for xi, yi in zip(x, y, strict=True))

            b1_hat = sxy / sxx
            resids = [yi - (y_bar + b1_hat * (xi - x_bar)) for xi, yi in zip(x, y, strict=True)]
            rss = sum(ri**2 for ri in resids)

            sigma2_hat = rss / df
            se_b1 = math.sqrt(sigma2_hat / sxx)

            margin = t_crit * se_b1
            if b1_hat - margin <= beta_1 <= b1_hat + margin:
                covered += 1

        coverage_rate = covered / replications
        binom_se = math.sqrt(coverage_rate * (1.0 - coverage_rate) / replications)

        print(f"      n = {n:3d} |  0.9500 |             {coverage_rate:.4f} |      {binom_se:.4f}")


main()
