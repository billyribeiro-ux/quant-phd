"""M3 lab L04: the spectral theorem checked on seeded random symmetric matrices.

SIMULATED: yes. The sample is 200 random symmetric 4 by 4 matrices, drawn from numpy's seeded generator
with seed 2604. Every count below is about this sample and the eigenvector pairs it contains. The checks
use a tolerance of 1e-10 and print True, False or a count, never a raw residual, because a raw residual
depends on the machine. The one number printed for the contrast matrix is an inner product rounded to four
decimals.

numpy.linalg.eigh is the routine whose output the lab checks. It is not the definition of any quantity on
the page: the spectral theorem asserts the orthogonality and the reconstruction that the lab tests.
numpy.linalg.eigvals is a general solver that makes no symmetry assumption; the lab uses it to check that
the spectrum of each sample is real. The two contrast matrices are fixed by hand. They show that the
symmetric hypothesis matters: they are not part of the sample.
"""

from __future__ import annotations

import numpy as np

SEED = 2604
N_MATRICES = 200
SIZE = 4
TOL = 1e-10
GAP = 1e-6


def symmetric_sample(rng: np.random.Generator) -> np.ndarray:
    """A random symmetric SIZE by SIZE matrix: the average of a Gaussian matrix and its transpose."""
    g = rng.standard_normal((SIZE, SIZE))
    return (g + g.T) / 2.0


def residual_ok(a: np.ndarray, values: np.ndarray, vectors: np.ndarray) -> bool:
    """True when every pair (w_j, q_j) from eigh satisfies ||A q_j - w_j q_j||_max below TOL."""
    worst = max(float(np.max(np.abs(a @ vectors[:, j] - values[j] * vectors[:, j]))) for j in range(SIZE))
    return worst < TOL


def main() -> None:
    rng = np.random.default_rng(SEED)
    orthogonal = reconstructs = residuals = real_spectrum = 0
    pairs = orthogonal_pairs = 0
    eye = np.eye(SIZE)
    for _ in range(N_MATRICES):
        a = symmetric_sample(rng)
        values, q = np.linalg.eigh(a)
        orthogonal += float(np.max(np.abs(q.T @ q - eye))) < TOL
        reconstructs += float(np.max(np.abs(q @ np.diag(values) @ q.T - a))) < TOL
        residuals += residual_ok(a, values, q)
        general = np.linalg.eigvals(a)
        real_spectrum += float(np.max(np.abs(general.imag))) < TOL
        for i in range(SIZE):
            for j in range(i + 1, SIZE):
                if abs(values[i] - values[j]) > GAP:
                    pairs += 1
                    orthogonal_pairs += abs(float(q[:, i] @ q[:, j])) < TOL

    print(f"seeded symmetric {SIZE} by {SIZE} matrices: {N_MATRICES}")
    print(f"Q^T Q equals I to {TOL:g} (orthogonal eigenvector matrix): {orthogonal} of {N_MATRICES}")
    print(f"Q diag(w) Q^T reconstructs A to {TOL:g}: {reconstructs} of {N_MATRICES}")
    print(f"every eigenpair residual is below {TOL:g}: {residuals} of {N_MATRICES}")
    print(f"general eigvals has imaginary part below {TOL:g} (real spectrum): {real_spectrum} of {N_MATRICES}")
    print(f"eigenvector pairs with eigenvalues more than {GAP:g} apart: {pairs}")
    print(f"of these pairs, orthogonal to {TOL:g}: {orthogonal_pairs} of {pairs}")

    rotation = np.array([[0.0, -1.0], [1.0, 0.0]])
    rot_imag = sorted(abs(float(v.imag)) for v in np.linalg.eigvals(rotation))
    print(
        f"rotation by 90 degrees, [[0, -1], [1, 0]]: both eigenvalues have imaginary part of size 1: "
        f"{all(abs(x - 1.0) < TOL for x in rot_imag)}"
    )

    shear = np.array([[1.0, 2.0], [0.0, 3.0]])
    _, vecs = np.linalg.eig(shear)
    dot = float(vecs[:, 0] @ vecs[:, 1])
    print(f"normalised eigenvectors of [[1, 2], [0, 3]] have |inner product| {abs(dot):.4f}")


main()
