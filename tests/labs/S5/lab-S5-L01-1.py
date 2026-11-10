"""Lab S5-L01-1: Just-identified sample moment conditions in GMM.

SIMULATED: generates synthetic instrumental variable series with known true parameter,
computes the closed-form method of moments estimator and numerical GMM root,
and verifies exact equality and zero sample moment condition.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    seed = 42
    rng = np.random.default_rng(seed)
    n = 500
    theta_true = 1.75

    # Instrument z, endogenous regressor x correlated with structural error eps
    z = rng.normal(loc=0.0, scale=1.0, size=n)
    v = rng.normal(loc=0.0, scale=0.5, size=n)
    eps = 0.6 * v + rng.normal(loc=0.0, scale=0.8, size=n)
    x = 1.2 * z + v
    y = theta_true * x + eps

    # Closed-form IV / Method of Moments estimator
    # Sample moment: g_n(theta) = (1/n) * sum(z * (y - x * theta)) = 0
    # => theta_hat = sum(z * y) / sum(z * x)
    zy = float(np.sum(z * y))
    zx = float(np.sum(z * x))
    theta_closed = zy / zx

    # GMM numerical criterion: Q(theta) = (g_n(theta))^2
    # Analytical gradient: d/dtheta g_n(theta) = - (1/n) * sum(z * x)
    # Newton step from initial guess theta_0 = 0.0
    theta_guess = 0.0
    for _ in range(5):
        g_val = float(np.mean(z * (y - x * theta_guess)))
        dg_val = -float(np.mean(z * x))
        theta_guess = theta_guess - g_val / dg_val

    theta_gmm = theta_guess
    sample_moment = float(np.mean(z * (y - x * theta_gmm)))
    abs_diff = abs(theta_gmm - theta_closed)

    print("Lab S5-L01-1: Just-Identified GMM Estimation")
    print(f"  Sample size T: {n} (SIMULATED, seed {seed})")
    print(f"  True parameter theta_0: {theta_true:.4f}")
    print(f"  Closed-form IV estimator: {theta_closed:.6f}")
    print(f"  Numerical GMM root: {theta_gmm:.6f}")
    print(f"  Absolute difference: {abs_diff:.2e}")
    print(f"  Evaluated sample moment g_T(theta_hat): {sample_moment:.2e}")
    print(f"  Exact root property (|g_T| < 1e-12): {abs(sample_moment) < 1e-12}")


main()
