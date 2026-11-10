"""Lab 5 · CGMY Lévy density integration and small-jump activity across Y.

Under the CGMY model (Carr, Geman, Madan & Yor 2002), the Lévy density on the positive axis is:
k(x) = C * exp(-M * x) / (x^(1 + Y)),   x > 0.
The total arrival rate of jumps with size exceeding threshold epsilon > 0 is:
Lambda(epsilon) = integral_epsilon^infinity C * exp(-M * x) / (x^(1 + Y)) dx.
The behavior as epsilon -> 0 depends fundamentally on the activity parameter Y:
- For Y < 0: Lambda(epsilon) converges to a finite limit Lambda(0) < infinity (finite activity / compound Poisson).
- For Y = 0 (Variance Gamma): Lambda(epsilon) ~ C * ln(1/epsilon) -> infinity (infinite activity, finite variation).
- For 0 < Y < 1: Lambda(epsilon) ~ (C/Y) * epsilon^(-Y) -> infinity (infinite activity, finite variation).
- For 1 <= Y < 2: both jump frequency and first variation diverge (infinite activity, infinite variation).
This lab numerically integrates the positive CGMY Lévy density for C = 1.0, M = 5.0 across Y in {-0.5, 0.0, 0.5}
and cutoffs epsilon in {0.1, 0.01, 0.001} (SIMULATED), demonstrating the explosion of small jumps.
"""

from __future__ import annotations

import math

from scipy.integrate import quad  # type: ignore[import-untyped]


def cgmy_density(x: float, c: float, m: float, y: float) -> float:
    """Evaluate CGMY right-tail Lévy density C * exp(-M * x) / x^(1 + Y)."""
    return float(c * math.exp(-m * x) / (x ** (1.0 + y)))


def main() -> None:
    c = 1.0
    m = 5.0
    y_values = [-0.5, 0.0, 0.5]
    epsilons = [0.1, 0.01, 0.001]

    results: dict[float, list[float]] = {}

    print(f"CGMY parameters: C = {c:.2f}, M = {m:.2f} (SIMULATED)")
    print("jump arrival intensity Lambda(epsilon) = int_epsilon^inf k(x) dx:")

    for y in y_values:
        row: list[float] = []
        for eps in epsilons:

            def density(x: float, y_param: float = y) -> float:
                return cgmy_density(x, c, m, y_param)

            val, _ = quad(density, eps, 20.0, limit=200)
            row.append(val)
        results[y] = row
        print(f"  Y = {y:4.1f}: eps=0.100 -> {row[0]:8.4f}, eps=0.010 -> {row[1]:8.4f}, eps=0.001 -> {row[2]:8.4f}")

    # Invariants:
    # 1. For Y = -0.5, the integral is bounded: ratio row[2] / row[1] is close to 1.0 (< 1.5).
    # 2. For Y = 0.5, the integral explodes by ~sqrt(10) ~ 3.16 per decade: row[2] / row[1] > 2.5.
    ratio_neg = results[-0.5][2] / results[-0.5][1]
    ratio_pos = results[0.5][2] / results[0.5][1]

    print(f"growth ratio (eps=0.001 vs eps=0.010) for Y = -0.5: {ratio_neg:.3f}")
    print(f"growth ratio (eps=0.001 vs eps=0.010) for Y =  0.5: {ratio_pos:.3f}")
    print("finite activity bounded growth (Y=-0.5):", ratio_neg < 1.5)
    print("infinite activity power-law explosion (Y=0.5):", ratio_pos > 2.5)


main()
