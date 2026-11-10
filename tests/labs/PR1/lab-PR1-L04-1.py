"""Lab 4: Covariance shrinkage and eigenvalue regularization.

Illustrative inputs in floating-point arithmetic.
Demonstrates singularity in the sample covariance when T < N (rank deficiency)
and proves that linear shrinkage toward the scaled identity target guarantees
strict positive definiteness with smallest eigenvalue bounded by delta * tr(S)/N.
"""

from __future__ import annotations

import math


def jacobi_eigenvalues(a_mat: list[list[float]], tol: float = 1e-12, max_iter: int = 100) -> list[float]:
    """Compute eigenvalues of a real symmetric matrix via Jacobi rotations."""
    n = len(a_mat)
    s_mat = [row[:] for row in a_mat]
    for _ in range(max_iter):
        max_val = 0.0
        p, q = 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                if abs(s_mat[i][j]) > max_val:
                    max_val = abs(s_mat[i][j])
                    p, q = i, j
        if max_val < tol:
            break
        diff = s_mat[q][q] - s_mat[p][p]
        if abs(s_mat[p][q]) < tol:
            continue
        theta = 0.5 * math.atan2(2 * s_mat[p][q], diff)
        c = math.cos(theta)
        s = math.sin(theta)

        s_pp = c * c * s_mat[p][p] - 2 * s * c * s_mat[p][q] + s * s * s_mat[q][q]
        s_qq = s * s * s_mat[p][p] + 2 * s * c * s_mat[p][q] + c * c * s_mat[q][q]
        s_mat[p][q] = s_mat[q][p] = 0.0
        s_mat[p][p] = s_pp
        s_mat[q][q] = s_qq
        for r in range(n):
            if r != p and r != q:
                s_rp = c * s_mat[r][p] - s * s_mat[r][q]
                s_rq = s * s_mat[r][p] + c * s_mat[r][q]
                s_mat[r][p] = s_mat[p][r] = s_rp
                s_mat[r][q] = s_mat[q][r] = s_rq

    return sorted(s_mat[i][i] for i in range(n))


def main() -> None:
    # Rank-deficient return panel: T = 3 observations for N = 4 assets
    # Sample covariance has at most rank T - 1 = 2 < 4
    x_returns = [
        [0.04, 0.01, -0.02, 0.03],
        [-0.01, 0.03, 0.04, -0.02],
        [0.03, -0.02, 0.01, 0.05],
    ]
    t_obs = len(x_returns)
    n_assets = len(x_returns[0])

    means = [sum(x_returns[t][i] for t in range(t_obs)) / t_obs for i in range(n_assets)]
    s_cov = [[0.0] * n_assets for _ in range(n_assets)]
    for t in range(t_obs):
        for i in range(n_assets):
            for j in range(n_assets):
                s_cov[i][j] += (x_returns[t][i] - means[i]) * (x_returns[t][j] - means[j])
    for i in range(n_assets):
        for j in range(n_assets):
            s_cov[i][j] /= t_obs - 1

    eigs_s = jacobi_eigenvalues(s_cov)
    tr_s = sum(s_cov[i][i] for i in range(n_assets))
    target_scale = tr_s / n_assets

    delta = 0.25
    s_shrunk = [
        [(1.0 - delta) * s_cov[i][j] + (delta * target_scale if i == j else 0.0) for j in range(n_assets)]
        for i in range(n_assets)
    ]
    eigs_shrunk = jacobi_eigenvalues(s_shrunk)

    print("Eigenvalues of S:", [round(x, 6) for x in eigs_s])
    print("Smallest eigenvalue of S:", round(eigs_s[0], 6))
    print("Trace of S:", round(tr_s, 6))
    print(
        "Theoretical minimum eigenvalue delta * tr(S)/N:",
        round(delta * target_scale, 6),
    )
    print("Eigenvalues of shrunk matrix:", [round(x, 6) for x in eigs_shrunk])
    print("Smallest eigenvalue after shrinkage:", round(eigs_shrunk[0], 6))


main()
