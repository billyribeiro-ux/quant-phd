"""Lab M8-L04-1: Cholesky decomposition and finite difference step-size trade-off.

Standard library only. Demonstrates exact Cholesky factorization in Fraction
and the truncation-roundoff error balance in forward finite differences.
"""

from __future__ import annotations

import math
from fractions import Fraction


def cholesky_3x3_fraction(a: list[list[Fraction]]) -> list[list[Fraction]]:
    """Compute Cholesky factor L for 3x3 SPD matrix in exact arithmetic."""
    l_mat: list[list[Fraction]] = [[Fraction(0) for _ in range(3)] for _ in range(3)]

    # Row 0
    # L00 = sqrt(A00)
    l00_sq = a[0][0]
    # For our chosen test matrix, l00_sq is a perfect square of a rational
    l00 = Fraction(math.isqrt(l00_sq.numerator), math.isqrt(l00_sq.denominator))
    l_mat[0][0] = l00
    l_mat[1][0] = a[1][0] / l00
    l_mat[2][0] = a[2][0] / l00

    # Row 1
    l11_sq = a[1][1] - l_mat[1][0] ** 2
    l11 = Fraction(math.isqrt(l11_sq.numerator), math.isqrt(l11_sq.denominator))
    l_mat[1][1] = l11
    l_mat[2][1] = (a[2][1] - l_mat[2][0] * l_mat[1][0]) / l11

    # Row 2
    l22_sq = a[2][2] - l_mat[2][0] ** 2 - l_mat[2][1] ** 2
    l22 = Fraction(math.isqrt(l22_sq.numerator), math.isqrt(l22_sq.denominator))
    l_mat[2][2] = l22

    return l_mat


def matmul_3x3_fraction(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    """Matrix multiplication in Fraction."""
    res: list[list[Fraction]] = [[Fraction(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            res[i][j] = sum((a[i][k] * b[k][j] for k in range(3)), Fraction(0))
    return res


def transpose_3x3_fraction(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[a[j][i] for j in range(3)] for i in range(3)]


def main() -> None:
    print("=== Part A: Cholesky Decomposition of 3x3 SPD Matrix ===")
    # A = [[4, 2, -2], [2, 10, 2], [-2, 2, 6]]
    a_frac = [
        [Fraction(4), Fraction(2), Fraction(-2)],
        [Fraction(2), Fraction(10), Fraction(2)],
        [Fraction(-2), Fraction(2), Fraction(6)],
    ]
    l_frac = cholesky_3x3_fraction(a_frac)
    lt_frac = transpose_3x3_fraction(l_frac)
    reconstructed = matmul_3x3_fraction(l_frac, lt_frac)

    print("Matrix A:")
    for row in a_frac:
        print("  ", [str(x) for x in row])
    print("Cholesky factor L (exact Fraction):")
    for row in l_frac:
        print("  ", [str(x) for x in row])
    print("L * L^T matches A exactly:", reconstructed == a_frac)

    print("\n=== Part B: Forward Difference Step-Size Trade-off on d/dx exp(x) at x=1 ===")
    x0 = 1.0
    true_deriv = math.exp(x0)
    u = 2.0 ** (-53)  # unit roundoff for binary64
    print(f"True derivative exp(1): {true_deriv:.16f}")
    print(f"Machine unit roundoff u: {u:.2e}")
    print(f"Theoretical optimal step h* ~ sqrt(2*u): {math.sqrt(2.0 * u):.2e}")
    print(" k    Step h       FD Approximation       Absolute Error   Dominant Reg.")

    for k in range(1, 17):
        h = 10.0 ** (-k)
        fd_approx = (math.exp(x0 + h) - math.exp(x0)) / h
        err = abs(fd_approx - true_deriv)
        regime = "Truncation" if k < 8 else ("Optimal" if k == 8 else "Roundoff")
        print(f"{k:2d}   {h:.1e}   {fd_approx:.16f}   {err:.2e}   {regime}")


main()
