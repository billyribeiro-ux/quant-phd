"""Lab X3-project-1: Rung 1 worked example for Kilian Structural VAR Oil-Shock Decomposition.

Executes the complete VAR estimation, Cholesky identification, IRF computation,
and FEVD calculation on seed 42.
"""

from __future__ import annotations

import math
from typing import Any


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
    """Multiply two 2D matrices."""
    n = len(a_mat)
    m = len(b_mat[0])
    p = len(b_mat)
    return [[sum(a_mat[i][k] * b_mat[k][j] for k in range(p)) for j in range(m)] for i in range(n)]


def transpose(a_mat: list[list[float]]) -> list[list[float]]:
    """Transpose a 2D matrix."""
    return [[a_mat[i][j] for i in range(len(a_mat))] for j in range(len(a_mat[0]))]


def estimate_var(data: list[list[float]], lags: int) -> dict[str, Any]:
    """Estimate VAR(p) via OLS."""
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
    sigma_u = [[round(ete[i][j] / dof, 8) for j in range(k_vars)] for i in range(k_vars)]

    intercepts = [round(b_hat[0][k], 6) for k in range(k_vars)]
    coefficients: list[list[list[float]]] = []
    for lag_idx in range(lags):
        bl: list[list[float]] = []
        for i in range(k_vars):
            row: list[float] = []
            for j in range(k_vars):
                idx = 1 + lag_idx * k_vars + j
                row.append(round(b_hat[idx][i], 6))
            bl.append(row)
        coefficients.append(bl)

    residuals = [[round(val, 6) for val in row] for row in e_mat]
    return {
        "intercepts": intercepts,
        "coefficients": coefficients,
        "residuals": residuals,
        "sigma_u": sigma_u,
    }


def compute_irf(
    coefficients: list[list[list[float]]], p_matrix: list[list[float]], horizon: int
) -> list[list[list[float]]]:
    """Compute structural impulse response functions Theta_h = Phi_h * P."""
    k_vars = len(p_matrix)
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
        theta_h = matmul(phi[h], p_matrix)
        irfs.append([[round(theta_h[i][j], 6) for j in range(k_vars)] for i in range(k_vars)])
    return irfs


def compute_fevd(irf: list[list[list[float]]]) -> list[list[list[float]]]:
    """Compute forecast error variance decomposition shares."""
    h_max = len(irf) - 1
    k_vars = len(irf[0])
    fevd: list[list[list[float]]] = []
    cum_mse = [[0.0] * k_vars for _ in range(k_vars)]
    for h in range(h_max + 1):
        fevd_h = [[0.0] * k_vars for _ in range(k_vars)]
        for i in range(k_vars):
            for j in range(k_vars):
                cum_mse[i][j] += irf[h][i][j] ** 2
            total_var_i = sum(cum_mse[i])
            for j in range(k_vars):
                fevd_h[i][j] = round(cum_mse[i][j] / total_var_i, 6) if total_var_i > 1e-12 else 0.0
        fevd.append(fevd_h)
    return fevd


