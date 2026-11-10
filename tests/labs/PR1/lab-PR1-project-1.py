"""Rung 1 worked example: 1/N equal weighting and global minimum variance.

Illustrative inputs in exact Fraction arithmetic.
Fully solves a three-asset, six-observation investment window:
1. 1/N equal weight benchmark.
2. Sample mean return vector.
3. Unbiased sample covariance matrix S with divisor T - 1 = 5.
4. Analytical global minimum-variance (GMV) portfolio weights.
"""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    # 3 assets over 6 observation periods (T = 6, N = 3)
    returns = [
        [Fraction(2, 100), Fraction(1, 100), Fraction(3, 100)],
        [Fraction(4, 100), Fraction(2, 100), Fraction(-1, 100)],
        [Fraction(-1, 100), Fraction(3, 100), Fraction(2, 100)],
        [Fraction(3, 100), Fraction(-1, 100), Fraction(4, 100)],
        [Fraction(1, 100), Fraction(4, 100), Fraction(1, 100)],
        [Fraction(3, 100), Fraction(3, 100), Fraction(3, 100)],
    ]
    t_obs = len(returns)
    n_assets = len(returns[0])

    # Step 1: 1/N equal weight allocation
    w_1n = [Fraction(1, n_assets)] * n_assets
    print("Step 1 1/N weights:", [str(x) for x in w_1n])

    # Step 2: Sample mean return vector mu_hat
    mu_hat = [sum((returns[t][i] for t in range(t_obs)), Fraction(0)) / Fraction(t_obs) for i in range(n_assets)]
    print("Step 2 sample mean mu_hat:", [str(x) for x in mu_hat])

    # Step 3: Unbiased sample covariance matrix (divisor T - 1)
    s_cov = [[Fraction(0)] * n_assets for _ in range(n_assets)]
    for t in range(t_obs):
        diff = [returns[t][i] - mu_hat[i] for i in range(n_assets)]
        for i in range(n_assets):
            for j in range(n_assets):
                s_cov[i][j] += diff[i] * diff[j]
    for i in range(n_assets):
        for j in range(n_assets):
            s_cov[i][j] /= Fraction(t_obs - 1)
    print("Step 3 sample covariance diagonal:", [str(s_cov[i][i]) for i in range(n_assets)])

    # Step 4: Minimum variance portfolio weights w_gmv = S^-1 iota / (iota' S^-1 iota)
    size = n_assets
    a_mat = [row[:] for row in s_cov]
    inv = [[Fraction(1 if i == j else 0) for j in range(size)] for i in range(size)]
    for col in range(size):
        pivot = next(r for r in range(col, size) if a_mat[r][col] != 0)
        a_mat[col], a_mat[pivot] = a_mat[pivot], a_mat[col]
        inv[col], inv[pivot] = inv[pivot], inv[col]
        p = a_mat[col][col]
        for j in range(size):
            a_mat[col][j] /= p
            inv[col][j] /= p
        for r in range(size):
            if r != col and a_mat[r][col] != 0:
                factor = a_mat[r][col]
                for j in range(size):
                    a_mat[r][j] -= factor * a_mat[col][j]
                    inv[r][j] -= factor * inv[col][j]

    inv_iota = [sum((inv[i][j] for j in range(n_assets)), Fraction(0)) for i in range(n_assets)]
    denom = sum(inv_iota, Fraction(0))
    w_gmv = [inv_iota[i] / denom for i in range(n_assets)]
    print("Step 4 GMV weights:", [str(x) for x in w_gmv])


main()
