"""Lab AP2-L01-1: Exact Global Minimum-Variance portfolio and efficient frontier.

Hypothetical parameters (3 assets), not real data.
Computes w_GMV and two frontier portfolios in exact Fraction arithmetic,
verifying budget sum(w) = 1, target return matching, and variance formulas.
"""

from __future__ import annotations

from fractions import Fraction


def invert_3x3(mat: list[list[Fraction]]) -> list[list[Fraction]]:
    """Invert 3x3 matrix using exact row elimination."""
    n = 3
    aug = [[mat[i][j] for j in range(n)] + [Fraction(1 if i == k else 0) for k in range(n)] for i in range(n)]
    for i in range(n):
        p = aug[i][i]
        for j in range(2 * n):
            aug[i][j] /= p
        for r in range(n):
            if r != i:
                f = aug[r][i]
                for j in range(2 * n):
                    aug[r][j] -= f * aug[i][j]
    return [[aug[i][n + j] for j in range(n)] for i in range(n)]


def main() -> None:
    # Hypothetical covariance matrix and expected return vector
    cov = [
        [Fraction(4, 100), Fraction(1, 100), Fraction(1, 100)],
        [Fraction(1, 100), Fraction(5, 100), Fraction(2, 100)],
        [Fraction(1, 100), Fraction(2, 100), Fraction(6, 100)],
    ]
    mu = [Fraction(6, 100), Fraction(10, 100), Fraction(12, 100)]
    iota = [Fraction(1, 1), Fraction(1, 1), Fraction(1, 1)]

    inv = invert_3x3(cov)
    inv_iota = [sum((inv[i][j] * iota[j] for j in range(3)), Fraction(0, 1)) for i in range(3)]
    inv_mu = [sum((inv[i][j] * mu[j] for j in range(3)), Fraction(0, 1)) for i in range(3)]

    scalar_a = sum((iota[i] * inv_iota[i] for i in range(3)), Fraction(0, 1))
    scalar_b = sum((iota[i] * inv_mu[i] for i in range(3)), Fraction(0, 1))
    scalar_c = sum((mu[i] * inv_mu[i] for i in range(3)), Fraction(0, 1))
    scalar_d = scalar_a * scalar_c - scalar_b * scalar_b

    print(f"Scalar A: {scalar_a}")
    print(f"Scalar B: {scalar_b}")
    print(f"Scalar C: {scalar_c}")
    print(f"Scalar D: {scalar_d}")

    # GMV portfolio: w_GMV = Sigma^-1 iota / A
    w_gmv = [inv_iota[i] / scalar_a for i in range(3)]
    mu_gmv = sum((w_gmv[i] * mu[i] for i in range(3)), Fraction(0, 1))
    var_gmv = sum((w_gmv[i] * sum(cov[i][j] * w_gmv[j] for j in range(3)) for i in range(3)), Fraction(0, 1))

    print(f"w_GMV: [{w_gmv[0]}, {w_gmv[1]}, {w_gmv[2]}]")
    print(f"sum(w_GMV): {sum(w_gmv, Fraction(0, 1))}")
    print(f"mu_GMV: {mu_gmv}")
    print(f"var_GMV direct: {var_gmv}")
    print(f"var_GMV 1/A: {Fraction(1, 1) / scalar_a}")

    # Frontier portfolios for target returns 8% and 10%
    for target in (Fraction(8, 100), Fraction(10, 100)):
        l1 = (scalar_c - scalar_b * target) / scalar_d
        l2 = (scalar_a * target - scalar_b) / scalar_d
        w_p = [l1 * inv_iota[i] + l2 * inv_mu[i] for i in range(3)]
        achieved_mu = sum((w_p[i] * mu[i] for i in range(3)), Fraction(0, 1))
        var_direct = sum((w_p[i] * sum(cov[i][j] * w_p[j] for j in range(3)) for i in range(3)), Fraction(0, 1))
        var_formula = (scalar_a * target * target - 2 * scalar_b * target + scalar_c) / scalar_d

        print(f"Target {target}: w=[{w_p[0]}, {w_p[1]}, {w_p[2]}], sum={sum(w_p, Fraction(0, 1))}")
        print(f"Target {target}: achieved_mu={achieved_mu}, var_direct={var_direct}, var_formula={var_formula}")


main()
