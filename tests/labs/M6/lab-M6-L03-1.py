"""M6 lab L03: the integral of simple functions with the length measure, and dyadic lower sums for x squared.

Part A is exact. A simple function is given as a list of pieces, each a Fraction length and a value on that piece;
its integral is the sum of value times length, computed in Fraction arithmetic.

Part B is numerical. It uses floating-point arithmetic and prints 10 decimals. It computes the integral of the
dyadic simple function floor(2^n x^2) / 2^n on [0, 1] in closed form for each level set, and compares 1/3 minus that
integral with the bound 2^(-n). The bound is proved on the page; the value 1/3 is the calculus value of the
integral of x^2, and this lab reads it off numerically. The output is therefore labelled numerical.

Standard library only. Nothing is random and nothing is read from a file.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import pairwise
from math import sqrt

Piece = tuple[Fraction, Fraction]


def simple_integral(pieces: list[Piece]) -> Fraction:
    """The integral of a simple function given by (length, value) pieces: the sum of value times length.

    A piece of length 0 is a single point and contributes nothing. Raises ValueError for a negative length.
    """
    if any(length < 0 for length, _ in pieces):
        raise ValueError("piece lengths must be non-negative")
    return sum((length * value for length, value in pieces), Fraction(0))


def dyadic_integral(n: int) -> float:
    """The integral over [0, 1] of floor(2^n x^2) / 2^n, using the length of each level set.

    For k from 0 to 2^n - 1, the level set where floor(2^n x^2) = k is the interval from sqrt(k / 2^n) up to
    sqrt((k + 1) / 2^n), whose length is sqrt((k + 1) / 2^n) - sqrt(k / 2^n). The level 2^n is the single point
    x = 1, of length 0. Raises ValueError when n is negative.
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    scale = 2**n
    total = 0.0
    for k in range(scale):
        total += (k / scale) * (sqrt((k + 1) / scale) - sqrt(k / scale))
    return total


def main() -> None:
    third_quarter = Fraction(3, 4)
    print("Part A (exact): values 0 on [0, 1/2), 1 on [1/2, 3/4), 3 on [3/4, 1]")
    base = [
        (Fraction(1, 2), Fraction(0)),
        (third_quarter - Fraction(1, 2), Fraction(1)),
        (Fraction(1) - third_quarter, Fraction(3)),
    ]
    print(f"integral = {simple_integral(base)}")
    moved_point = [
        (Fraction(1, 2), Fraction(0)),
        (Fraction(0), Fraction(5)),
        (third_quarter - Fraction(1, 2), Fraction(1)),
        (Fraction(1) - third_quarter, Fraction(3)),
    ]
    print(f"step function plus a point at 1/2 of value 5 (length 0): integral = {simple_integral(moved_point)}")

    print("Part B (numerical, 10 decimals): dyadic lower sums of x^2 on [0, 1]")
    values: list[float] = []
    for n in range(1, 11):
        integral = dyadic_integral(n)
        values.append(integral)
        error = 1 / 3 - integral
        bound = 2.0**-n
        print(
            f"n {n:2d}  I_n {integral:.10f}  1/3 - I_n {error:.10f}  2^(-n) {bound:.10f}  "
            f"0 <= error <= 2^(-n): {0 <= error <= bound}"
        )
    nondecreasing = all(a <= b for a, b in pairwise(values))
    print(f"I_n is nondecreasing for n from 1 to 10: {nondecreasing}")


main()
