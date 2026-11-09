"""M2 lab L06: the sign of the derivative of f(x) = x^3 - 3x against its monotone intervals, on an exact grid.

Standard library only. No randomness and no network. The derivative is f'(x) = 3x^2 - 3 = 3(x - 1)(x + 1), so f is
increasing on (-infinity, -1] and on [1, infinity), decreasing on [-1, 1], with a local maximum at -1 and a local
minimum at 1. The script uses exact rational numbers (fractions.Fraction) on the grid of x from -2 to 2 with step 1/4,
which has 16 intervals. It checks two things: the sign of f' at each grid point against the predicted sign, and the
direction of f on each grid interval against the sign of f' at its midpoint. It also prints the values f(-1) and f(1)
without a comparison. A grid is a finite check, and the monotone intervals are established on the page by the mean
value argument, under Assumption 2.1.
"""

from __future__ import annotations

import itertools
from fractions import Fraction


def f(x: Fraction) -> Fraction:
    """The cubic x^3 - 3x for a rational x."""
    return x**3 - 3 * x


def fprime(x: Fraction) -> Fraction:
    """The derivative 3x^2 - 3 of the cubic."""
    return 3 * x * x - 3


def predicted_sign(x: Fraction) -> int:
    """The sign of 3(x - 1)(x + 1) from the factored form: +1, 0 or -1."""
    value = 3 * (x - 1) * (x + 1)
    return (value > 0) - (value < 0)


def grid(lo: Fraction, hi: Fraction, step: Fraction) -> list[Fraction]:
    """The points lo, lo + step, ..., hi, for a positive step that divides hi - lo exactly."""
    if step <= 0 or (hi - lo) % step != 0:
        raise ValueError("the grid needs a positive step that divides hi - lo")
    count = int((hi - lo) / step)
    return [lo + i * step for i in range(count + 1)]


def main() -> None:
    points = grid(Fraction(-2), Fraction(2), Fraction(1, 4))
    signs_agree = all((fprime(x) > 0) - (fprime(x) < 0) == predicted_sign(x) for x in points)
    print(f"sign of f' agrees with 3(x - 1)(x + 1) at all {len(points)} grid points: {signs_agree}")
    increasing = 0
    agreements = 0
    for lo, hi in itertools.pairwise(points):
        rising = f(hi) > f(lo)
        increasing += rising
        midpoint = (lo + hi) / 2
        agreements += rising == (fprime(midpoint) > 0)
    intervals = len(points) - 1
    print(f"grid intervals on which f increases: {increasing} of {intervals}")
    print(f"increase agrees with the sign of f' at the midpoint on {agreements} of {intervals} intervals")
    print(f"f(-1) = {f(Fraction(-1))}; f(1) = {f(Fraction(1))}")


main()
