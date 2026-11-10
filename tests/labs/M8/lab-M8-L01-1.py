"""Lab M8-L01-1: Catastrophic cancellation in arithmetic, roots, and sample variance.

Standard library only. All offsets and simulated sequences are deterministic.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    print("=== Part A: Cancellation in (1 + h) - 1 ===")
    for k in [1, 5, 10, 14, 15, 16, 17]:
        h = 10.0 ** (-k)
        computed = (1.0 + h) - 1.0
        rel_err = abs(computed - h) / h if h != 0.0 else 0.0
        print(f"k={k:2d}: h={h:.1e}, computed={computed:.16e}, rel_err={rel_err:.2e}")

    print("\n=== Part B: Quadratic Roots for b^2 >> 4ac ===")
    # Solve x^2 + 10^8 x + 1 = 0.
    # True roots: x1 ~ -10^8, x2 ~ -10^-8
    a, b, c = 1.0, 1.0e8, 1.0
    disc = math.sqrt(b * b - 4.0 * a * c)

    # Standard textbook formula for smaller root (in magnitude)
    x2_textbook = (-b + disc) / (2.0 * a)

    # Numerically stable Citardauq formula
    x2_stable = (2.0 * c) / (-b - math.copysign(disc, b))

    # Exact high-precision approximation for x2 via Taylor series:
    # -c/b * (1 + a*c/b^2) = -1e-8 * (1 + 1e-16) ~ -1.0000000000000000e-8
    x2_exact = -1.0e-8
    err_textbook = abs(x2_textbook - x2_exact)
    err_stable = abs(x2_stable - x2_exact)

    print(f"x2 textbook: {x2_textbook:.16e}, abs error: {err_textbook:.2e}")
    print(f"x2 stable:   {x2_stable:.16e}, abs error: {err_stable:.2e}")

    print("\n=== Part C: Sample Variance of Offset Data (SIMULATED) ===")
    rng = random.Random(42)
    n = 1000
    base_data = [rng.gauss(0.0, 1.0) for _ in range(n)]

    # Exact two-pass sample variance of base data
    mean_base = sum(base_data) / n
    var_base = sum((x - mean_base) ** 2 for x in base_data) / (n - 1)

    # Add large offset: variance should be invariant to constant shift Var(X + C) = Var(X)
    offset = 1.0e9
    shifted_data = [x + offset for x in base_data]

    # Naive one-pass formula: Var = (sum(x^2) - (sum x)^2 / n) / (n - 1)
    sum_x = sum(shifted_data)
    sum_sq = sum(x * x for x in shifted_data)
    var_naive = (sum_sq - (sum_x * sum_x) / n) / (n - 1)

    # Numerically stable two-pass formula
    mean_shifted = sum_x / n
    var_two_pass = sum((x - mean_shifted) ** 2 for x in shifted_data) / (n - 1)

    print(f"True variance:       {var_base:.10f}")
    print(f"Stable two-pass var: {var_two_pass:.10f}, error: {abs(var_two_pass - var_base):.2e}")
    print(f"Naive one-pass var:  {var_naive:.10f}, error: {abs(var_naive - var_base):.2e}")


main()
