"""Rung 3 reference numbers: the repairs, their distances from the input, and the determinant and weights of the input.

SIMULATED: the four-by-four matrix and the volatilities are set by hand for this run. They are not estimated from data.
Standard library only. Copy this file into report/run_report.py, delete the six functions jacobi_eigen, psd_projection,
min_eigenvalue, clip_repair, projection_repair and comparison_weights, and import the four names min_eigenvalue,
clip_repair, projection_repair and comparison_weights from your covariance_doctor module. frobenius and determinant
stay. Your module must print the same lines.
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


def psd_projection(a: Matrix) -> Matrix:
    """The nearest positive semidefinite matrix in the Frobenius norm: negative eigenvalues set to 0, then rebuilt."""
    n = len(a)
    values, vectors = jacobi_eigen(a)
    clipped = [max(x, 0.0) for x in values]
    return [[sum(vectors[i][k] * clipped[k] * vectors[j][k] for k in range(n)) for j in range(n)] for i in range(n)]


def min_eigenvalue(a: Matrix) -> float:
    """The smallest eigenvalue of a symmetric matrix."""
    values, _ = jacobi_eigen(a)
    return min(values)


def clip_repair(a: Matrix) -> Matrix:
    """Eigenvalue clipping at 0, then rescaling to unit diagonal: D^(-1/2) X D^(-1/2) with D the diagonal of X."""
    n = len(a)
    values, vectors = jacobi_eigen(a)
    clipped = [max(x, 0.0) for x in values]
    x_matrix = [[sum(vectors[i][k] * clipped[k] * vectors[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
    d = [x_matrix[i][i] for i in range(n)]
    return [[x_matrix[i][j] / math.sqrt(d[i] * d[j]) for j in range(n)] for i in range(n)]


def projection_repair(a: Matrix, tol: float = 1e-10, max_iter: int = 500) -> Matrix:
    """Dykstra's alternating projections between the positive semidefinite and the unit-diagonal matrices."""
    n = len(a)
    x = [row[:] for row in a]
    corr_s = [[0.0] * n for _ in range(n)]
    corr_u = [[0.0] * n for _ in range(n)]
    for _ in range(max_iter):
        y = psd_projection([[x[i][j] + corr_s[i][j] for j in range(n)] for i in range(n)])
        corr_s = [[x[i][j] + corr_s[i][j] - y[i][j] for j in range(n)] for i in range(n)]
        new_x = [[y[i][j] + corr_u[i][j] for j in range(n)] for i in range(n)]
        for i in range(n):
            new_x[i][i] = 1.0
        corr_u = [[y[i][j] + corr_u[i][j] - new_x[i][j] for j in range(n)] for i in range(n)]
        gap = math.sqrt(sum((new_x[i][j] - y[i][j]) ** 2 for i in range(n) for j in range(n)))
        step = math.sqrt(sum((new_x[i][j] - x[i][j]) ** 2 for i in range(n) for j in range(n)))
        x = new_x
        if gap <= tol and step <= tol:
            break
    return x


def comparison_weights(corr: Matrix, vols: list[float]) -> list[float]:
    """Weights proportional to Sigma^(-1) 1, with Sigma = S C S and S = diag(vols), normalised to sum to 1."""
    n = len(corr)
    sigma = [[vols[i] * corr[i][j] * vols[j] for j in range(n)] for i in range(n)]
    aug = [[*sigma[i], 1.0] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        aug[col], aug[pivot] = aug[pivot], aug[col]
        for r in range(n):
            if r != col:
                factor = aug[r][col] / aug[col][col]
                aug[r] = [p - factor * q for p, q in zip(aug[r], aug[col], strict=True)]
    solution = [aug[i][n] / aug[i][i] for i in range(n)]
    total = sum(solution)
    return [x / total for x in solution]


def determinant(a: Matrix) -> float:
    """The determinant by Gaussian elimination with partial pivoting: the pivots' product, sign-flipped per swap."""
    n = len(a)
    m = [row[:] for row in a]
    det = 1.0
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))
        if m[pivot][col] == 0.0:
            return 0.0
        if pivot != col:
            m[col], m[pivot] = m[pivot], m[col]
            det = -det
        det *= m[col][col]
        for r in range(col + 1, n):
            factor = m[r][col] / m[col][col]
            m[r] = [p - factor * q for p, q in zip(m[r], m[col], strict=True)]
    return det


def frobenius(a: Matrix, b: Matrix) -> float:
    """The Frobenius distance: the square root of the sum of squared entry differences."""
    n = len(a)
    return math.sqrt(sum((a[i][j] - b[i][j]) ** 2 for i in range(n) for j in range(n)))


def main() -> None:
    # The illustrative input: a symmetric matrix with unit diagonal that is not positive semidefinite, and volatilities.
    corr = [
        [1.0, 0.7, 0.3, -0.6],
        [0.7, 1.0, 0.5, 0.4],
        [0.3, 0.5, 1.0, 0.2],
        [-0.6, 0.4, 0.2, 1.0],
    ]
    vols = [0.10, 0.20, 0.15, 0.30]
    n = len(corr)
    smallest = min_eigenvalue(corr)
    print("smallest eigenvalue:", f"{smallest:.6f}", "| positive semidefinite at tol 1e-10:", smallest >= -1e-10)
    clip = clip_repair(corr)
    proj = projection_repair(corr)
    dist_clip = frobenius(clip, corr)
    dist_proj = frobenius(proj, corr)
    print("distance from the input, clipping:", f"{dist_clip:.6f}")
    print("distance from the input, projection:", f"{dist_proj:.6f}")
    print("distance saved by projection over clipping:", f"{dist_clip - dist_proj:.6f}")
    print(
        "largest entry difference, projection minus clipping:",
        f"{max(abs(proj[i][j] - clip[i][j]) for i in range(n) for j in range(n)):.6f}",
    )
    print(
        "largest diagonal deviation: clipping",
        f"{max(abs(clip[i][i] - 1.0) for i in range(n)):.6f}",
        "| projection",
        f"{max(abs(proj[i][i] - 1.0) for i in range(n)):.6f}",
    )
    print("projection positive semidefinite at tol 1e-8:", min_eigenvalue(proj) >= -1e-8)
    print("determinant of the input:", f"{determinant(corr):.6f}")
    w_input = comparison_weights(corr, vols)
    print("weights, input:", " ".join(f"{x:.6f}" for x in w_input), "| sum", f"{sum(w_input):.6f}")


main()
