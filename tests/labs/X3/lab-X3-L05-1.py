"""Lab X3-L05-1: Kilian (2009) Structural VAR: Disentangling Demand and Supply Oil Shocks.

Estimates the 3-variable structural VAR model identifying crude oil supply shocks,
global aggregate demand shocks, and oil-market-specific precautionary demand shocks.
"""

from __future__ import annotations

import math
import random


def cholesky(a_mat: list[list[float]]) -> list[list[float]]:
    """Compute lower-triangular Cholesky factorization."""
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


def invert_matrix(a_mat: list[list[float]]) -> list[list[float]]:
    """Invert square matrix via Gauss-Jordan elimination."""
    n = len(a_mat)
    m = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(a_mat)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(m[r][i]))
        if abs(m[max_row][i]) < 1e-12:
            raise ValueError("Matrix is singular")
        m[i], m[max_row] = m[max_row], m[i]
        pivot = m[i][i]
        for c in range(2 * n):
            m[i][c] /= pivot
        for r in range(n):
            if r != i:
                factor = m[r][i]
                for c in range(2 * n):
                    m[r][c] -= factor * m[i][c]
    return [[m[r][c + n] for c in range(n)] for r in range(n)]


def matmul(a_mat: list[list[float]], b_mat: list[list[float]]) -> list[list[float]]:
    """Matrix multiplication."""
    n = len(a_mat)
    m = len(b_mat[0])
    p = len(b_mat)
    return [[sum(a_mat[i][k] * b_mat[k][j] for k in range(p)) for j in range(m)] for i in range(n)]


def transpose(a_mat: list[list[float]]) -> list[list[float]]:
    """Matrix transpose."""
    return [[a_mat[i][j] for i in range(len(a_mat))] for j in range(len(a_mat[0]))]


def estimate_var(data: list[list[float]], lags: int = 2) -> tuple[list[list[list[float]]], list[list[float]]]:
    """Estimate VAR(p) returning lag coefficients and reduced-form covariance Sigma_u."""
    t_obs = len(data)
    k_vars = len(data[0])
    n_eff = t_obs - lags
    num_params = 1 + k_vars * lags

    x_mat = []
    y_mat = []
    for t in range(lags, t_obs):
        row_x = [1.0]
        for lag_idx in range(1, lags + 1):
            row_x.extend(data[t - lag_idx])
        x_mat.append(row_x)
        y_mat.append(data[t][:])

    xt = transpose(x_mat)
    xtx_inv = invert_matrix(matmul(xt, x_mat))
    b_hat = matmul(xtx_inv, matmul(xt, y_mat))

    xb = matmul(x_mat, b_hat)
    e_mat = [[y_mat[t][k] - xb[t][k] for k in range(k_vars)] for t in range(n_eff)]
    et = transpose(e_mat)
    ete = matmul(et, e_mat)
    dof = float(n_eff - num_params)
    sigma_u = [[ete[i][j] / dof for j in range(k_vars)] for i in range(k_vars)]

    coefficients: list[list[list[float]]] = []
    for lag_idx in range(lags):
        bl: list[list[float]] = []
        for i in range(k_vars):
            row: list[float] = []
            for j in range(k_vars):
                idx = 1 + lag_idx * k_vars + j
                row.append(b_hat[idx][i])
            bl.append(row)
        coefficients.append(bl)

    return coefficients, sigma_u


def compute_irf_and_fevd(
    coefficients: list[list[list[float]]], p_mat: list[list[float]], horizon: int = 18
) -> tuple[list[list[list[float]]], list[list[list[float]]]]:
    """Compute structural IRFs and FEVD shares."""
    k_vars = len(p_mat)
    p_lags = len(coefficients)

    phi: list[list[list[float]]] = [[[1.0 if i == j else 0.0 for j in range(k_vars)] for i in range(k_vars)]]
    for h in range(1, horizon + 1):
        phi_h = [[0.0] * k_vars for _ in range(k_vars)]
        for j in range(1, min(h, p_lags) + 1):
            b_phi = matmul(coefficients[j - 1], phi[h - j])
            for r in range(k_vars):
                for c in range(k_vars):
                    phi_h[r][c] += b_phi[r][c]
        phi.append(phi_h)

    irfs: list[list[list[float]]] = []
    for h in range(horizon + 1):
        theta_h = matmul(phi[h], p_mat)
        irfs.append([[round(theta_h[i][j], 4) for j in range(k_vars)] for i in range(k_vars)])

    fevd: list[list[list[float]]] = []
    cum_mse = [[0.0] * k_vars for _ in range(k_vars)]
    for h in range(horizon + 1):
        fevd_h = [[0.0] * k_vars for _ in range(k_vars)]
        for i in range(k_vars):
            for j in range(k_vars):
                cum_mse[i][j] += irfs[h][i][j] ** 2
            tot = sum(cum_mse[i])
            for j in range(k_vars):
                fevd_h[i][j] = round(cum_mse[i][j] / tot, 4) if tot > 1e-12 else 0.0
        fevd.append(fevd_h)

    return irfs, fevd


