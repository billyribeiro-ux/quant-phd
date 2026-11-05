"""Rung 1 worked example: repair one pairwise-estimated matrix by eigenvalue clipping, step by step.

SIMULATED: the three off-diagonal entries are set by hand for this example. They are not estimated from data.
Standard library only. Every number printed is computed from unrounded values; printing rounds it for display.
"""

import math

Matrix = list[list[float]]


def jacobi_eigen(a: Matrix) -> tuple[list[float], Matrix]:
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


def main() -> None:
    # Step 1. The pairwise estimates form a symmetric matrix with unit diagonal. The entries are SIMULATED.
    corr = [[1.0, 0.8, -0.5], [0.8, 1.0, 0.6], [-0.5, 0.6, 1.0]]
    n = len(corr)
    # Step 2. Eigenvalues and orthonormal eigenvectors. The eigenvalues of a symmetric matrix are real.
    values, vectors = jacobi_eigen(corr)
    print("eigenvalues, sorted:", " ".join(f"{x:.6f}" for x in sorted(values)))
    # Step 3. The positive semidefinite check: every eigenvalue must be at least -tol. Here tol = 1e-10.
    smallest = min(values)
    print("smallest eigenvalue:", f"{smallest:.6f}", "| positive semidefinite at tol 1e-10:", smallest >= -1e-10)
    # Step 4. Clipping: each eigenvalue below the floor 0 becomes 0; the matrix is rebuilt from the same eigenvectors.
    clipped = [max(x, 0.0) for x in values]
    rebuilt = [[sum(vectors[i][k] * clipped[k] * vectors[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
    print("rebuilt diagonal:", " ".join(f"{rebuilt[i][i]:.6f}" for i in range(n)))
    # Step 5. Rescaling: entry (i, j) is divided by sqrt(d_i d_j), where d is the diagonal of the rebuilt matrix.
    # The diagonal becomes 1, and D^(-1/2) X D^(-1/2) stays positive semidefinite when every d_i is positive
    # (result A2 of the appendix).
    d = [rebuilt[i][i] for i in range(n)]
    repaired = [[rebuilt[i][j] / math.sqrt(d[i] * d[j]) for j in range(n)] for i in range(n)]
    for row in repaired:
        print("repaired row:", " ".join(f"{x:.6f}" for x in row))
    # Step 6. Checks on the repaired matrix: the largest diagonal deviation from 1, and its positive semidefinite check.
    deviation = max(abs(repaired[i][i] - 1.0) for i in range(n))
    new_values, _ = jacobi_eigen(repaired)
    print("largest deviation of the diagonal from 1:", f"{deviation:.6f}")
    print("positive semidefinite at tol 1e-9 after repair:", min(new_values) >= -1e-9)


main()
