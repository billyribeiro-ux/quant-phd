"""M2 L12 lab 1: truncated integrals against their improper limits, and the divergence of the integral of 1/x.

Part A uses f(x) = 1/x^2 on [1, infinity). The truncated integral from 1 to b equals 1 - 1/b exactly, by the
antiderivative F(x) = -1/x, so its error against the improper value 1 is exactly 1/b, and b times that error is
1 for every b in the table. Part B uses f(x) = 1/x^3, whose truncated integral is (1 - 1/b^2)/2, with error
1/(2 b^2), so b^2 times the error is 1/2. Part C takes f(x) = 1/x on [1, N] with the uniform partition into
unit steps. Since f is decreasing, the infimum on [k, k+1] is 1/(k+1), so the lower sum is H_N - 1, where H_N is
the N-th harmonic number. For N = 2^m the program checks H_N - 1 >= m/2, which shows the lower sums are unbounded.
Parts A and B use exact fractions; Part C uses floating point for the harmonic sums. Standard library only; no
randomness and no network access.
"""

from __future__ import annotations

from fractions import Fraction

B_VALUES_A = (10, 100, 1000, 10000)
B_VALUES_B = (10, 100, 1000)
M_VALUES_C = tuple(range(1, 15))
M_DISPLAY_C = (1, 4, 8, 12, 14)


def part_a() -> None:
    print("part A: f(x) = 1/x^2, truncated integral from 1 to b, improper value 1")
    print("part A:       b       truncated value     error      b * error")
    for b in B_VALUES_A:
        value = (-Fraction(1, b)) - (-Fraction(1))
        error = Fraction(1) - value
        if error != Fraction(1, b):
            raise AssertionError(f"error is not 1/b at b = {b}")
        if b * error != 1:
            raise AssertionError(f"b * error is not 1 at b = {b}")
        print(f"part A: {b:8d}   {float(value):16.10f}  {float(error):12.10f}  {float(b * error):8.4f}")
    print("part A: the error is exactly 1/b, so b times the error is 1 at every b in the table")


def part_b() -> None:
    print("part B: f(x) = 1/x^3, truncated integral from 1 to b, improper value 1/2")
    print("part B:       b       truncated value     error      b^2 * error")
    for b in B_VALUES_B:
        value = (-Fraction(1, 2 * b * b)) - (-Fraction(1, 2))
        error = Fraction(1, 2) - value
        if error != Fraction(1, 2 * b * b):
            raise AssertionError(f"error is not 1/(2 b^2) at b = {b}")
        if b * b * error != Fraction(1, 2):
            raise AssertionError(f"b^2 * error is not 1/2 at b = {b}")
        print(f"part B: {b:8d}   {float(value):16.10f}  {float(error):12.10f}  {float(b * b * error):8.4f}")
    print("part B: the error is exactly 1/(2 b^2), so b^2 times the error is 1/2 at every b in the table")


def part_c() -> None:
    print("part C: f(x) = 1/x on [1, N], unit steps, lower sum H_N - 1 (floating point)")
    print("part C:      N = 2^m       H_N - 1      m / 2     H_N - 1 >= m/2")
    harmonic = 0.0
    n = 1
    for m in M_VALUES_C:
        while n < 2**m:
            n += 1
            harmonic += 1.0 / n
        lower = harmonic
        if lower < m / 2:
            raise AssertionError(f"H_N - 1 is below m/2 at N = 2^{m}")
        if m in M_DISPLAY_C:
            print(f"part C: {2**m:10d}  {lower:12.8f}  {m / 2:9.4f}     True")
    print("part C: the bound H_N - 1 >= m/2 holds for m = 1 to 14; the bound m/2 grows without limit (Theorem 3.3)")


def main() -> None:
    part_a()
    part_b()
    part_c()


main()
