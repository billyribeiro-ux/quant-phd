"""M5 L06 lab 1: bisection for a convergent subsequence, grid maxima, and unit vectors in the sup distance.

Standard library only. No randomness and no network: the sequence is a fixed formula, every grid is enumerated, and
all arithmetic is exact with Fraction, so every run prints the same lines.

Part A: the bisection construction of Bolzano-Weierstrass, run on a finite prefix. The prefix is the first 4096 terms
of x_n = (n^2 mod 1000)/1000 in [0, 1). At each of 8 steps the current interval is halved, and the half that contains
more of the remaining prefix indices inside the current interval is kept. The output gives each interval, the chosen
index, and whether every chosen value from step j on lies in the interval of step j. A finite prefix is not
an infinite sequence, so this illustrates the construction and proves nothing about the infinite sequence.
Part B: f(x) = x(1 - x) on two grids of [0, 1]: k/10 (which contains 1/2, where f is largest) and k/7 (which does
not contain 1/2). The grid maxima are exact, and the printed values show that a grid maximum is a lower bound for
the true maximum 1/4.
Part C: the unit vectors e_0, ..., e_9 truncated to length 20 in the sup distance. Every pair of distinct vectors
has distance exactly 1. The output reports the minimum and maximum pairwise distance over all 45 pairs.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

PREFIX = 4096
STEPS = 8
TRUNCATION = 20
VECTORS = 10


def term(n: int) -> Fraction:
    """The n-th term of the prefix, (n^2 mod 1000)/1000, an exact fraction in [0, 1)."""
    return Fraction(n * n % 1000, 1000)


def unit_vector(index: int, length: int) -> tuple[Fraction, ...]:
    """The vector with a 1 in position index and zeros elsewhere, of the given length."""
    return tuple(Fraction(1) if k == index else Fraction(0) for k in range(length))


def sup_distance(f: tuple[Fraction, ...], g: tuple[Fraction, ...]) -> Fraction:
    """The maximum over positions of |f_k - g_k|, exact. Both vectors have the same length."""
    return max(abs(a - b) for a, b in zip(f, g, strict=True))


def bisect_prefix() -> None:
    """Halve [0, 1] for STEPS steps and print each step.

    At each step the pool is the set of prefix indices after the last chosen index whose terms lie in the current
    interval. The half of the interval that holds more pool indices is kept, and the first pool index in it is chosen.
    """
    values = [term(n) for n in range(1, PREFIX + 1)]
    left, right = Fraction(0), Fraction(1)
    last_index = 0
    chosen: list[tuple[int, Fraction]] = []
    intervals: list[tuple[Fraction, Fraction]] = []
    for step in range(1, STEPS + 1):
        mid = (left + right) / 2
        pool = [n for n in range(last_index + 1, PREFIX + 1) if left <= values[n - 1] <= right]
        in_left = [n for n in pool if values[n - 1] < mid]
        in_right = [n for n in pool if values[n - 1] >= mid]
        if len(in_left) >= len(in_right):
            right = mid
            half = in_left
        else:
            left = mid
            half = in_right
        index = half[0]
        last_index = index
        chosen.append((index, values[index - 1]))
        intervals.append((left, right))
        print(f"step {step} interval [{left}, {right}] width {right - left} chosen_index {index}")
    nested = all(intervals[j][0] <= value <= intervals[j][1] for j in range(STEPS) for _, value in chosen[j:])
    print(f"tail_values_in_their_interval {nested}")
    print(f"subsequence_indices {' '.join(str(index) for index, _ in chosen)}")


def grid_maximum(grid: list[Fraction]) -> tuple[Fraction, Fraction]:
    """The maximum of f(x) = x(1 - x) over the grid, and the first grid point that attains it."""
    best = max(x * (1 - x) for x in grid)
    point = next(x for x in grid if x * (1 - x) == best)
    return point, best


def main() -> None:
    """Print Parts A, B and C. Every value is an exact fraction, an integer, or a boolean."""
    print("Part A: bisection on a prefix of 4096 terms of (n^2 mod 1000)/1000, on [0, 1]")
    bisect_prefix()

    print("Part B: maximum of x(1 - x) on grids of [0, 1]; the true maximum is 1/4 at x = 1/2")
    fine = [Fraction(k, 10) for k in range(11)]
    point, value = grid_maximum(fine)
    print(f"grid_tenths argmax {point} maximum {value} true_maximum {Fraction(1, 4)}")
    coarse = [Fraction(k, 7) for k in range(8)]
    point, value = grid_maximum(coarse)
    print(f"grid_sevenths argmax {point} maximum {value} lower_bound_for_true {value <= Fraction(1, 4)}")

    print("Part C: unit vectors e_0 to e_9 of length 20, sup distance between distinct vectors")
    vectors = [unit_vector(i, TRUNCATION) for i in range(VECTORS)]
    distances = [sup_distance(f, g) for f, g in combinations(vectors, 2)]
    print(f"pairs {len(distances)} min_distance {min(distances)} max_distance {max(distances)}")
    print(f"self_distance {sup_distance(vectors[0], vectors[0])}")


main()
