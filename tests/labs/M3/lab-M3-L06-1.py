"""M3 L06 lab 1: the singular value decomposition, checked on seeded matrices.

SIMULATED: every matrix is generated here from a seeded generator (numpy default_rng). No data are read.
Units: none (dimensionless matrix entries). Tolerances are absolute and stated in each printed line.

For each of five seeds, two matrices are checked: a 4x3 matrix and a 3x4 matrix. For each one the lab
computes the full SVD with numpy.linalg.svd and checks the statements of Theorems 2.1 and 2.2 and
Proposition 2.4 numerically: U and V are orthogonal, A = U S V^T, the squared singular values equal the
eigenvalues of A^T A, and the sum of the squared singular values equals the squared Frobenius norm of A.
NumPy's SVD and eigenvalue routines are used only to produce the numbers that these identities are checked
against; no quantity is defined by them. A planted rank-2 matrix shows the numerical rank, and a sign flip
of one singular-vector pair shows that the vectors are not unique. Standard library and NumPy only. No
randomness outside the seeded generator, and no network access.
"""

from __future__ import annotations

import numpy as np

SEEDS = range(5)
TOL = 1e-10


def svd_residuals(a: np.ndarray) -> tuple[float, float, float, float, float]:
    """Return the five residuals for one matrix A: orth(U), orth(V), reconstruction, eigen gap, Frobenius gap."""
    u, s, vt = np.linalg.svd(a, full_matrices=True)
    m, n = a.shape
    k = min(m, n)
    sigma = np.zeros((m, n))
    sigma[:k, :k] = np.diag(s)
    v = vt.T
    eig = np.linalg.eigvalsh(a.T @ a)[::-1]  # eigenvalues of the n x n Gram matrix, descending
    orth_u = float(np.max(np.abs(u.T @ u - np.eye(m))))
    orth_v = float(np.max(np.abs(v.T @ v - np.eye(n))))
    recon = float(np.max(np.abs(u @ sigma @ v.T - a)))
    eig_gap = float(np.max(np.abs(s**2 - eig[:k])))
    frob_gap = abs(float(np.sum(s**2)) - float(np.sum(a * a)))
    return orth_u, orth_v, recon, eig_gap, frob_gap


def main() -> None:
    worst = [0.0, 0.0, 0.0, 0.0, 0.0]
    count = 0
    for seed in SEEDS:
        for a in (
            np.random.default_rng(seed).normal(size=(4, 3)),
            np.random.default_rng(100 + seed).normal(size=(3, 4)),
        ):
            residuals = svd_residuals(a)
            worst = [max(w, r) for w, r in zip(worst, residuals, strict=True)]
            count += 1
    print(f"matrices checked: {count} (5 seeds, shapes 4x3 and 3x4)")
    print(f"U and V orthogonal to 1e-12: {max(worst[0], worst[1]) < 1e-12}")
    print(f"A = U S V^T to 1e-12: {worst[2] < 1e-12}")
    print(f"squared singular values equal eigenvalues of A^T A to {TOL:g}: {worst[3] < TOL}")
    print(f"sum of squared singular values equals squared Frobenius norm to {TOL:g}: {worst[4] < TOL}")

    a0 = np.random.default_rng(0).normal(size=(4, 3))
    s0 = np.linalg.svd(a0, compute_uv=False)
    print(f"singular values of the seed-0 4x3 matrix, descending: {s0[0]:.4f} {s0[1]:.4f} {s0[2]:.4f}")

    planted = np.random.default_rng(7).normal(size=(4, 2)) @ np.random.default_rng(8).normal(size=(2, 3))
    s_planted = np.linalg.svd(planted, compute_uv=False)
    numerical_rank = int(np.sum(s_planted > 1e-10 * s_planted[0]))
    print(f"planted rank-2 4x3 matrix: singular values above 1e-10 relative: {numerical_rank}")

    u, s, vt = np.linalg.svd(a0, full_matrices=True)
    flipped_u = u.copy()
    flipped_vt = vt.copy()
    flipped_u[:, 0] *= -1.0
    flipped_vt[0, :] *= -1.0
    sigma = np.zeros(a0.shape)
    sigma[: len(s), : len(s)] = np.diag(s)
    still_a = np.max(np.abs(flipped_u @ sigma @ flipped_vt - a0)) < 1e-12
    print(f"flipping the signs of the first singular pair still reconstructs A: {bool(still_a)}")


main()
