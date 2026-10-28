"""Alternative B (verifier round 2): pure Python. Cholesky bisection for the minimum eigenvalue, Jacobi with an
absolute pivot cutoff, Dykstra with an absolute change stopping rule, and Cholesky solves for the weights.
"""

from __future__ import annotations

import math


def _check(rows: list[list[float]]) -> int:
    n = len(rows)
    if any(len(r) != n for r in rows):
        raise ValueError("the matrix is not square")
    for i in range(n):
        for j in range(i + 1, n):
            if abs(rows[i][j] - rows[j][i]) > 1e-9:
                raise ValueError("the matrix is not symmetric beyond 1e-9")
    return n


def _pd(m: list[list[float]]) -> bool:
    n = len(m)
    low = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(low[i][k] * low[j][k] for k in range(j))
            if i == j:
                p = m[i][i] - s
                if p <= 0.0:
                    return False
                low[i][i] = math.sqrt(p)
            else:
                low[i][j] = (m[i][j] - s) / low[j][j]
    return True


def min_eigenvalue(matrix: list[list[float]]) -> float:
    n = _check(matrix)
    radius = sum(abs(x) for r in matrix for x in r) + 1.0
    lo, hi = -radius, radius
    for _ in range(120):
        mid = 0.5 * (lo + hi)
        shifted = [[matrix[i][j] - (mid if i == j else 0.0) for j in range(n)] for i in range(n)]
        if _pd(shifted):
            lo = mid
        else:
            hi = mid
    return lo


def is_psd(matrix: list[list[float]], tol: float = 1e-10) -> bool:
    return min_eigenvalue(matrix) >= -tol


def _jacobi(a: list[list[float]]) -> tuple[list[float], list[list[float]]]:
    n = len(a)
    m = [r[:] for r in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(60):
        off = sum(m[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-28:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(m[p][q]) < 1e-14:
                    m[p][q] = m[q][p] = 0.0
                    continue
                theta = (m[q][q] - m[p][p]) / (2.0 * m[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    mkp, mkq = m[k][p], m[k][q]
                    m[k][p], m[k][q] = c * mkp - s * mkq, s * mkp + c * mkq
                for k in range(n):
                    mpk, mqk = m[p][k], m[q][k]
                    m[p][k], m[q][k] = c * mpk - s * mqk, s * mpk + c * mqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    return [m[i][i] for i in range(n)], v


def _rebuild(values: list[float], vectors: list[list[float]]) -> list[list[float]]:
    n = len(values)
    return [[sum(vectors[i][k] * values[k] * vectors[j][k] for k in range(n)) for j in range(n)] for i in range(n)]


def clip_repair(matrix: list[list[float]], floor: float = 0.0) -> list[list[float]]:
    _check(matrix)
    values, vectors = _jacobi(matrix)
    x = _rebuild([max(val, floor) for val in values], vectors)
    n = len(x)
    d = [x[i][i] for i in range(n)]
    return [[x[i][j] / math.sqrt(d[i] * d[j]) for j in range(n)] for i in range(n)]


def _psd_part(a: list[list[float]]) -> list[list[float]]:
    values, vectors = _jacobi(a)
    return _rebuild([max(val, 0.0) for val in values], vectors)


def projection_repair(matrix: list[list[float]], tol: float = 1e-10, max_iter: int = 500) -> list[list[float]]:
    _check(matrix)
    n = len(matrix)
    x = [r[:] for r in matrix]
    ds = [[0.0] * n for _ in range(n)]
    du = [[0.0] * n for _ in range(n)]
    for _ in range(max_iter):
        y = _psd_part([[x[i][j] + ds[i][j] for j in range(n)] for i in range(n)])
        ds = [[x[i][j] + ds[i][j] - y[i][j] for j in range(n)] for i in range(n)]
        new_x = [[y[i][j] + du[i][j] for j in range(n)] for i in range(n)]
        for i in range(n):
            new_x[i][i] = 1.0
        du = [[y[i][j] + du[i][j] - new_x[i][j] for j in range(n)] for i in range(n)]
        change = max(abs(new_x[i][j] - x[i][j]) for i in range(n) for j in range(n))
        x = new_x
        if change <= tol:
            break
    return x


def comparison_weights(corr: list[list[float]], vols: list[float]) -> list[float]:
    n = _check(corr)
    if len(vols) != n:
        raise ValueError("one volatility per row is required")
    if any(v <= 0 for v in vols):
        raise ValueError("a volatility must be strictly positive")
    sigma = [[vols[i] * corr[i][j] * vols[j] for j in range(n)] for i in range(n)]
    low = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(low[i][k] * low[j][k] for k in range(j))
            if i == j:
                low[i][i] = math.sqrt(sigma[i][i] - s)
            else:
                low[i][j] = (sigma[i][j] - s) / low[j][j]
    y = [0.0] * n
    for i in range(n):
        y[i] = (1.0 - sum(low[i][k] * y[k] for k in range(i))) / low[i][i]
    w = [0.0] * n
    for i in reversed(range(n)):
        w[i] = (y[i] - sum(low[k][i] * w[k] for k in range(i + 1, n))) / low[i][i]
    total = sum(w)
    return [x / total for x in w]
