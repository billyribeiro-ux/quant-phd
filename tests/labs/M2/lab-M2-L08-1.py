"""M2 L08 lab 1: the Lagrange remainder of 1/(1 - x) at 0, checked at sampled points.

For f(x) = 1/(1 - x) and x0 = 0, the Taylor polynomial of degree n is P_n(x) = sum of x^k for k = 0..n, and the
remainder is R_n(x) = f(x) - P_n(x) = x^(n+1)/(1 - x) (Lesson 7, Proposition 2.3). Taylor's theorem with the Lagrange
form (Theorem 2.1 of this lesson) says R_n(x) = f^(n+1)(xi) x^(n+1) / (n+1)! for some xi strictly between 0 and x.
Here f^(n+1)(t) = (n+1)! / (1 - t)^(n+2), so the theorem asks for xi with (1 - xi)^(n+2) = 1 - x. The program computes
that xi in closed form, xi = 1 - (1 - x)^(1/(n+2)), and checks two things at each of the 133 (x, n) pairs: x = k/20
for k = 1..19 (19 values) and n = 0..6 (7 degrees), that 0 < xi < x, and that the Lagrange form evaluated at xi equals
the exact remainder. Part B checks the bound of Example 2.4 of this lesson (Corollary 2.2 with
M = (n+1)! 2^(n+2)) on [0, 1/2]: |R_n(x)| <= 2^(n+2) x^(n+1), at every sampled x in that interval. Part C prints a
few rows of the table. Standard library only; no randomness and no network access.
"""

from __future__ import annotations

import math
from math import factorial

N_VALUES = range(0, 7)
X_GRID = [k / 20 for k in range(1, 20)]


def derivative(k: int, t: float) -> float:
    """k-th derivative of 1/(1 - t): k! / (1 - t)^(k+1), for t < 1."""
    return factorial(k) / (1 - t) ** (k + 1)


def remainder_exact(x: float, n: int) -> float:
    """R_n(x) = x^(n+1) / (1 - x), the closed form of the remainder for 1/(1 - x) at 0."""
    return x ** (n + 1) / (1 - x)


def xi_for(x: float, n: int) -> float:
    """The point xi that Taylor's theorem asks for: the solution of (1 - xi)^(n+2) = 1 - x in (0, x)."""
    return float(1 - (1 - x) ** (1 / (n + 2)))


def lagrange_form(x: float, n: int, xi: float) -> float:
    """f^(n+1)(xi) x^(n+1) / (n+1)!, the Lagrange form of the remainder evaluated at xi."""
    return derivative(n + 1, xi) * x ** (n + 1) / factorial(n + 1)


def part_a() -> None:
    checks = 0
    for x in X_GRID:
        for n in N_VALUES:
            xi = xi_for(x, n)
            if not 0 < xi < x:
                raise AssertionError(f"xi is not strictly between 0 and x at x = {x}, n = {n}")
            if not math.isclose(lagrange_form(x, n, xi), remainder_exact(x, n), rel_tol=1e-9):
                raise AssertionError(f"Lagrange form differs from the exact remainder at x = {x}, n = {n}")
            checks += 1
    print(f"part A: {checks} (x, n) pairs (x = k/20, k = 1 to 19; n = 0 to 6): 0 < xi < x at every pair")
    print("part A: the Lagrange form at xi equals the exact remainder to relative error 1e-9 at every pair")


def part_b() -> None:
    checks = 0
    for x in X_GRID:
        if x > 0.5:
            continue
        for n in N_VALUES:
            bound = 2 ** (n + 2) * x ** (n + 1)
            if not remainder_exact(x, n) <= bound:
                raise AssertionError(f"Corollary bound fails at x = {x}, n = {n}")
            checks += 1
    print(f"part B: the bound |R_n(x)| <= 2^(n+2) x^(n+1) holds at all {checks} (x, n) pairs with 0 < x <= 1/2")


def part_c() -> None:
    print("part C: a sample of rows, with xi from the closed form")
    print("part C:     x     n        xi        R_n(x) exact    Lagrange form at xi")
    for x in (0.1, 0.3, 0.5, 0.9):
        for n in (1, 3, 5):
            xi = xi_for(x, n)
            print(
                f"part C: {x:5.2f} {n:4d}  {xi:10.6f}  {remainder_exact(x, n):14.8f}  {lagrange_form(x, n, xi):14.8f}"
            )


def main() -> None:
    part_a()
    part_b()
    part_c()


main()
