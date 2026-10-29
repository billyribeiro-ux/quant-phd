"""M2 lab L02: the limit laws for sums, products and quotients, checked term by term on a grid of n.

Standard library only. No randomness and no network. Two sequences are used: a_n = (2n + 1)/(n + 1), with limit 2,
and b_n = (n + 2)/n, with limit 1. Every term and every error is an exact rational number (fractions.Fraction).
The script checks the closed forms of the exact errors against the terms, and the triangle inequality for the sum,
at n = 1, 10, 100, 1000 and 10000 only. The limit laws themselves are proved on the page for every n. The grid
is a finite check of the closed forms, and it says nothing about other n.
"""

from __future__ import annotations

from fractions import Fraction

GRID = (1, 10, 100, 1000, 10000)


def a(n: int) -> Fraction:
    """The term a_n = (2n + 1)/(n + 1), with limit 2, for an integer n >= 1."""
    if n < 1:
        raise ValueError(f"a needs n >= 1, got {n}")
    return Fraction(2 * n + 1, n + 1)


def b(n: int) -> Fraction:
    """The term b_n = (n + 2)/n, with limit 1, for an integer n >= 1. Never zero."""
    if n < 1:
        raise ValueError(f"b needs n >= 1, got {n}")
    return Fraction(n + 2, n)


def sum_error(n: int) -> Fraction:
    """The exact distance |(a_n + b_n) - 3| from the sum to its limit 3."""
    return abs(a(n) + b(n) - 3)


def product_error(n: int) -> Fraction:
    """The exact distance |a_n b_n - 2| from the product to its limit 2 (the product of limits 2 and 1)."""
    return abs(a(n) * b(n) - 2)


def quotient_error(n: int) -> Fraction:
    """The exact distance |a_n / b_n - 2| from the quotient to its limit 2 (the quotient of limits 2 and 1)."""
    return abs(a(n) / b(n) - 2)


def closed_forms_hold(n: int) -> bool:
    """True when the three errors equal the closed forms (n+2)/(n(n+1)), (3n+2)/(n(n+1)) and (5n+4)/((n+1)(n+2))."""
    return (
        sum_error(n) == Fraction(n + 2, n * (n + 1))
        and product_error(n) == Fraction(3 * n + 2, n * (n + 1))
        and quotient_error(n) == Fraction(5 * n + 4, (n + 1) * (n + 2))
    )


def main() -> None:
    print("n, sum error, product error, quotient error")
    for n in GRID:
        print(f"{n}, {float(sum_error(n)):.6e}, {float(product_error(n)):.6e}, {float(quotient_error(n)):.6e}")
    print(f"closed forms match the exact errors at every grid n: {all(closed_forms_hold(n) for n in GRID)}")
    triangle = all(sum_error(n) <= abs(a(n) - 2) + abs(b(n) - 1) for n in GRID)
    print(f"sum error at most |a_n - 2| + |b_n - 1| at every grid n: {triangle}")


main()
