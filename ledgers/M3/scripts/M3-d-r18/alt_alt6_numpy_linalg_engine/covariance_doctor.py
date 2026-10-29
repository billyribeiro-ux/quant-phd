"""Alternative correct implementation with NumPy: eigh clipping, numpy projection and linear solve."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

Matrix = list[list[float]]


def _as_matrix(matrix: Sequence[Sequence[float]]) -> np.ndarray:
    rows = [list(row) for row in matrix]
    n = len(rows)
    if n == 0 or any(len(row) != n for row in rows):
        raise ValueError("the matrix is not square")
    arr = np.array(rows, dtype=float)
    if np.max(np.abs(arr - arr.T)) > 1e-9:
        raise ValueError("the matrix is not symmetric beyond 1e-9")
    return (arr + arr.T) / 2.0


def min_eigenvalue(matrix: Sequence[Sequence[float]]) -> float:
    return float(np.linalg.eigvalsh(_as_matrix(matrix))[0])


def is_psd(matrix: Sequence[Sequence[float]], tol: float = 1e-10) -> bool:
    return bool(min_eigenvalue(matrix) >= -tol)


def _clip_array(arr: np.ndarray, floor: float) -> np.ndarray:
    values, vectors = np.linalg.eigh(arr)
    x = (vectors * np.maximum(values, floor)) @ vectors.T
    d = np.sqrt(np.diag(x))
    return x / np.outer(d, d)


def clip_repair(matrix: Sequence[Sequence[float]], floor: float = 0.0) -> Matrix:
    return _clip_array(_as_matrix(matrix), floor).tolist()


def _psd_part(arr: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh(arr)
    return (vectors * np.maximum(values, 0.0)) @ vectors.T


def projection_repair(matrix: Sequence[Sequence[float]], tol: float = 1e-10, max_iter: int = 500) -> Matrix:
    a = _as_matrix(matrix)
    n = a.shape[0]
    x = a.copy()
    ds = np.zeros((n, n))
    du = np.zeros((n, n))
    for _ in range(max_iter):
        y = _psd_part(x + ds)
        ds = x + ds - y
        new_x = y + du
        np.fill_diagonal(new_x, 1.0)
        du = y + du - new_x
        gap = float(np.linalg.norm(new_x - y))
        step = float(np.linalg.norm(new_x - x))
        x = new_x
        if gap <= tol and step <= tol:
            break
    return x.tolist()


def comparison_weights(corr: Sequence[Sequence[float]], vols: Sequence[float]) -> list[float]:
    c = _as_matrix(corr)
    n = c.shape[0]
    if len(vols) != n:
        raise ValueError("the volatilities must have one entry per row of the correlation matrix")
    if not all(float(v) > 0.0 for v in vols):
        raise ValueError("every volatility must be strictly positive")
    d = np.array([float(v) for v in vols])
    sigma = d[:, None] * c * d[None, :]
    raw = np.linalg.solve(sigma, np.ones(n))
    total = float(raw.sum())
    return [float(x) / total for x in raw]
