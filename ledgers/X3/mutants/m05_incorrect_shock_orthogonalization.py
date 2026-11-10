"""Mutant: Multiplies residuals by P instead of inverting P to compute structural shocks."""

from __future__ import annotations

import math
from typing import Any


def cholesky(a_mat: list[list[float]]) -> list[list[float]]:
    """Compute lower-triangular Cholesky factorization L such that L L^T = A."""
    n = len(a_mat)
    if any(len(row) != n for row in a_mat):
        raise ValueError("Matrix must be square")
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
    """Invert a square matrix using Gauss-Jordan elimination with partial pivoting."""
    n = len(a_mat)
    if any(len(row) != n for row in a_mat):
        raise ValueError("Matrix must be square")
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
    """Estimate a VAR(p) model with constant intercepts via ordinary least squares."""
    if lags < 1:
        raise ValueError("Lag order must be at least 1")
    t_obs = len(data)
    if t_obs == 0:
        raise ValueError("Data cannot be empty")
    k_vars = len(data[0])
    n_effective = t_obs - lags
    num_params = 1 + k_vars * lags
    if n_effective <= num_params:
        raise ValueError("Insufficient observations for lag order")

    x_mat: list[list[float]] = []
    y_mat: list[list[float]] = []
    for t in range(lags, t_obs):
        row_x = [1.0]
        for lag_idx in range(1, lags + 1):
            row_x.extend(data[t - lag_idx])
        x_mat.append(row_x)
        y_mat.append(data[t][:])

    xt = transpose(x_mat)
    xtx = matmul(xt, x_mat)
    xtx_inv = invert_matrix(xtx)
    xty = matmul(xt, y_mat)
    b_hat = matmul(xtx_inv, xty)

    xb = matmul(x_mat, b_hat)
    e_mat = [[y_mat[t][k] - xb[t][k] for k in range(k_vars)] for t in range(n_effective)]

    et = transpose(e_mat)
    ete = matmul(et, e_mat)
    dof = float(n_effective - num_params)
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


def cholesky_identification(sigma_u: list[list[float]]) -> list[list[float]]:
    """Compute the lower-triangular structural impact matrix P such that P P^T = Sigma_u."""
    l_mat = cholesky(sigma_u)
    k_vars = len(l_mat)
    p_mat = [[0.0] * k_vars for _ in range(k_vars)]
    for i in range(k_vars):
        for j in range(i + 1):
            p_mat[i][j] = round(l_mat[i][j], 6)
    return p_mat


def compute_structural_shocks(residuals: list[list[float]], p_matrix: list[list[float]]) -> list[list[float]]:
    """Mutant: Multiplies residuals by P instead of P^-1."""
    k_vars = len(p_matrix)
    shocks: list[list[float]] = []
    for e in residuals:
        # Erroneously computes eps = P * e instead of P^-1 * e
        eps = [sum(p_matrix[i][j] * e[j] for j in range(k_vars)) for i in range(k_vars)]
        shocks.append([round(x, 6) for x in eps])
    return shocks


def compute_irf(
    coefficients: list[list[list[float]]], p_matrix: list[list[float]], horizon: int
) -> list[list[list[float]]]:
    """Compute structural impulse response functions."""
    if horizon < 0:
        raise ValueError("Horizon must be non-negative")
    k_vars = len(p_matrix)
    p_lags = len(coefficients)

    phi: list[list[list[float]]] = [[[1.0 if i == j else 0.0 for j in range(k_vars)] for i in range(k_vars)]]
    for h in range(1, horizon + 1):
        phi_h = [[0.0] * k_vars for _ in range(k_vars)]
        for j in range(1, min(h, p_lags) + 1):
            bj = coefficients[j - 1]
            phi_prev = phi[h - j]
            b_phi = matmul(bj, phi_prev)
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


def compute_historical_decomposition(
    residuals: list[list[float]], coefficients: list[list[list[float]]], p_matrix: list[list[float]]
) -> dict[str, Any]:
    """Compute cumulative historical shock contributions."""
    k_vars = len(p_matrix)
    n_obs = len(residuals)
    shocks = compute_structural_shocks(residuals, p_matrix)
    irf = compute_irf(coefficients, p_matrix, n_obs - 1)

    contributions = [[[0.0] * k_vars for _ in range(n_obs)] for _ in range(k_vars)]
    for j in range(k_vars):
        for t in range(n_obs):
            for i in range(k_vars):
                val = sum(irf[s][i][j] * shocks[t - s][j] for s in range(t + 1))
                contributions[j][t][i] = round(val, 6)

    fitted = [
        [round(sum(contributions[j][t][i] for j in range(k_vars)), 6) for i in range(k_vars)] for t in range(n_obs)
    ]
    return {
        "structural_shocks": shocks,
        "contributions": contributions,
        "fitted": fitted,
    }


def run_oil_shock_var(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute the pipeline with incorrect shock orthogonalization mutant."""
    data = [[float(v) for v in row] for row in instance["data"]]
    lags = int(instance["lags"])
    horizon = int(instance.get("horizon", 24))

    var_res = estimate_var(data, lags)
    p_matrix = cholesky_identification(var_res["sigma_u"])
    shocks = compute_structural_shocks(var_res["residuals"], p_matrix)
    irf = compute_irf(var_res["coefficients"], p_matrix, horizon)
    fevd = compute_fevd(irf)
    hd = compute_historical_decomposition(var_res["residuals"], var_res["coefficients"], p_matrix)

    return {
        "seed": int(instance["seed"]),
        "intercepts": var_res["intercepts"],
        "coefficients": var_res["coefficients"],
        "sigma_u": var_res["sigma_u"],
        "p_matrix": p_matrix,
        "structural_shocks": shocks,
        "irf": irf,
        "fevd": fevd,
        "historical_decomposition": hd,
    }
