"""Lab S2-L04-1: Gauss-Markov theorem Monte Carlo efficiency comparison.

Compares the empirical variance of the OLS estimator against an alternative
linear unbiased estimator on a fixed design under homoskedastic errors.
SIMULATED: generated using standard library random.Random(42).
"""

from __future__ import annotations

import random


def main() -> None:
    rng = random.Random(42)
    # Fixed design matrix: n = 10 observations, k = 2 (intercept and slope x)
    x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    n = len(x)
    x_bar = sum(x) / n
    sxx = sum((xi - x_bar) ** 2 for xi in x)

    # OLS weights for slope: w_i = (x_i - x_bar) / sxx
    w_ols = [(xi - x_bar) / sxx for xi in x]

    # Alternative linear unbiased weights:
    # Must satisfy sum(w) = 0 (unbiased for intercept) and sum(w * x) = 1 (unbiased for slope)
    # Take difference between average of last two and average of first two observations:
    # w_alt: first two are -0.25, last two are +0.25, middle are 0.0
    # Mean of x in first two: 1.5; mean of x in last two: 9.5; diff = 8.0
    # Scaling by 1/8.0: w_alt: [-0.0625, -0.0625, 0, ..., 0, 0.0625, 0.0625]
    diff_x = ((x[-1] + x[-2]) / 2.0) - ((x[0] + x[1]) / 2.0)
    w_alt = [-0.5 / diff_x, -0.5 / diff_x] + [0.0] * (n - 4) + [0.5 / diff_x, 0.5 / diff_x]

    # Verify linear unbiasedness conditions
    assert abs(sum(w_ols)) < 1e-12
    assert abs(sum(w * xi for w, xi in zip(w_ols, x, strict=True)) - 1.0) < 1e-12

    assert abs(sum(w_alt)) < 1e-12
    assert abs(sum(w * xi for w, xi in zip(w_alt, x, strict=True)) - 1.0) < 1e-12

    # Theoretical variances under sigma^2 = 1.0
    sigma2 = 1.0
    var_ols_theo = sigma2 * sum(w**2 for w in w_ols)
    var_alt_theo = sigma2 * sum(w**2 for w in w_alt)

    # Monte Carlo simulation: R = 5000 replications
    replications = 5000
    beta_true = 2.0
    alpha_true = 1.0

    b1_ols_draws: list[float] = []
    b1_alt_draws: list[float] = []

    for _ in range(replications):
        # Draw homoskedastic standard normal disturbances
        errors = [rng.gauss(0.0, 1.0) for _ in range(n)]
        y = [alpha_true + beta_true * xi + ei for xi, ei in zip(x, errors, strict=True)]

        b1_ols = sum(w * yi for w, yi in zip(w_ols, y, strict=True))
        b1_alt = sum(w * yi for w, yi in zip(w_alt, y, strict=True))

        b1_ols_draws.append(b1_ols)
        b1_alt_draws.append(b1_alt)

    # Empirical moments
    mean_ols = sum(b1_ols_draws) / replications
    mean_alt = sum(b1_alt_draws) / replications

    var_ols_emp = sum((b - mean_ols) ** 2 for b in b1_ols_draws) / (replications - 1)
    var_alt_emp = sum((b - mean_alt) ** 2 for b in b1_alt_draws) / (replications - 1)

    print(f"Theoretical Var(OLS): {var_ols_theo:.6f}")
    print(f"Theoretical Var(Alt): {var_alt_theo:.6f}")
    print(f"Empirical Mean OLS: {mean_ols:.4f} (True: {beta_true})")
    print(f"Empirical Mean Alt: {mean_alt:.4f} (True: {beta_true})")
    print(f"Empirical Var(OLS): {var_ols_emp:.6f}")
    print(f"Empirical Var(Alt): {var_alt_emp:.6f}")
    print(f"Variance ratio Var(Alt)/Var(OLS): {var_alt_emp / var_ols_emp:.4f}")


main()
