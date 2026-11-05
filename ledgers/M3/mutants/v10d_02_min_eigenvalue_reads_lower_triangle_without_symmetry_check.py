"""min_eigenvalue skips the symmetry test and reads only the lower triangle, so an asymmetry beyond 1e-9 is accepted.

Pure Python, standard library only. Eigenvalues come from cyclic Jacobi rotations; the projection repair is computed by
alternating projections, with correction terms, between the positive semidefinite and the unit-diagonal matrices.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

Matrix = list[list[float]]

SYMMETRY_TOL = 1e-9


def _as_matrix(matrix: Sequence[Sequence[float]]) -> Matrix:
    """The input as a square float matrix, symmetrised. Non-square and asymmetric inputs raise ValueError."""
    rows = [list(row) for row in matrix]
    n = len(rows)
    if n == 0:
        raise ValueError("the matrix needs at least one row")
    if any(len(row) != n for row in rows):
        raise ValueError("the matrix is not square: every row must have as many entries as there are rows")
    out = [[float(x) for x in row] for row in rows]
    for i in range(n):
        for j in range(i + 1, n):
            if abs(out[i][j] - out[j][i]) > SYMMETRY_TOL:
                raise ValueError("the matrix is not symmetric: entries m[i][j] and m[j][i] differ by more than 1e-9")
    return [[(out[i][j] + out[j][i]) / 2.0 for j in range(n)] for i in range(n)]


def _eigh(a: Matrix) -> tuple[list[float], Matrix]:
    """Eigenvalues and eigenvectors (as columns) of a symmetric matrix, by cyclic Jacobi rotations."""
    n = len(a)
    m = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(100):
        off = math.sqrt(sum(m[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        scale = math.sqrt(sum(m[i][j] ** 2 for i in range(n) for j in range(n)))
        if off <= 1e-15 * max(scale, 1e-300):
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if m[p][q] == 0.0:
                    continue
                theta = (m[q][q] - m[p][p]) / (2.0 * m[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    mkp, mkq = m[k][p], m[k][q]
                    m[k][p] = c * mkp - s * mkq
                    m[k][q] = s * mkp + c * mkq
                for k in range(n):
                    mpk, mqk = m[p][k], m[q][k]
                    m[p][k] = c * mpk - s * mqk
                    m[q][k] = s * mpk + c * mqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp - s * vkq
                    v[k][q] = s * vkp + c * vkq
    return [m[i][i] for i in range(n)], v


def _rebuild(values: list[float], vectors: Matrix) -> Matrix:
    """V diag(values) V^T, for eigenvectors stored as the columns of vectors."""
    n = len(values)
    return [[sum(vectors[i][k] * values[k] * vectors[j][k] for k in range(n)) for j in range(n)] for i in range(n)]


def _psd_projection(a: Matrix) -> Matrix:
    """Negative eigenvalues set to zero, then the matrix rebuilt from its eigenvectors; no rescaling."""
    values, vectors = _eigh(a)
    return _rebuild([max(x, 0.0) for x in values], vectors)


def _rescale(x: Matrix) -> Matrix:
    """D^(-1/2) X D^(-1/2) with D the diagonal of X: unit diagonal, and it keeps positive semidefiniteness."""
    d = [x[i][i] for i in range(len(x))]
    if any(value <= 0.0 for value in d):
        raise ValueError("a diagonal entry of the repaired matrix is not positive, so it cannot be rescaled")
    return [[x[i][j] / math.sqrt(d[i] * d[j]) for j in range(len(x))] for i in range(len(x))]


def _frobenius(a: Matrix, b: Matrix) -> float:
    return math.sqrt(sum((a[i][j] - b[i][j]) ** 2 for i in range(len(a)) for j in range(len(a))))


def min_eigenvalue(matrix: list[list[float]]) -> float:
    """The smallest eigenvalue of the symmetric matrix."""
    rows = [list(row) for row in matrix]
    n = len(rows)
    full = [[rows[i][j] if j <= i else rows[j][i] for j in range(n)] for i in range(n)]
    values, _ = _eigh(full)
    return min(values)


def is_psd(matrix: list[list[float]], tol: float = 1e-10) -> bool:
    """True when every eigenvalue of the symmetric matrix is at least -tol."""
    return min_eigenvalue(matrix) >= -tol


def clip_repair(matrix: list[list[float]], floor: float = 0.0) -> list[list[float]]:
    """Eigenvalues below floor set to floor, the matrix rebuilt, then rescaled to unit diagonal."""
    a = _as_matrix(matrix)
    values, vectors = _eigh(a)
    x = _rebuild([max(value, floor) for value in values], vectors)
    return _rescale(x)


def projection_repair(matrix: list[list[float]], tol: float = 1e-10, max_iter: int = 500) -> list[list[float]]:
    """Alternating projections, with correction terms, onto the positive semidefinite and the unit-diagonal matrices."""
    a = _as_matrix(matrix)
    n = len(a)
    x = a
    corr_s = [[0.0] * n for _ in range(n)]
    corr_u = [[0.0] * n for _ in range(n)]
    for _ in range(max_iter):
        y = _psd_projection([[x[i][j] + corr_s[i][j] for j in range(n)] for i in range(n)])
        corr_s = [[x[i][j] + corr_s[i][j] - y[i][j] for j in range(n)] for i in range(n)]
        new_x = [[y[i][j] + corr_u[i][j] for j in range(n)] for i in range(n)]
        for i in range(n):
            new_x[i][i] = 1.0
        corr_u = [[y[i][j] + corr_u[i][j] - new_x[i][j] for j in range(n)] for i in range(n)]
        gap = _frobenius(new_x, y)
        step = _frobenius(new_x, x)
        x = new_x
        if gap <= tol and step <= tol:
            break
    return x


def comparison_weights(corr: list[list[float]], vols: list[float]) -> list[float]:
    """Weights proportional to the solution of (S C S) x = 1, normalised to sum to one; S = diag(vols)."""
    c = _as_matrix(corr)
    n = len(c)
    if len(vols) != n:
        raise ValueError("the volatilities must have one entry per row of the correlation matrix")
    if not all(float(v) > 0.0 for v in vols):
        raise ValueError("every volatility must be strictly positive")
    sigma = [[float(vols[i]) * c[i][j] * float(vols[j]) for j in range(n)] for i in range(n)]
    aug = [[*sigma[i], 1.0] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        aug[col], aug[pivot] = aug[pivot], aug[col]
        for r in range(n):
            if r != col:
                factor = aug[r][col] / aug[col][col]
                aug[r] = [a - factor * b for a, b in zip(aug[r], aug[col], strict=True)]
    solution = [aug[i][n] / aug[i][i] for i in range(n)]
    total = sum(solution)
    return [x / total for x in solution]
