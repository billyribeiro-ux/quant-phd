"""M3 lab L03: eigenpairs, the identity AP = PD, and a matrix with too few eigenvectors.

SIMULATED: no. Every matrix is written out by hand and no random numbers are drawn.
The exact checks use Python integers, so their printed counts and True values are exact.
The floating-point checks use numpy.linalg.eig, numpy.linalg.eigvals, numpy.linalg.det and numpy.linalg.matrix_rank.
They are compared with a tolerance of 1e-12. The lab prints verdicts, eigenvalues rounded to four
decimals, and a rank, never a raw residual, because a raw residual depends on the machine. The lab supports
the statements for these three matrices only. It is not a proof, and no proof on the page depends on it.
"""

from __future__ import annotations

import numpy as np

TOL = 1e-12

# Upper triangular, so its eigenvalues are its diagonal entries 2, 3 and 5. The eigenvectors below
# are checked against the matrix, not taken from the triangular structure.
A_INT: list[list[int]] = [[2, 1, 0], [0, 3, 1], [0, 0, 5]]
# Columns of P are the eigenvectors for the eigenvalues in D, in the same order.
P_INT: list[list[int]] = [[1, 1, 1], [0, 1, 3], [0, 0, 6]]
D_INT: list[int] = [2, 3, 5]

# A matrix with eigenvalue 1 repeated twice and only one independent eigenvector.
B: np.ndarray = np.array([[1.0, 1.0], [0.0, 1.0]])


def matmul_int(x: list[list[int]], y: list[list[int]]) -> list[list[int]]:
    """Product of two integer matrices of compatible sizes, by the row-column rule."""
    inner = len(y)
    return [[sum(x[i][k] * y[k][j] for k in range(inner)) for j in range(len(y[0]))] for i in range(len(x))]


def column(m: list[list[int]], j: int) -> list[int]:
    """Column j of an integer matrix, as a list."""
    return [row[j] for row in m]


def det3_int(m: list[list[int]]) -> int:
    """Determinant of a 3 by 3 integer matrix, by cofactor expansion along the first row."""
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def exact_eigenpair_count(a: list[list[int]], p: list[list[int]], eigenvalues: list[int]) -> int:
    """Count the columns v of p for which a v equals lambda v exactly, with lambda the matching entry of eigenvalues."""
    count = 0
    for j, lam in enumerate(eigenvalues):
        v = column(p, j)
        av = [sum(a[i][k] * v[k] for k in range(3)) for i in range(3)]
        count += av == [lam * x for x in v]
    return count


def main() -> None:
    eigenpairs = exact_eigenpair_count(A_INT, P_INT, D_INT)
    print(f"exact eigenpairs (integer arithmetic): {eigenpairs} of 3 satisfy A v = lambda v")

    ap = matmul_int(A_INT, P_INT)
    pd = [[P_INT[i][j] * D_INT[j] for j in range(3)] for i in range(3)]
    print(f"A P equals P D exactly (integer arithmetic): {ap == pd}")
    print(f"det P = {det3_int(P_INT)}, which is nonzero, so P is invertible")

    a = np.array(A_INT, dtype=float)
    values, vectors = np.linalg.eig(a)
    order = np.argsort(values.real)
    sorted_values = values.real[order]
    print(f"numpy eigenvalues of A, sorted: {sorted_values[0]:.4f} {sorted_values[1]:.4f} {sorted_values[2]:.4f}")
    residuals = [np.max(np.abs(a @ vectors[:, j] - values[j] * vectors[:, j])) for j in range(3)]
    print(f"every numpy eigenpair of A has residual below 1e-12: {all(r < TOL for r in residuals)}")
    print(f"det(A - 3I) is zero to 1e-12, so 3 is an eigenvalue: {abs(np.linalg.det(a - 3.0 * np.eye(3))) < TOL}")

    values_b = np.linalg.eigvals(B)
    print(f"eigenvalues of B = [[1, 1], [0, 1]], sorted: {min(values_b.real):.4f} {max(values_b.real):.4f}")
    rank = int(np.linalg.matrix_rank(B - np.eye(2)))
    print(f"rank of B - I: {rank}, so the eigenspace for 1 has dimension {2 - rank}")
    print(f"eigenspace dimension is below the repeated root 2, so B has no basis of eigenvectors: {2 - rank < 2}")


main()
