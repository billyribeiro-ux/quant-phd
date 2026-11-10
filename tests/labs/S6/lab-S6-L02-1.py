"""Lab S6-L02-1: Instrumental variables and the Wald estimator identity.

SIMULATED: verifies that the Wald ratio of differences in means identically equals
the ratio of sample covariances, and demonstrates that 2SLS / IV recovers the true
causal parameter under endogeneity where OLS fails.
"""

from __future__ import annotations

import random


def main() -> None:
    rng = random.Random(101)
    n = 12000

    # True parameters: structural equation Y = alpha + beta * D + eps
    true_alpha = 1.00
    true_beta = 3.00

    # Binary instrument Z in {0, 1}
    z = [1 if rng.random() < 0.5 else 0 for _ in range(n)]

    # Confounder U affects both D and Y (creating endogeneity)
    u = [rng.gauss(0.0, 1.2) for _ in range(n)]

    # First stage: D is endogenous, positively correlated with Z and U
    # D = gamma_0 + gamma_1 * Z + pi * U + v
    gamma_1 = 0.65
    d = [1 if (0.2 + gamma_1 * z[i] + 0.8 * u[i] + rng.gauss(0.0, 0.5)) > 0.8 else 0 for i in range(n)]

    # Structural outcome Y: affected by D, U (unobserved), and independent noise
    eps = [u[i] + rng.gauss(0.0, 0.8) for i in range(n)]  # Cov(D, eps) > 0
    y = [true_alpha + true_beta * d[i] + eps[i] for i in range(n)]

    # 1. Compute Wald estimator from subgroup sample means
    n_z1 = sum(z)
    n_z0 = n - n_z1

    y_bar_z1 = sum(y[i] for i in range(n) if z[i] == 1) / n_z1
    y_bar_z0 = sum(y[i] for i in range(n) if z[i] == 0) / n_z0

    d_bar_z1 = sum(d[i] for i in range(n) if z[i] == 1) / n_z1
    d_bar_z0 = sum(d[i] for i in range(n) if z[i] == 0) / n_z0

    wald_beta = (y_bar_z1 - y_bar_z0) / (d_bar_z1 - d_bar_z0)

    # 2. Compute covariance ratio: Cov(Y, Z) / Cov(D, Z)
    z_bar = sum(z) / n
    y_bar = sum(y) / n
    d_bar = sum(d) / n

    cov_yz = sum((y[i] - y_bar) * (z[i] - z_bar) for i in range(n)) / n
    cov_dz = sum((d[i] - d_bar) * (z[i] - z_bar) for i in range(n)) / n
    cov_ratio_beta = cov_yz / cov_dz

    # 3. Naive OLS estimator: Cov(Y, D) / Var(D)
    cov_yd = sum((y[i] - y_bar) * (d[i] - d_bar) for i in range(n)) / n
    var_d = sum((d[i] - d_bar) ** 2 for i in range(n)) / n
    ols_beta = cov_yd / var_d

    discrepancy = abs(wald_beta - cov_ratio_beta)

    print("Instrumental Variables Identification & Wald Equivalence (SIMULATED):")
    print(f"  Sample size N: {n}")
    print(f"  True causal beta: {true_beta:.4f}")
    print(f"  Naive OLS estimate: {ols_beta:.4f} (biased by endogeneity)")
    print("\nWald Estimator Components:")
    print(f"  E[Y|Z=1] - E[Y|Z=0] (Reduced Form): {y_bar_z1 - y_bar_z0:.4f}")
    print(f"  E[D|Z=1] - E[D|Z=0] (First Stage):   {d_bar_z1 - d_bar_z0:.4f}")
    print(f"  Wald ratio: {wald_beta:.6f}")
    print(f"  Sample covariance ratio: {cov_ratio_beta:.6f}")
    print(f"  Numerical discrepancy: {discrepancy:.2e}")
    print(f"  Wald recovery error: {abs(wald_beta - true_beta):.4f}")


main()
