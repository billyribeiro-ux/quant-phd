"""Lab X3-project-2: Rung 2 completion problem for Kilian SVAR identification and FEVD.

Tests completed implementation of Cholesky factorization, structural shock extraction,
and forecast error variance decomposition normalization.
"""

from __future__ import annotations

import math


def cholesky(a_mat: list[list[float]]) -> list[list[float]]:
    """Compute lower-triangular Cholesky factorization L such that L L^T = A."""
    n = len(a_mat)
    l_mat = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(l_mat[i][k] * l_mat[j][k] for k in range(j))
            if i == j:
                val = a_mat[i][i] - s
                if val <= 1e-14:
                    raise ValueError("Matrix is not positive definite")
                l_mat[i][j] = math.sqrt(val)
            else:
                l_mat[i][j] = (a_mat[i][j] - s) / l_mat[j][j]
    return l_mat


def invert_lower_triangular(l_mat: list[list[float]]) -> list[list[float]]:
    """Invert lower triangular matrix via forward substitution."""
    n = len(l_mat)
    inv = [[0.0] * n for _ in range(n)]
    for i in range(n):
        inv[i][i] = 1.0 / l_mat[i][i]
        for j in range(i):
            s = sum(l_mat[i][k] * inv[k][j] for k in range(j, i))
            inv[i][j] = -s / l_mat[i][i]
    return inv


def compute_structural_shocks(residuals: list[list[float]], p_mat: list[list[float]]) -> list[list[float]]:
    """Compute structural innovations eps_t = P^-1 e_t."""
    p_inv = invert_lower_triangular(p_mat)
    k_vars = len(p_mat)
    shocks: list[list[float]] = []
    for e in residuals:
        eps = [sum(p_inv[i][j] * e[j] for j in range(k_vars)) for i in range(k_vars)]
        shocks.append([round(x, 6) for x in eps])
    return shocks


def compute_fevd_shares(cum_mse: list[list[float]]) -> list[list[float]]:
    """Compute FEVD percentage shares normalizing by total variable forecast error variance."""
    k_vars = len(cum_mse)
    fevd_matrix = [[0.0] * k_vars for _ in range(k_vars)]
    for i in range(k_vars):
        total_var = sum(cum_mse[i])
        for j in range(k_vars):
            fevd_matrix[i][j] = cum_mse[i][j] / total_var if total_var > 1e-12 else 0.0
    return fevd_matrix


def main() -> None:
    print("Lab X3-project-2 | Completion Problem: Cholesky & FEVD Normalization")
    print("-" * 75)

    # Sample covariance matrix Sigma_u
    sigma_u = [
        [1.4400, 0.7200, -0.0360],
        [0.7200, 64.3600, 0.2880],
        [-0.0360, 0.2880, 0.0169],
    ]

    p_mat = cholesky(sigma_u)
    print("1. Cholesky Factorization P (A_0^-1):")
    for i, row in enumerate(p_mat):
        print(f"   Row {i}: [{row[0]:8.4f}, {row[1]:8.4f}, {row[2]:8.4f}]")

    # Sample residuals (2 periods)
    sample_e = [
        [1.2000, 8.0000, 0.1200],
        [-0.6000, 4.0000, -0.0500],
    ]
    shocks = compute_structural_shocks(sample_e, p_mat)
    print("\n2. Extracted Structural Shocks eps_t:")
    for t, eps in enumerate(shocks):
        print(f"   t={t}: [{eps[0]:8.4f}, {eps[1]:8.4f}, {eps[2]:8.4f}]")

    # Sample cumulative MSE matrix at horizon 12
    sample_mse = [
        [2.5000, 0.2000, 0.1000],  # var 0 (delta_prod): total = 2.80
        [4.0000, 45.0000, 1.0000],  # var 1 (rea): total = 50.00
        [0.0080, 0.0620, 0.0200],  # var 2 (rpo): total = 0.090
    ]
    shares = compute_fevd_shares(sample_mse)
    print("\n3. Normalized FEVD Shares (H=12M):")
    for name, row in zip(["delta_prod", "rea       ", "rpo       "], shares, strict=True):
        print(f"   {name}: Supply={row[0] * 100:5.1f}%, Demand={row[1] * 100:5.1f}%, Oil-Spec={row[2] * 100:5.1f}%")

    # Row sum verification
    sums_ok = all(abs(sum(shares[i]) - 1.0) < 1e-6 for i in range(3))
    print(f"\n4. Verification: All FEVD rows sum to 1.0: {sums_ok}")


main()
