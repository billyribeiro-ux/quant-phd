"""Alternative A (verifier round 2): NumPy eigh for the spectral steps, Dykstra with a max-entry stopping rule.

Different numerical route from the reference: numpy.linalg.eigh instead of cyclic Jacobi; the stopping rule is the
largest entry change of the iterate instead of the two Frobenius norms; the nearness claim is the same spec.
"""

from __future__ import annotations

import numpy as np


def _matrix(rows: object) -> np.ndarray:
    a = np.array(rows, dtype=float)
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError("the matrix is not square")
    if np.max(np.abs(a - a.T)) > 1e-9:
        raise ValueError("the matrix is not symmetric beyond 1e-9")
    return (a + a.T) / 2.0


def min_eigenvalue(matrix: list[list[float]]) -> float:
    return float(np.linalg.eigvalsh(_matrix(matrix))[0])


def is_psd(matrix: list[list[float]], tol: float = 1e-10) -> bool:
    return bool(min_eigenvalue(matrix) >= -tol)


def clip_repair(matrix: list[list[float]], floor: float = 0.0) -> list[list[float]]:
    a = _matrix(matrix)
    values, vectors = np.linalg.eigh(a)
    x = (vectors * np.maximum(values, floor)) @ vectors.T
    d = np.sqrt(np.diag(x))
    return (x / np.outer(d, d)).tolist()


def projection_repair(matrix: list[list[float]], tol: float = 1e-10, max_iter: int = 500) -> list[list[float]]:
    x = _matrix(matrix)
    n = x.shape[0]
    corr_s = np.zeros((n, n))
    corr_u = np.zeros((n, n))
    for _ in range(max_iter):
        values, vectors = np.linalg.eigh(x + corr_s)
        y = (vectors * np.maximum(values, 0.0)) @ vectors.T
        corr_s = x + corr_s - y
        new_x = y + corr_u
        np.fill_diagonal(new_x, 1.0)
        corr_u = y + corr_u - new_x
        change = float(np.max(np.abs(new_x - x)))
        x = new_x
        if change <= tol:
            break
    return x.tolist()


def comparison_weights(corr: list[list[float]], vols: list[float]) -> list[float]:
    c = _matrix(corr)
    n = c.shape[0]
    if len(vols) != n:
        raise ValueError("one volatility per row is required")
    if any(v <= 0 for v in vols):
        raise ValueError("a volatility must be strictly positive")
    d = np.diag(np.asarray(vols, dtype=float))
    sigma = d @ c @ d
    w = np.linalg.solve(sigma, np.ones(n))
    return (w / w.sum()).tolist()
