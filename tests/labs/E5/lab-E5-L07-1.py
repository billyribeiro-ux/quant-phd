"""E5 L07 lab 1: the Taylor-type policy rule evaluated exactly, and its response to an inflation gap.

Standard library only (fractions). No randomness and no network, so every run prints the same lines.

Every parameter is an illustrative input chosen for the arithmetic, not an estimate: the natural real rate
r^n = 1 percent per year, the inflation target 2 percent per year, and the coefficients phi_pi = 3/2 and
phi_y = 1/2. No published value is used. All rates are in percent per year, and the output gap is in percent of
trend output (Lesson 4). Every number is an exact Fraction, so nothing is rounded.

Part A: the nominal policy rate i = r^n + pi + phi_pi (pi - target) + phi_y y on a grid of inflation rates and
output gaps.
Part B: the nominal and the real response to a one-point inflation gap at output gap zero, for four values of phi_pi.
Part C: the rule is affine in inflation, so its second differences are zero, and the real rate rises with inflation
exactly when phi_pi is positive.
Part D: one worked point, and the neutral point where inflation is at target and the output gap is zero.
"""

from __future__ import annotations

import itertools
from fractions import Fraction

NATURAL_REAL_RATE = Fraction(1)
TARGET = Fraction(2)
PHI_PI = Fraction(3, 2)
PHI_Y = Fraction(1, 2)
INFLATION_GRID = (Fraction(1), Fraction(2), Fraction(3), Fraction(4), Fraction(5))
GAP_GRID = (Fraction(-2), Fraction(0), Fraction(2))
PHI_PI_GRID = (Fraction(0), Fraction(1, 2), Fraction(1), Fraction(3, 2))


def policy_rate(inflation: Fraction, output_gap: Fraction, phi_pi: Fraction, phi_y: Fraction) -> Fraction:
    """Nominal policy rate in percent per year: r^n + pi + phi_pi (pi - target) + phi_y y, all arguments in percent."""
    return NATURAL_REAL_RATE + inflation + phi_pi * (inflation - TARGET) + phi_y * output_gap


def real_policy_rate(inflation: Fraction, output_gap: Fraction, phi_pi: Fraction, phi_y: Fraction) -> Fraction:
    """Real policy rate in percent per year, the nominal rate minus inflation, which the rule sets to r^n + ..."""
    return policy_rate(inflation, output_gap, phi_pi, phi_y) - inflation


def main() -> None:
    """Print Parts A to D in a fixed order. Every line is an exact fraction or a fixed string."""
    print(f"parameters: natural_real_rate {NATURAL_REAL_RATE} target {TARGET} phi_pi {PHI_PI} phi_y {PHI_Y}")

    print("Part A: nominal policy rate i in percent per year, by inflation pi and output gap y")
    for y in GAP_GRID:
        cells = " ".join(f"pi_{p}={policy_rate(p, y, PHI_PI, PHI_Y)}" for p in INFLATION_GRID)
        print(f"output_gap {y}: {cells}")

    print("Part B: response to a one-point inflation gap at output gap 0")
    for phi in PHI_PI_GRID:
        nominal = policy_rate(TARGET + 1, Fraction(0), phi, PHI_Y) - policy_rate(TARGET, Fraction(0), phi, PHI_Y)
        real = real_policy_rate(TARGET + 1, Fraction(0), phi, PHI_Y) - real_policy_rate(TARGET, Fraction(0), phi, PHI_Y)
        print(
            f"phi_pi {phi} nominal_response {nominal} equals_one_plus_phi {nominal == 1 + phi} "
            f"real_response {real} equals_phi {real == phi}"
        )

    print("Part C: second differences in inflation at output gap 0, and the sign of the real response")
    values = [policy_rate(p, Fraction(0), PHI_PI, PHI_Y) for p in INFLATION_GRID]
    first = [b - a for a, b in itertools.pairwise(values)]
    second = [b - a for a, b in itertools.pairwise(first)]
    print("first_differences " + " ".join(str(d) for d in first))
    print("second_differences " + " ".join(str(d) for d in second))
    print(f"affine_in_inflation {all(d == 0 for d in second)}")
    for phi in PHI_PI_GRID:
        reals = [real_policy_rate(p, Fraction(0), phi, PHI_Y) for p in INFLATION_GRID]
        rising = all(b > a for a, b in itertools.pairwise(reals))
        print(f"phi_pi {phi} real_rate_rises_with_inflation {rising} matches_phi_positive {rising == (phi > 0)}")

    print("Part D: a worked point and the neutral point")
    worked = policy_rate(Fraction(3), Fraction(-1), PHI_PI, PHI_Y)
    print(f"worked pi 3 y -1: i {worked}")
    neutral = policy_rate(TARGET, Fraction(0), PHI_PI, PHI_Y)
    neutral_real = real_policy_rate(TARGET, Fraction(0), PHI_PI, PHI_Y)
    matches = neutral_real == NATURAL_REAL_RATE
    print(f"neutral pi 2 y 0: i {neutral} real {neutral_real} equals_natural_real_rate {matches}")


main()
