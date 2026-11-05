"""Round-10 verifier probe (correct alternative, not a mutant): eigenvalues of a symmetric matrix from its SVD (singular
values give |lambda|; the sign is that of the Rayleigh quotient of the corresponding left singular vector), weights from
np.linalg.lstsq (SVD-based least squares, rcond cutoff), and a projection whose PSD step is the SVD reconstruction."""

from __future__ import annotations

import math

import numpy as np


def _as_matrix(matrix):
    rows = [list(row) for row in matrix]
    n = len(rows)
    if n == 0:
        raise ValueError("the matrix needs at least one row")
    if any(len(row) != n for row in rows):
        raise ValueError("the matrix is not square: every row must have as many entries as there are rows")
    a = np.array(rows, dtype=float)
    if np.max(np.abs(a - a.T)) > 1e-9:
        raise ValueError("the matrix is not symmetric: entries m[i][j] and m[j][i] differ by more than 1e-9")
    return (a + a.T) / 2.0


def _svd_eig(a):
    u, s, vt = np.linalg.svd(a)
    signs = np.sign(np.einsum("ij,ji->i", u.T, a @ u))
    signs[signs == 0] = 1.0
    return s * signs, u


def min_eigenvalue(matrix):
    vals, _ = _svd_eig(_as_matrix(matrix))
    return float(np.min(vals))


def is_psd(matrix, tol=1e-10):
    return bool(min_eigenvalue(matrix) >= -tol)


def _psd_part(a):
    vals, u = _svd_eig(a)
    return (u * np.maximum(vals, 0.0)) @ u.T


def clip_repair(matrix, floor=0.0):
    a = _as_matrix(matrix)
    vals, u = _svd_eig(a)
    x = (u * np.maximum(vals, floor)) @ u.T
    d = np.sqrt(np.diag(x))
    return (x / np.outer(d, d)).tolist()


def projection_repair(matrix, tol=1e-10, max_iter=500):
    a = _as_matrix(matrix)
    n = a.shape[0]
    x = a.copy()
    cs = np.zeros((n, n))
    cu = np.zeros((n, n))
    for _ in range(max_iter):
        y = _psd_part(x + cs)
        cs = x + cs - y
        nx = y + cu
        np.fill_diagonal(nx, 1.0)
        cu = y + cu - nx
        gap = float(np.linalg.norm(nx - y))
        step = float(np.linalg.norm(nx - x))
        x = nx
        if gap <= tol and step <= tol:
            break
    return x.tolist()


def comparison_weights(corr, vols):
    c = _as_matrix(corr)
    n = c.shape[0]
    if len(vols) != n:
        raise ValueError("the volatilities must have one entry per row of the correlation matrix")
    if not all(float(v) > 0.0 for v in vols):
        raise ValueError("every volatility must be strictly positive")
    s = np.diag([float(v) for v in vols])
    sigma = s @ c @ s
    x, *_ = np.linalg.lstsq(sigma, np.ones(n), rcond=None)
    total = float(np.sum(x))
    return [float(v) / total for v in x]
