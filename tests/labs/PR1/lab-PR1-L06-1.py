"""Lab 6: Robust optimization: worst-case returns over box uncertainty sets.

Illustrative inputs in exact Fraction arithmetic.
Computes worst-case expected portfolio returns across all 2^N = 4 vertices of a
rectangular uncertainty set |mu_i - mu_hat_i| <= epsilon_i, and compares the
minimum with the closed-form penalty identity mu_hat' w - epsilon' |w|.
"""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    # 2 assets with nominal returns mu_hat and box radii epsilon
    mu_hat = [Fraction(6, 100), Fraction(4, 100)]
    eps = [Fraction(1, 100), Fraction(2, 100)]

    # 4 vertices of the rectangular box
    vertices = [[mu_hat[0] + s0 * eps[0], mu_hat[1] + s1 * eps[1]] for s0 in (-1, 1) for s1 in (-1, 1)]

    # Case 1: Long-only portfolio w = (0.7, 0.3)
    w_long = [Fraction(7, 10), Fraction(3, 10)]
    vals_long = [v[0] * w_long[0] + v[1] * w_long[1] for v in vertices]
    min_vertex_long = min(vals_long)
    formula_long = sum(mu_hat[i] * w_long[i] - eps[i] * abs(w_long[i]) for i in range(2))

    # Case 2: Long-short portfolio w = (0.8, -0.2)
    w_ls = [Fraction(8, 10), Fraction(-2, 10)]
    vals_ls = [v[0] * w_ls[0] + v[1] * w_ls[1] for v in vertices]
    min_vertex_ls = min(vals_ls)
    formula_ls = sum(mu_hat[i] * w_ls[i] - eps[i] * abs(w_ls[i]) for i in range(2))

    print("Long-only vertex values:", [str(x) for x in vals_long])
    print(f"Long-only worst-case vertex: {min_vertex_long} | Formula: {formula_long}")
    print("Long-only exact match:", min_vertex_long == formula_long)

    print("Long-short vertex values:", [str(x) for x in vals_ls])
    print(f"Long-short worst-case vertex: {min_vertex_ls} | Formula: {formula_ls}")
    print("Long-short exact match:", min_vertex_ls == formula_ls)


main()
