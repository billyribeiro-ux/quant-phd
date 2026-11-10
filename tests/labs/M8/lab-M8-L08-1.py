"""Lab M8-L08-1: Importance sampling for Gaussian tail probability estimation.

Standard library only. Compares crude Monte Carlo to exponentially tilted importance
sampling for estimating P(Z > 4) (SIMULATED).
"""

from __future__ import annotations

import math
import random


def main() -> None:
    c = 4.0
    # Exact probability: P(Z > 4) = 1 - Phi(4) = 1/2 erfc(4 / sqrt(2))
    exact_prob = 0.5 * math.erfc(c / math.sqrt(2.0))

    print("=== Importance Sampling for Gaussian Tail P(Z > 4) (SIMULATED) ===")
    print(f"Exact theoretical tail probability: {exact_prob:.12e}")

    n = 100_000
    rng = random.Random(42)

    # 1. Crude Monte Carlo: Z ~ N(0, 1)
    z_crude = [rng.gauss(0.0, 1.0) for _ in range(n)]
    hits_crude = [1.0 if z > c else 0.0 for z in z_crude]
    p_crude = sum(hits_crude) / n
    var_crude = p_crude * (1.0 - p_crude)
    se_crude = math.sqrt(var_crude / n)
    rel_se_crude = (se_crude / p_crude) if p_crude > 0 else float("inf")

    # 2. Importance Sampling with shifted proposal Y ~ N(mu, 1) with mu = c = 4
    # Likelihood ratio w(y) = phi(y) / phi(y - c) = exp(-c*y + c^2 / 2)
    # Integrand: 1_{Y > c} * exp(-c*Y + c^2 / 2)
    rng_is = random.Random(42)
    y_is = [rng_is.gauss(c, 1.0) for _ in range(n)]
    c_sq_half = 0.5 * c * c
    weights = [math.exp(-c * y + c_sq_half) if y > c else 0.0 for y in y_is]

    p_is = sum(weights) / n
    var_is = sum((w - p_is) ** 2 for w in weights) / (n - 1)
    se_is = math.sqrt(var_is / n)
    rel_se_is = se_is / p_is

    print(f"\nSample size: N = {n}")
    print(f"Crude MC:     Estimate = {p_crude:.6e}, Hits = {int(sum(hits_crude))}")
    print(f"              Std Error = {se_crude:.4e}, Rel Std Error = {rel_se_crude:.2%}")
    print(f"Importance S: Estimate = {p_is:.6e}")
    print(f"              Std Error = {se_is:.4e}, Rel Std Error = {rel_se_is:.2%}")
    print(f"Variance reduction factor Var(Crude) / Var(IS): {var_crude / var_is:.1f}x")
    print(f"Standard error reduction factor SE(Crude) / SE(IS): {se_crude / se_is:.1f}x")


main()
