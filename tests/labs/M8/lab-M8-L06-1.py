"""Lab M8-L06-1: PRNG determinism and Monte Carlo integration error scaling.

Standard library only. Demonstrates pseudo-random determinism from seeds,
sample variance, standard error, and the O(1/sqrt(n)) Monte Carlo rate (SIMULATED).
"""

from __future__ import annotations

import math
import random


def main() -> None:
    print("=== Part A: PRNG Determinism from Seed ===")
    rng1 = random.Random(42)
    rng2 = random.Random(42)
    draws1 = [rng1.random() for _ in range(5)]
    draws2 = [rng2.random() for _ in range(5)]
    print("PRNG 1 first 5 draws:", [f"{x:.8f}" for x in draws1])
    print("PRNG 2 first 5 draws:", [f"{x:.8f}" for x in draws2])
    print("Sequences match bit-for-bit:", draws1 == draws2)

    print("\n=== Part B: Monte Carlo Integration of int_0^1 exp(x) dx (SIMULATED) ===")
    # Exact integral theta = e - 1
    theta = math.e - 1.0
    # Exact variance: Var(e^U) = E[e^(2U)] - (E[e^U])^2 = (e^2 - 1)/2 - (e - 1)^2
    true_var = (math.exp(2.0) - 1.0) / 2.0 - theta**2
    true_sd = math.sqrt(true_var)

    print(f"Exact integral theta = e - 1: {theta:.16f}")
    print(f"Exact integrand variance:     {true_var:.10f} (SD: {true_sd:.10f})")
    print("    n       Estimate theta_n    Std Error (se)    Abs Error      Error * sqrt(n)")

    rng = random.Random(2026)
    for exponent in [3, 4, 5, 6]:
        n = 10**exponent
        # Draw n uniform variates in [0, 1]
        sample = [math.exp(rng.random()) for _ in range(n)]
        theta_hat = sum(sample) / n
        s_sq = sum((x - theta_hat) ** 2 for x in sample) / (n - 1)
        s = math.sqrt(s_sq)
        se = s / math.sqrt(n)
        abs_err = abs(theta_hat - theta)
        scaled_err = abs_err * math.sqrt(n)

        print(f"{n:8d}   {theta_hat:.10f}      {se:.4e}        {abs_err:.4e}     {scaled_err:.4f}")


main()
