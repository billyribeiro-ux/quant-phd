"""Rung 2 completed solution: the matched factor of a Student-t draw and the index of the 99% loss.

Standard library only. The two functions are the completion problem's blanks. The inputs are whole numbers; no data
is read. Every printed value is exact, or a float printed to six decimals.
"""

import math
from fractions import Fraction


def matched_factor(nu: int) -> float:
    """The matched scale (nu - 2) / nu of a Student-t draw, for nu greater than 2."""
    if nu <= 2:
        raise ValueError("nu must be greater than 2")
    return (nu - 2) / nu


def quantile_index(n: int) -> int:
    """The 1-based index ceil(0.99 n) of the 99% loss among n losses, in exact integers."""
    if n < 1:
        raise ValueError("n must be 1 or more")
    return (99 * n + 99) // 100


def main() -> None:
    print("matched factor for nu = 5:", f"{matched_factor(5):.6f}")
    print("matched factor for nu = 3:", f"{matched_factor(3):.6f}")
    print("index for n = 20000:", quantile_index(20_000))
    print("index for n = 101:", quantile_index(101))
    exact = math.ceil(Fraction(99, 100) * 101)
    print("exact check, n = 101:", exact == quantile_index(101))


main()