def main() -> None:
    # Inline make_instance(42) logic to keep standalone
    import random

    rng = random.Random(42)
    n_obs = 140
    p = 2
    k_vars = 3

    b1 = [
        [0.15 + rng.uniform(-0.02, 0.02), 0.01 + rng.uniform(-0.002, 0.002), -0.05 + rng.uniform(-0.01, 0.01)],
        [0.50 + rng.uniform(-0.05, 0.05), 0.70 + rng.uniform(-0.02, 0.02), -0.50 + rng.uniform(-0.05, 0.05)],
        [0.02 + rng.uniform(-0.005, 0.005), 0.008 + rng.uniform(-0.001, 0.001), 0.82 + rng.uniform(-0.02, 0.02)],
    ]
    b2 = [
        [0.05 + rng.uniform(-0.01, 0.01), 0.005 + rng.uniform(-0.001, 0.001), -0.02 + rng.uniform(-0.005, 0.005)],
        [-0.20 + rng.uniform(-0.02, 0.02), 0.15 + rng.uniform(-0.02, 0.02), -0.20 + rng.uniform(-0.02, 0.02)],
        [-0.01 + rng.uniform(-0.002, 0.002), 0.002 + rng.uniform(-0.001, 0.001), 0.06 + rng.uniform(-0.01, 0.01)],
    ]
    mu = [0.10, 0.0, 4.0]
    i_minus_b = [
        [1.0 - b1[0][0] - b2[0][0], -b1[0][1] - b2[0][1], -b1[0][2] - b2[0][2]],
        [-b1[1][0] - b2[1][0], 1.0 - b1[1][1] - b2[1][1], -b1[1][2] - b2[1][2]],
        [-b1[2][0] - b2[2][0], -b1[2][1] - b2[2][1], 1.0 - b1[2][2] - b2[2][2]],
    ]
    intercepts = [sum(i_minus_b[i][j] * mu[j] for j in range(k_vars)) for i in range(k_vars)]
    p_mat_true = [
        [1.20, 0.0, 0.0],
        [0.60 + rng.uniform(-0.05, 0.05), 8.00, 0.0],
        [-0.03 + rng.uniform(-0.005, 0.005), 0.04 + rng.uniform(-0.005, 0.005), 0.12],
    ]

    burn = 100
    y = [mu[:] for _ in range(p)]
    for _ in range(burn + n_obs - p):
        eps = [rng.gauss(0.0, 1.0) for _ in range(k_vars)]
        e = [sum(p_mat_true[i][j] * eps[j] for j in range(k_vars)) for i in range(k_vars)]
        yt = [
            intercepts[i]
            + sum(b1[i][j] * y[-1][j] for j in range(k_vars))
            + sum(b2[i][j] * y[-2][j] for j in range(k_vars))
            + e[i]
            for i in range(k_vars)
        ]
        y.append(yt)

    data = [[round(val, 6) for val in row] for row in y[burn:]]

    print("Lab X3-project-1 | Kilian Structural VAR Worked Example (Seed 42)")
    print("-" * 75)
    print(f"Step 1 | Data loaded: N = {len(data)} monthly observations across 3 variables")
    print(f"       | Variables: [0: delta_prod, 1: rea, 2: rpo], Lag order p = {p}")

    var_res = estimate_var(data, lags=p)
    l_mat = cholesky(var_res["sigma_u"])
    p_est = [[round(l_mat[i][j], 4) for j in range(k_vars)] for i in range(k_vars)]

    print("Step 2 | Estimated Cholesky Impact Matrix P (A_0^-1):")
    for i, vname in enumerate(["delta_prod", "rea", "rpo"]):
        print(f"       | {vname:<12} [ {p_est[i][0]:8.4f}  {p_est[i][1]:8.4f}  {p_est[i][2]:8.4f} ]")

    irf = compute_irf(var_res["coefficients"], p_est, horizon=24)
    fevd = compute_fevd(irf)

    print("-" * 75)
    print("Step 3 | Forecast Error Variance Decomposition of Real Oil Price (rpo):")
    print(f"{'Horizon':>12} {'Oil Supply Shock':>20} {'Aggregate Demand':>20} {'Precautionary Demand':>20}")
    print("-" * 75)
    for h in [0, 1, 6, 12, 24]:
        shares = fevd[h][2]
        print(f"{h:10d}M {shares[0] * 100:19.1f}% {shares[1] * 100:19.1f}% {shares[2] * 100:19.1f}%")

    print("-" * 75)
    print("Step 4 | Identification Verification: P[0, 1] == 0, P[0, 2] == 0, P[1, 2] == 0.")
    print("       | At horizon 0, oil supply is 100% explained by supply shock.")
    print(f"       | Actual FEVD(0, delta_prod) = {fevd[0][0][0] * 100:.1f}%.")


main()
