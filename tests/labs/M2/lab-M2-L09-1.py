"""M2 L09 lab 1: upper and lower Darboux sums for x^2 on [0, 1], and the bound for monotone integrands.

Part A takes f(x) = x^2 on [0, 1], which is nondecreasing, and the uniform partitions with n = 1, 2, 4, 8, 16, 32,
64, 128 subintervals. For a nondecreasing f the supremum on each subinterval is the value at its right endpoint and
the infimum is the value at its left endpoint, so U_n = sum of f(i/n)/n and L_n = sum of f((i-1)/n)/n. The program
checks in exact fractions that U_n - L_n = 1/n, that L_n <= 1/3 <= U_n, and that U_n - 1/3 = (3n+1)/(6n^2) and L_n -
1/3 = -(3n-1)/(6n^2). Part B takes a nonuniform partition with points (i/n)^2 and checks that U - L is at most the
mesh times f(1) - f(0). Part C takes the uniform partitions with n = 8, 16 and 32, with midpoint tags and
right-endpoint tags, and checks |R - 1/3| <= 1/n for each Riemann sum R. Exact fractions throughout; standard
library only; no randomness and no network access.
"""

from __future__ import annotations

from fractions import Fraction

N_VALUES = (1, 2, 4, 8, 16, 32, 64, 128)
TARGET = Fraction(1, 3)


def f(x: Fraction) -> Fraction:
    """f(x) = x^2, nondecreasing on [0, 1]."""
    return x * x


def upper_uniform(n: int) -> Fraction:
    """U_n for f on [0, 1] with n equal subintervals; the supremum on [(i-1)/n, i/n] is f(i/n)."""
    return sum((f(Fraction(i, n)) / n for i in range(1, n + 1)), Fraction(0))


def lower_uniform(n: int) -> Fraction:
    """L_n for f on [0, 1] with n equal subintervals; the infimum on [(i-1)/n, i/n] is f((i-1)/n)."""
    return sum((f(Fraction(i - 1, n)) / n for i in range(1, n + 1)), Fraction(0))


def part_a() -> None:
    print("part A: f(x) = x^2 on [0, 1], uniform partitions into n subintervals")
    print("part A:    n         L_n          U_n        U_n - L_n")
    for n in N_VALUES:
        lo, up = lower_uniform(n), upper_uniform(n)
        if up - lo != Fraction(1, n):
            raise AssertionError(f"U - L is not 1/n at n = {n}")
        if not lo <= TARGET <= up:
            raise AssertionError(f"the integral 1/3 is not between L and U at n = {n}")
        if up - TARGET != Fraction(3 * n + 1, 6 * n * n):
            raise AssertionError(f"U - 1/3 formula fails at n = {n}")
        if lo - TARGET != -Fraction(3 * n - 1, 6 * n * n):
            raise AssertionError(f"L - 1/3 formula fails at n = {n}")
        print(f"part A: {n:4d}  {float(lo):12.8f}  {float(up):12.8f}  {float(up - lo):12.8f}")
    print("part A: U - L = 1/n exactly, and L <= 1/3 <= U, at every n in the table")


def part_b() -> None:
    n = 10
    points = [Fraction(i * i, n * n) for i in range(n + 1)]
    points_are_x_squared = [Fraction(i, n) ** 2 for i in range(n + 1)]
    if points != points_are_x_squared:
        raise AssertionError("partition points are not (i/n)^2")
    widths = [points[i] - points[i - 1] for i in range(1, n + 1)]
    mesh = max(widths)
    upper = sum((f(points[i]) * widths[i - 1] for i in range(1, n + 1)), Fraction(0))
    lower = sum((f(points[i - 1]) * widths[i - 1] for i in range(1, n + 1)), Fraction(0))
    gap = upper - lower
    bound = mesh * (f(Fraction(1)) - f(Fraction(0)))
    if gap > bound:
        raise AssertionError("U - L exceeds the mesh bound for a monotone f")
    print(f"part B: nonuniform partition of [0, 1] with n = {n} subintervals and points (i/n)^2")
    print(f"part B: mesh = {float(mesh):.8f}, U - L = {float(gap):.8f}, bound mesh*(f(1)-f(0)) = {float(bound):.8f}")
    print("part B: U - L is at most the mesh bound, as the monotone argument predicts")


def part_c() -> None:
    print("part C: Riemann sums of x^2 on [0, 1], error against 1/3 and the bound 1/n")
    for n in (8, 16, 32):
        right = sum((f(Fraction(i, n)) / n for i in range(1, n + 1)), Fraction(0))
        midpoint = sum((f(Fraction(2 * i - 1, 2 * n)) / n for i in range(1, n + 1)), Fraction(0))
        for label, value in (("right", right), ("midpoint", midpoint)):
            error = value - TARGET
            if abs(error) > Fraction(1, n):
                raise AssertionError(f"{label} Riemann sum error exceeds 1/n at n = {n}")
            print(
                f"part C: n = {n:3d} {label:>8s}  error = {float(error):+.8f}  bound 1/n = {float(Fraction(1, n)):.8f}"
            )
    print("part C: every Riemann sum in the table lies within 1/n of 1/3")


def main() -> None:
    part_a()
    part_b()
    part_c()


main()
