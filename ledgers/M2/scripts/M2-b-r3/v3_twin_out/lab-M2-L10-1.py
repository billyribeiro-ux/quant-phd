"""M2 L10 lab 1: the integral of a derivative recovers the increment, checked by Darboux sums.

Part A takes F(x) = x^3 - 2x on [0, 1], so f = F' = 3x^2 - 2, which is nondecreasing on [0, 1]. For uniform
partitions into n parts, the upper and lower sums of f bracket F(1) - F(0) = -1, and U_n - L_n = 3/n exactly. Part B
takes F(x) = x/(1 + x) on [0, 1], so f = F' = 1/(1 + x)^2, which is nonincreasing; its increment is
F(1) - F(0) = 1/2 and U_n - L_n = 3/(4n) exactly. Part C checks by a central difference, in floating point, that
F'(0.3) = f(0.3) for the function of Part B. Exact fractions are used in Parts A and B; standard library only; no
randomness and no network access.
"""

from __future__ import annotations

from fractions import Fraction

N_VALUES = (1, 2, 4, 8, 16, 32, 64, 128, 256)
N_VALUES_B = (1, 2, 4, 8, 16, 32, 64, 128)


def fa(x: Fraction) -> Fraction:
    """f = F' for F(x) = x^3 - 2x, namely 3x^2 - 2."""
    return 3 * x * x - 2


def antider_a(x: Fraction) -> Fraction:
    """F(x) = x^3 - 2x."""
    return x**3 - 2 * x


def fb(x: Fraction) -> Fraction:
    """f = F' for F(x) = x/(1 + x), namely 1/(1 + x)^2."""
    return 1 / (1 + x) ** 2


def antider_b(x: Fraction) -> Fraction:
    """F(x) = x/(1 + x)."""
    return x / (1 + x)


def part_a() -> None:
    target = antider_a(Fraction(1)) - antider_a(Fraction(0))
    print(f"part A: F(x) = x^3 - 2x, F(1) - F(0) = {target}; f = 3x^2 - 2 is nondecreasing on [0, 1]")
    print("part A:    n         L_n          U_n        U_n - L_n")
    for n in N_VALUES:
        upper = sum((fa(Fraction(i, n)) / n for i in range(1, n + 1)), Fraction(0))
        lower = sum((fa(Fraction(i - 1, n)) / n for i in range(1, n + 1)), Fraction(0))
        if not lower <= target <= upper:
            raise AssertionError(f"F(1) - F(0) is not between L and U at n = {n}")
        if upper - lower != Fraction(3, n):
            raise AssertionError(f"U - L is not 3/n at n = {n}")
        print(f"part A: {n:4d}  {float(lower):12.8f}  {float(upper):12.8f}  {float(upper - lower):12.8f}")
    print("part A: F(1) - F(0) = -1 lies between L_n and U_n at every n, and U_n - L_n = 3/n exactly")


def part_b() -> None:
    target = antider_b(Fraction(1)) - antider_b(Fraction(0))
    print(f"part B: F(x) = x/(1 + x), F(1) - F(0) = {target}; f = 1/(1 + x)^2 is nonincreasing on [0, 1]")
    print("part B:    n         L_n          U_n        U_n - L_n")
    for n in N_VALUES_B:
        upper = sum((fb(Fraction(i - 1, n)) / n for i in range(1, n + 1)), Fraction(0))
        lower = sum((fb(Fraction(i, n)) / n for i in range(1, n + 1)), Fraction(0))
        if not lower <= target <= upper:
            raise AssertionError(f"F(1) - F(0) is not between L and U at n = {n}")
        if upper - lower != Fraction(3, 4 * n):
            raise AssertionError(f"U - L is not 3/(4n) at n = {n}")
        print(f"part B: {n:4d}  {float(lower):12.8f}  {float(upper):12.8f}  {float(upper - lower):12.8f}")
    print("part B: F(1) - F(0) = 1/2 lies between L_n and U_n at every n, and U_n - L_n = 3/(4n) exactly")


def part_c() -> None:
    x = 0.3
    h = 1e-6
    central = ((x + h) / (1 + x + h) - (x - h) / (1 + x - h)) / (2 * h)
    exact = 1 / (1 + x) ** 2
    error = abs(central - exact)
    if error > 1e-7:
        raise AssertionError(f"central difference of F disagrees with f at x = {x}: error {error}")
    print(f"part C: central difference of F at x = 0.3 with h = 1e-6 is {central:.8f}")
    print(f"part C: f(0.3) = 1/(1.3)^2 = {exact:.8f}")
    print(f"part C: absolute difference below 1e-7: {error < 1e-7}")


def main() -> None:
    part_a()
    part_b()
    part_c()


main()
