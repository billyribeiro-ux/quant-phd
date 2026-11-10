"""Lab 6: Copula Models, Sklar's Theorem, and Non-Linear Tail Comovement.

Demonstrates Sklar's decomposition and proves that the Student-t copula generates
substantially higher extreme co-crashes than the Gaussian copula with identical linear correlation.
"""

from __future__ import annotations

import math

import numpy as np
import scipy.special
import scipy.stats


def main() -> None:
    rng = np.random.default_rng(42)
    n_sims = 100_000
    rho = 0.50

    cov = np.array([[1.0, rho], [rho, 1.0]], dtype=np.float64)
    chol = np.linalg.cholesky(cov)

    # 1. Bivariate Gaussian Copula
    z = rng.standard_normal((n_sims, 2)) @ chol.T
    u_norm = 0.5 * (1.0 + scipy.special.erf(z / math.sqrt(2.0)))

    # 2. Bivariate Student-t Copula (df = 4)
    v = rng.chisquare(df=4, size=(n_sims, 1))
    t_samples = z / np.sqrt(v / 4.0)
    u_t = scipy.stats.t.cdf(t_samples, df=4)

    # 3. Evaluate Joint Tail Risk at q = 0.99 (99th percentile loss quadrant)
    q = 0.99
    joint_norm = float(np.mean((u_norm[:, 0] > q) & (u_norm[:, 1] > q)))
    joint_t = float(np.mean((u_t[:, 0] > q) & (u_t[:, 1] > q)))
    independent_benchmark = (1.0 - q) ** 2  # 0.0001

    print(f"Simulation Runs: {n_sims} | Target Correlation rho: {rho:.2f}")
    print(f"Independent Baseline Joint P(U1 > 0.99, U2 > 0.99): {independent_benchmark:.6f}")
    print(f"Gaussian Copula Joint P(U1 > 0.99, U2 > 0.99):     {joint_norm:.6f}")
    print(f"Student-t Copula Joint P(U1 > 0.99, U2 > 0.99):    {joint_t:.6f}")
    print("-" * 65)
    ratio = joint_t / joint_norm
    print(f"Student-t / Gaussian Joint Tail Multiplier: {ratio:.2f}x")


main()
