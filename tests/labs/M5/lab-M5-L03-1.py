"""M5 lab L03: an epsilon-delta check for f(x) = x * x at x0 = 2, on an exact grid.

Standard library only. No randomness and no network. The grid is x = 2 + k/200 for integers k with
|k| <= 200, so every grid point satisfies |x - 2| <= 1, the range in which the page proves the bound
|x * x - 4| <= 5 |x - 2|. All comparisons use fractions.Fraction, so each printed count is exact.
The lab checks the bound and the choice delta = min(1, eps / 5) on this grid only. A grid check is
evidence about the grid. The page's proof covers every x with |x - 2| <= 1.
"""

from __future__ import annotations

from fractions import Fraction

X0 = Fraction(2)
K_MAX = 200
EPS = Fraction(1, 10)


def f(x: Fraction) -> Fraction:
    """The function f(x) = x * x."""
    return x * x


def grid() -> list[Fraction]:
    """The points x = 2 + k/200 for integers k with -200 <= k <= 200, in increasing order."""
    return [X0 + Fraction(k, K_MAX) for k in range(-K_MAX, K_MAX + 1)]


def delta_for(eps: Fraction) -> Fraction:
    """The delta the page proves works for eps: min(1, eps / 5)."""
    return min(Fraction(1), eps / 5)


def main() -> None:
    points = grid()
    bound_holds = sum(abs(f(x) - 4) <= 5 * abs(x - X0) for x in points)
    print(f"bound |x*x - 4| <= 5|x - 2| on the grid: holds at {bound_holds} of {len(points)} points")

    delta = delta_for(EPS)
    inside = [x for x in points if abs(x - X0) < delta]
    good = sum(abs(f(x) - 4) < EPS for x in inside)
    print(f"delta = {delta}: points with |x - 2| < delta: {len(inside)}")
    print(f"of those, points with |x*x - 4| < 1/10: {good} of {len(inside)}")

    too_large = Fraction(1, 10)
    failing = [x for x in points if abs(x - X0) < too_large and abs(f(x) - 4) >= EPS]
    first = failing[0]
    print(f"delta = {too_large} fails: first failing grid point x = {first}, with |x*x - 4| = {abs(f(first) - 4)}")
    print(f"grid points with |x - 2| < {too_large} and |x*x - 4| >= 1/10: {len(failing)}")


main()
