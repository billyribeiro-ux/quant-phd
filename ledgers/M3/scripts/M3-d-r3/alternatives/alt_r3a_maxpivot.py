"""Alternative r3a: classical max-pivot Jacobi (cutoff 1e-13), Dykstra with unit-diagonal projection first,
LU with partial pivoting for the weights. Standard library only."""

from __future__ import annotations

import math

SYMMETRY_TOL = 1e-9


def _check(matrix):
    rows = [list(r) for r in matrix]
    n = len(rows)
    if n == 0 or any(len(r) != n for r in rows):
        raise ValueError("the matrix is not square: every row must have as many entries as there are rows")
    out = [[float(x) for x in r] for r in rows]
    for i in range(n):
        for j in range(i + 1, n):
            if abs(out[i][j] - out[j][i]) > SYMMETRY_TOL:
                raise ValueError("the matrix is not symmetric: entries m[i][j] and m[j][i] differ by more than 1e-9")
    return [[(out[i][j] + out[j][i]) / 2.0 for j in range(n)] for i in range(n)]


def _eig(a):
    n = len(a)
    m = [r[:] for r in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(2000):
        p = q = 0
        big = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(m[i][j]) > big:
                    big, p, q = abs(m[i][j]), i, j
        scale = math.sqrt(sum(m[i][j] ** 2 for i in range(n) for j in range(n)))
        if big <= 1e-13 * max(scale, 1e-300):
            break
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


def _psd_part(a):
    values, vecs = _eig(a)
    return _rebuild([max(x, 0.0) for x in values], vecs)


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


def projection_repair(matrix, tol=1e-10, max_iter=500):
    """Dykstra, with the unit-diagonal projection applied first; stops at the caller's tol and max_iter."""
    a = _check(matrix)
    n = len(a)
    x = [r[:] for r in a]
    cs = [[0.0] * n for _ in range(n)]
    cu = [[0.0] * n for _ in range(n)]
    for _ in range(max_iter):
        z = [[x[i][j] + cu[i][j] for j in range(n)] for i in range(n)]
        for i in range(n):
            z[i][i] = 1.0
        cu = [[x[i][j] + cu[i][j] - z[i][j] for j in range(n)] for i in range(n)]
        y = _psd_part([[z[i][j] + cs[i][j] for j in range(n)] for i in range(n)])
        cs = [[z[i][j] + cs[i][j] - y[i][j] for j in range(n)] for i in range(n)]
        gap = math.sqrt(sum((z[i][j] - y[i][j]) ** 2 for i in range(n) for j in range(n)))
        step = math.sqrt(sum((y[i][j] - x[i][j]) ** 2 for i in range(n) for j in range(n)))
        x = y
        if gap <= tol and step <= tol:
            break
    for i in range(n):
        x[i][i] = 1.0
    return x


def comparison_weights(corr, vols):
    c = _check(corr)
    n = len(c)
    if len(vols) != n:
        raise ValueError("the volatilities must have one entry per row of the correlation matrix")
    if any(float(v) <= 0.0 for v in vols):
        raise ValueError("every volatility must be strictly positive")
    s = [[float(vols[i]) * c[i][j] * float(vols[j]) for j in range(n)] for i in range(n)]
    # LU with partial pivoting, then solve S w = 1
    lu = [r[:] for r in s]
    perm = list(range(n))
    for k in range(n):
        p = max(range(k, n), key=lambda r: abs(lu[r][k]))
        lu[k], lu[p] = lu[p], lu[k]
        perm[k], perm[p] = perm[p], perm[k]
        for r in range(k + 1, n):
            lu[r][k] /= lu[k][k]
            for col in range(k + 1, n):
                lu[r][col] -= lu[r][k] * lu[k][col]
    b = [1.0] * n
    y = [0.0] * n
    for i in range(n):
        y[i] = b[perm[i]] - sum(lu[i][j] * y[j] for j in range(i))
    x = [0.0] * n
    for i in reversed(range(n)):
        x[i] = (y[i] - sum(lu[i][j] * x[j] for j in range(i + 1, n))) / lu[i][i]
    total = sum(x)
    return [v / total for v in x]
