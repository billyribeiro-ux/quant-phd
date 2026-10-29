"""Alternative r3c: cyclic Jacobi with atan2 rotation angles and a RELATIVE cutoff of 1e-15 (100 sweeps); is_psd by the
eigenvalues; Dykstra stopping on the gap only; weights by Gauss-Jordan with the first nonzero pivot. Standard library."""

from __future__ import annotations

import math


def _check(matrix):
    rows = [list(r) for r in matrix]
    n = len(rows)
    if n == 0 or any(len(r) != n for r in rows):
        raise ValueError("the matrix is not square: every row must have as many entries as there are rows")
    out = [[float(x) for x in r] for r in rows]
    for i in range(n):
        for j in range(i + 1, n):
            if abs(out[i][j] - out[j][i]) > 1e-9:
                raise ValueError("the matrix is not symmetric: entries m[i][j] and m[j][i] differ by more than 1e-9")
    return [[(out[i][j] + out[j][i]) / 2.0 for j in range(n)] for i in range(n)]


def _eig(a):
    n = len(a)
    m = [r[:] for r in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(100):
        scale = math.sqrt(sum(m[i][j] ** 2 for i in range(n) for j in range(n)))
        off = math.sqrt(sum(m[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        if off <= 1e-15 * max(scale, 1e-300):
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if m[p][q] == 0.0:
                    continue
                phi = 0.5 * math.atan2(2.0 * m[p][q], m[p][p] - m[q][q])
                c, s = math.cos(phi), math.sin(phi)
                for k in range(n):
                    mkp, mkq = m[k][p], m[k][q]
                    m[k][p] = c * mkp + s * mkq
                    m[k][q] = -s * mkp + c * mkq
                for k in range(n):
                    mpk, mqk = m[p][k], m[q][k]
                    m[p][k] = c * mpk + s * mqk
                    m[q][k] = -s * mpk + c * mqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp + s * vkq
                    v[k][q] = -s * vkp + c * vkq
    return [m[i][i] for i in range(n)], v


def _rebuild(values, vecs):
    n = len(values)
    return [[sum(vecs[i][k] * values[k] * vecs[j][k] for k in range(n)) for j in range(n)] for i in range(n)]


def _cholesky_ok(m):
    """True when every Cholesky pivot is at least zero (so m is positive semidefinite up to rounding)."""
    n = len(m)
    low = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(low[i][k] * low[j][k] for k in range(j))
            if i == j:
                pivot = m[i][i] - s
                if pivot < 0.0:
                    return False
                low[i][i] = math.sqrt(pivot)
            elif low[j][j] == 0.0:
                if abs(m[i][j] - s) > 1e-300:
                    return False
            else:
                low[i][j] = (m[i][j] - s) / low[j][j]
    return True


def min_eigenvalue(matrix):
    values, _ = _eig(_check(matrix))
    return min(values)


def is_psd(matrix, tol=1e-10):
    return min_eigenvalue(matrix) >= -tol


def clip_repair(matrix, floor=0.0):
    a = _check(matrix)
    values, vecs = _eig(a)
    x = _rebuild([max(v, floor) for v in values], vecs)
    d = [x[i][i] for i in range(len(x))]
    if any(v <= 0.0 for v in d):
        raise ValueError("a diagonal entry of the repaired matrix is not positive, so it cannot be rescaled")
    return [[x[i][j] / math.sqrt(d[i] * d[j]) for j in range(len(x))] for i in range(len(x))]


def _psd_part(a):
    values, vecs = _eig(a)
    return _rebuild([max(v, 0.0) for v in values], vecs)


def projection_repair(matrix, tol=1e-10, max_iter=500):
    a = _check(matrix)
    n = len(a)
    x = [r[:] for r in a]
    cs = [[0.0] * n for _ in range(n)]
    cu = [[0.0] * n for _ in range(n)]
    for _ in range(max_iter):
        y = _psd_part([[x[i][j] + cs[i][j] for j in range(n)] for i in range(n)])
        cs = [[x[i][j] + cs[i][j] - y[i][j] for j in range(n)] for i in range(n)]
        new_x = [[y[i][j] + cu[i][j] for j in range(n)] for i in range(n)]
        for i in range(n):
            new_x[i][i] = 1.0
        cu = [[y[i][j] + cu[i][j] - new_x[i][j] for j in range(n)] for i in range(n)]
        gap = math.sqrt(sum((new_x[i][j] - y[i][j]) ** 2 for i in range(n) for j in range(n)))
        step = math.sqrt(sum((new_x[i][j] - x[i][j]) ** 2 for i in range(n) for j in range(n)))
        x = new_x
        if gap <= tol:
            break
    return x


def comparison_weights(corr, vols):
    c = _check(corr)
    n = len(c)
    if len(vols) != n:
        raise ValueError("the volatilities must have one entry per row of the correlation matrix")
    if any(float(v) <= 0.0 for v in vols):
        raise ValueError("every volatility must be strictly positive")
    s = [[float(vols[i]) * c[i][j] * float(vols[j]) for j in range(n)] for i in range(n)]
    aug = [s[i][:] + [1.0] for i in range(n)]
    for col in range(n):
        piv = next(r for r in range(col, n) if abs(aug[r][col]) > 0.0)
        aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        aug[col] = [x / pv for x in aug[col]]
        for r in range(n):
            if r != col:
                f = aug[r][col]
                aug[r] = [x - f * y for x, y in zip(aug[r], aug[col])]
    sol = [aug[i][n] for i in range(n)]
    total = sum(sol)
    return [x / total for x in sol]
