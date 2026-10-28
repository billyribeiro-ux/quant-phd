"""M2 lab L20: a double integral over a rectangle, by iterated midpoint sums in both orders.

SIMULATED: the integrand f(x, y) = x * y + x**2 on the rectangle [0, 1] x [0, 2] is a test function chosen for
this lab. It is not market data.
The lab uses exact rational arithmetic (fractions.Fraction), so every printed value is exact. For each n it
computes the iterated midpoint sum with n cells in each direction, once with x as the outer variable and once with
y as the outer variable, and compares each sum with the exact integral 5/3 and with the predicted error -1/(6 n**2).
The lab checks the two orders numerically on this one integrand. It does not invoke any theorem that equates
iterated integrals, and it makes no claim about other integrands.
Standard library only; no randomness and no network access.
"""

from __future__ import annotations

from fractions import Fraction

X_LO, X_HI = Fraction(0), Fraction(1)
Y_LO, Y_HI = Fraction(0), Fraction(2)
EXACT = Fraction(5, 3)


def integrand(x: Fraction, y: Fraction) -> Fraction:
    """f(x, y) = x * y + x**2, evaluated exactly."""
    return x * y + x * x


def midpoints(lo: Fraction, hi: Fraction, n: int) -> list[Fraction]:
    """The n midpoints of the n equal cells of [lo, hi]. A cell count below 1 raises ValueError."""
    if n < 1:
        raise ValueError(f"the cell count must be at least 1, got {n}")
    width = (hi - lo) / n
    return [lo + (i + Fraction(1, 2)) * width for i in range(n)]


def sum_x_outer(n: int) -> Fraction:
    """Iterated midpoint sum with x outer: the outer sum over x-midpoints of the inner sum over y-midpoints."""
    dx = (X_HI - X_LO) / n
    dy = (Y_HI - Y_LO) / n
    total = Fraction(0)
    for x in midpoints(X_LO, X_HI, n):
        inner = sum((integrand(x, y) * dy for y in midpoints(Y_LO, Y_HI, n)), Fraction(0))
        total += inner * dx
    return total


def sum_y_outer(n: int) -> Fraction:
    """Iterated midpoint sum with y outer: the outer sum over y-midpoints of the inner sum over x-midpoints."""
    dx = (X_HI - X_LO) / n
    dy = (Y_HI - Y_LO) / n
    total = Fraction(0)
    for y in midpoints(Y_LO, Y_HI, n):
        inner = sum((integrand(x, y) * dx for x in midpoints(X_LO, X_HI, n)), Fraction(0))
        total += inner * dy
    return total


def sum_of_odd_squares_identity(limit: int) -> bool:
    """True when 1**2 + 3**2 + ... + (2n-1)**2 equals n * (4 n**2 - 1) / 3 for every n from 1 to limit."""
    for n in range(1, limit + 1):
        odd_sum = sum((2 * i + 1) ** 2 for i in range(n))
        if 3 * odd_sum != n * (4 * n * n - 1):
            return False
    return True


def main() -> None:
    print("integrand f(x, y) = x*y + x**2 on [0, 1] x [0, 2]; exact integral 5/3")
    for n in (1, 2, 4, 8, 16, 32):
        sx = sum_x_outer(n)
        sy = sum_y_outer(n)
        error_x = sx - EXACT
        error_y = sy - EXACT
        predicted = Fraction(-1, 6 * n * n)
        match = error_x == predicted and error_y == predicted
        print(
            f"n = {n:>2}: x outer {sx}, error {error_x}; y outer {sy}, error {error_y}; "
            f"predicted error -1/(6 n^2) = {predicted}; match {match}"
        )
    print(f"sum of odd squares identity for n from 1 to 50: {sum_of_odd_squares_identity(50)}")


main()
