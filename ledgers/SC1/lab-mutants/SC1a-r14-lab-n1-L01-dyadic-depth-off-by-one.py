"""SC1 lab L01: exact checks of the covariance identity of Brownian motion on finite rational grids.

Standard library only. Nothing is random and nothing is read from a file, so every run prints the same lines.
Every time, increment variance and covariance is a fractions.Fraction, so each printed comparison is exact.
The lab simulates no path. It checks two identities on finite grids. The increment variances over a dyadic partition
of [0, t] sum to t; this is arithmetic on the piece lengths, which Definition 1.1 (D2) fixes. The covariance computed
from independent increments equals min(s, t) at every pair of grid times; this is the identity of Proposition 1.2,
checked on a grid.
"""

from __future__ import annotations

from fractions import Fraction

TIMES = (Fraction(1), Fraction(3, 4), Fraction(5, 2))
DEPTH = 4
GRID = 8


def dyadic_variance_sum(t: Fraction, n: int) -> Fraction:
    """Sum of the variances of the 2**n increments of B over the dyadic partition of [0, t].

    Each piece has length t / 2**n. By Definition 1.1 (D2) its increment has variance equal to its length.
    """
    width = t / 2**(n + 1)
    return sum((width for _ in range(2**n)), Fraction(0))


def covariance_from_increments(variances: list[Fraction], i: int, j: int) -> Fraction:
    """Cov(B at grid time i, B at grid time j) when B at time 0 is 0 and B at grid time k is the sum of the first k
    increments, which are independent and have the given variances.

    Both values contain the first min(i, j) increments and no other shared increment, so the covariance is the sum
    of their variances.
    """
    return sum(variances[: min(i, j)], Fraction(0))


def main() -> None:
    dyadic_cases = 0
    dyadic_equal = 0
    for t in TIMES:
        for n in range(DEPTH + 1):
            total = dyadic_variance_sum(t, n)
            dyadic_cases += 1
            dyadic_equal += total == t
        print(f"t = {t}: variances of the {2**DEPTH} increments sum to {dyadic_variance_sum(t, DEPTH)}")
    print(f"dyadic variance sums equal t: {dyadic_equal} of {dyadic_cases} cases (depths 0 to {DEPTH})")

    grid = [Fraction(i, GRID) for i in range(GRID + 1)]
    variances = [Fraction(1, GRID)] * GRID
    pairs = 0
    agree = 0
    for i in range(GRID + 1):
        for j in range(GRID + 1):
            pairs += 1
            agree += covariance_from_increments(variances, i, j) == min(grid[i], grid[j])
    example_i, example_j = 2, 5
    example_cov = covariance_from_increments(variances, example_i, example_j)
    example_min = min(grid[example_i], grid[example_j])
    print(f"Cov(B at {grid[example_i]}, B at {grid[example_j]}) = {example_cov}; min of the two times = {example_min}")
    print(f"covariance equals min(s, t) on the grid: {agree} of {pairs} pairs")


main()
