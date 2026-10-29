"""M2 lab L03: one-sided limits of a piecewise function at its break, and an epsilon-delta check.

Standard library only. No randomness and no network. The piecewise function is f(x) = x^2 for x < 1 and
f(x) = 2x for x >= 1. Its left-hand values tend to 1 and its right-hand values tend to 2 as x tends to 1, so the
two-sided limit at 1 does not exist. Each value is an exact rational number (fractions.Fraction). The second part
checks, on a finite grid of points x with 0 < |x - 2| < delta, that delta = epsilon/3 gives |g(x) - 7| < epsilon
for g(x) = 3x + 1 (limit 7 at x = 2), for three values of epsilon. The grid is a finite check of one choice
of delta. The epsilon-delta proof on the page covers every x.
"""

from __future__ import annotations

from fractions import Fraction

BREAK = Fraction(1)


def f(x: Fraction) -> Fraction:
    """The piecewise function: x^2 when x < 1, and 2x when x >= 1. Exact for a rational x."""
    return x * x if x < BREAK else 2 * x


def g(x: Fraction) -> Fraction:
    """The linear function 3x + 1, whose limit at 2 is 7."""
    return 3 * x + 1


def grid_points(centre: Fraction, radius: Fraction) -> list[Fraction]:
    """Points centre + (k/20) * radius for k from -19 to 19, k != 0. Each satisfies 0 < |x - centre| < radius."""
    return [centre + Fraction(k, 20) * radius for k in range(-19, 20) if k != 0]


def delta_works(epsilon: Fraction) -> bool:
    """True when every grid point with 0 < |x - 2| < epsilon/3 has |g(x) - 7| < epsilon."""
    delta = epsilon / 3
    return all(abs(g(x) - 7) < epsilon for x in grid_points(Fraction(2), delta))


def main() -> None:
    print("h, f(1 - h), f(1 + h), gap f(1 + h) - f(1 - h)")
    for k in range(1, 5):
        h = Fraction(1, 10**k)
        left, right = f(BREAK - h), f(BREAK + h)
        print(f"{float(h):g}, {float(left):.6f}, {float(right):.6f}, {float(right - left):.6f}")
    for epsilon in (Fraction(1, 10), Fraction(1, 100), Fraction(1, 1000)):
        print(f"epsilon {float(epsilon):g}: delta = epsilon/3 works on the grid: {delta_works(epsilon)}")


main()