def main() -> None:
    print("Lab X3-L05-1 | Kilian (2009) Structural VAR Oil-Shock Decomposition")
    print("-" * 75)

    # Generate synthetic monthly data matching Kilian (2009) moments
    rng = random.Random(42)
    n_obs = 150
    k_vars = 3
    true_p = [
        [1.20, 0.0, 0.0],
        [0.60, 8.00, 0.0],
        [-0.03, 0.04, 0.12],
    ]
    b1 = [
        [0.15, 0.01, -0.05],
        [0.50, 0.70, -0.50],
        [0.02, 0.008, 0.82],
    ]
    b2 = [
        [0.05, 0.005, -0.02],
        [-0.20, 0.15, -0.20],
        [-0.01, 0.002, 0.06],
    ]

    y = [[0.10, 0.0, 4.0] for _ in range(2)]
    for _ in range(n_obs):
        eps = [rng.gauss(0.0, 1.0) for _ in range(k_vars)]
        e = [sum(true_p[i][j] * eps[j] for j in range(k_vars)) for i in range(k_vars)]
        yt = [
            0.05
            + sum(b1[i][j] * y[-1][j] for j in range(k_vars))
            + sum(b2[i][j] * y[-2][j] for j in range(k_vars))
            + e[i]
            for i in range(k_vars)
        ]
        y.append(yt)

    data = y[2:]
    coeffs, sigma_u = estimate_var(data, lags=2)
    p_mat = cholesky(sigma_u)
    _irfs, fevd = compute_irf_and_fevd(coeffs, p_mat, horizon=18)

    print("Estimated Contemporaneous Impact Matrix P (A_0^-1):")
    print(f"  [Delta Prod]  {p_mat[0][0]:8.4f}  {p_mat[0][1]:8.4f}  {p_mat[0][2]:8.4f}")
    print(f"  [Real Act]    {p_mat[1][0]:8.4f}  {p_mat[1][1]:8.4f}  {p_mat[1][2]:8.4f}")
    print(f"  [Real Price]  {p_mat[2][0]:8.4f}  {p_mat[2][1]:8.4f}  {p_mat[2][2]:8.4f}")
    print("-" * 75)
    print("Verification of Recursive Cholesky Zero Restrictions:")
    print(f"  P[0, 1] = {p_mat[0][1]:.4f} == 0 (Supply predetermined to agg demand)")
    print(f"  P[0, 2] = {p_mat[0][2]:.4f} == 0 (Supply predetermined to oil-specific demand)")
    print(f"  P[1, 2] = {p_mat[1][2]:.4f} == 0 (Real activity predetermined to oil-specific demand)")
    print("-" * 75)

    print("Forecast Error Variance Decomposition (FEVD) of Real Oil Price (rpo):")
    print(f"{'Horizon':>10} {'Oil Supply Shock':>20} {'Aggregate Demand':>20} {'Oil-Specific Demand':>20}")
    print("-" * 75)
    horizons = [0, 1, 3, 6, 12, 18]
    for h in horizons:
        shares = fevd[h][2]
        print(f"{h:10d}M {shares[0] * 100:19.1f}% {shares[1] * 100:19.1f}% {shares[2] * 100:19.1f}%")

    print("-" * 75)
    print("Economic Finding (Kilian 2009):")
    print("  Oil-specific precautionary demand and global aggregate demand account for over 90%")
    print("  of the variance in real oil prices; crude oil supply shocks account for under 10%.")


main()
