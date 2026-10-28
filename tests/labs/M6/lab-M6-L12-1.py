"""M6 L12 lab 1: dyadic martingales and a nonnegative martingale without L1 convergence.

Part A, the dyadic martingale. On [0, 1] with the length measure, let Y(x) = x. For n >= 0 the level-n cells are the
half-open intervals [j/2**n, (j+1)/2**n), with the last cell closed at 1. M_n is Y averaged over the level-n cell
that contains x, so M_n(x) is the midpoint c of that cell. The lab computes every integral exactly with
fractions.Fraction. The exact integral of (x - c)**2 over a cell [a, b] is ((b - c)**3 - (a - c)**3) / 3. It checks:
E[(M_n - Y)**2] = 1/(12 * 4**n) for n = 0, ..., 10; E[M_n**2] = 1/3 - 1/(12 * 4**n); E[Y**2] = 1/3; and the largest
value of |M_n(x) - x| over the grid j/4096, j = 0, ..., 4096, which is 1/2**(n+1) for each n.

Part B, a nonnegative martingale. A fair coin gives flips 1 (heads) or 0 (tails). M_n = 2**n when the first n flips
are all heads and M_n = 0 otherwise. The lab enumerates all coin sequences of length n <= 10 and checks the one-step
martingale identity on every atom of the first-n-flips partition, prints E[M_n] = 1 and P(M_n not equal to 0) = 2**(-n).

Every quantity is an exact Fraction. The lab uses no random draws, so every run prints the same lines.
"""

from __future__ import annotations

import itertools
from fractions import Fraction

MAX_LEVEL = 10
GRID_SIZE = 4096


def cell_index(x: Fraction, level: int) -> int:
    """The index j of the level-n cell [j/2**n, (j+1)/2**n) that contains x, with the last cell closed at 1."""
    cells: int = 2**level
    index: int = int(x * cells)
    return min(index, cells - 1)


def cell_midpoint(index: int, level: int) -> Fraction:
    """The midpoint c = (j + 1/2) / 2**n of the level-n cell with index j."""
    return Fraction(2 * index + 1, 2 ** (level + 1))


def part_a() -> None:
    """Exact moments and errors of the dyadic martingale M_n = E[Y | F_n] for Y(x) = x, for n from 0 to 10."""
    print("Part A: dyadic martingale M_n = E[Y | F_n] for Y(x) = x on [0, 1]")
    expected_y = Fraction(0)
    expected_y2 = Fraction(0)
    for j in range(2**MAX_LEVEL):
        a, b = Fraction(j, 2**MAX_LEVEL), Fraction(j + 1, 2**MAX_LEVEL)
        expected_y += (b * b - a * a) / 2
        expected_y2 += (b**3 - a**3) / 3
    print(f"E_Y {expected_y} E_Y_squared {expected_y2} E_Y_squared_is_one_third {expected_y2 == Fraction(1, 3)}")
    grid = [Fraction(j, GRID_SIZE) for j in range(GRID_SIZE + 1)]
    for level in range(MAX_LEVEL + 1):
        cells = 2**level
        error = Fraction(0)
        second_moment = Fraction(0)
        for j in range(cells):
            a, b = Fraction(j, cells), Fraction(j + 1, cells)
            c = cell_midpoint(j, level)
            error += ((b - c) ** 3 - (a - c) ** 3) / 3
            second_moment += c * c * (b - a)
        worst = max(abs(cell_midpoint(cell_index(x, level), level) - x) for x in grid)
        print(
            f"n {level} E_error_squared {error} formula_matches {error == Fraction(1, 12 * 4**level)} "
            f"E_M_squared_matches_one_third_minus {second_moment == Fraction(1, 3) - Fraction(1, 12 * 4**level)} "
            f"largest_grid_error {worst} equals_half_over_2_to_n {worst == Fraction(1, 2 ** (level + 1))}"
        )


def coin_value(flips: tuple[int, ...], level: int) -> int:
    """M_level for one coin sequence: 2**level if the first level flips are all heads, otherwise 0."""
    return 2**level if all(flips[:level]) else 0


def part_b() -> None:
    """A nonnegative martingale: E[M_n] = 1 for every n, yet M_n is 0 except on the all-heads path."""
    print("Part B: nonnegative martingale M_n = 2**n on all heads, 0 otherwise")
    every_step_holds = True
    for level in range(MAX_LEVEL):
        for prefix in itertools.product((0, 1), repeat=level):
            extensions = [(*prefix, flip) for flip in (0, 1)]
            average_next = Fraction(sum(coin_value(e, level + 1) for e in extensions), 2)
            every_step_holds = every_step_holds and average_next == coin_value(prefix, level)
    print(f"one_step_martingale_on_every_atom {every_step_holds}")
    for level in range(MAX_LEVEL + 1):
        sample = list(itertools.product((0, 1), repeat=level))
        expected = sum((Fraction(coin_value(s, level), 2**level) for s in sample), Fraction(0))
        nonzero = sum(1 for s in sample if coin_value(s, level) != 0)
        print(
            f"n {level} E_M_n {expected} P_M_n_nonzero {Fraction(nonzero, 2**level)} "
            f"is_two_to_minus_n {Fraction(nonzero, 2**level) == Fraction(1, 2**level)}"
        )


def main() -> None:
    """Print Part A and Part B."""
    part_a()
    part_b()


main()
