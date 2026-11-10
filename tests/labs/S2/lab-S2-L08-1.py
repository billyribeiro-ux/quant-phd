"""Lab S2-L08-1: Classical versus White HC0 coverage under heteroskedasticity.

Demonstrates the breakdown of homoskedastic OLS standard errors when error variance
increases with regressor magnitude, and validates the nominal 95% coverage of
White (1980) heteroskedasticity-robust standard errors. Standard library only.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    rng = random.Random(42)
    n = 200
    replications = 3000
    beta_0 = 1.00
    beta_1 = 2.00
    z_crit = 1.96

    cov_classical = 0
    cov_hc0 = 0

    for _ in range(replications):
        x = [rng.gauss(0.0, 1.0) for _ in range(n)]
        x_bar = sum(x) / n
        sxx = sum((xi - x_bar) ** 2 for xi in x)

        # Strongly heteroskedastic error: sigma_i = 1.0 + 2.0 * x_i^2
        errors = [rng.gauss(0.0, 1.0 + 2.0 * xi**2) for xi in x]
        y = [beta_0 + beta_1 * xi + ei for xi, ei in zip(x, errors, strict=True)]
        y_bar = sum(y) / n
        sxy = sum((xi - x_bar) * (yi - y_bar) for xi, yi in zip(x, y, strict=True))
        b1_hat = sxy / sxx
        e = [yi - (y_bar + b1_hat * (xi - x_bar)) for xi, yi in zip(x, y, strict=True)]

        # Classical homoskedastic standard error
        s2 = sum(ei**2 for ei in e) / (n - 2)
        se_classical = math.sqrt(s2 / sxx)

        # White (1980) HC0 heteroskedasticity-robust standard error
        meat = sum(((xi - x_bar) ** 2) * (ei**2) for xi, ei in zip(x, e, strict=True))
        se_hc0 = math.sqrt(meat) / sxx

        if b1_hat - z_crit * se_classical <= beta_1 <= b1_hat + z_crit * se_classical:
            cov_classical += 1
        if b1_hat - z_crit * se_hc0 <= beta_1 <= b1_hat + z_crit * se_hc0:
            cov_hc0 += 1

    rate_classical = cov_classical / replications
    rate_hc0 = cov_hc0 / replications

    print("Estimator     | Nominal | Empirical Coverage | Under-coverage")
    print("-" * 59)
    print(f"Classical OLS |  0.9500 |             {rate_classical:.4f} |        {0.95 - rate_classical:+.4f}")
    print(f"White HC0     |  0.9500 |             {rate_hc0:.4f} |        {0.95 - rate_hc0:+.4f}")


main()
