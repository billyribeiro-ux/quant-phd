"""M3 L09 lab 1: clipping, rescaling and a closer correlation matrix, on fixed and seeded inputs.

Claims checked, each on the inputs named in the code:
1. C0, the 3x3 symmetric matrix with unit diagonal and off-diagonal entries 0.9, 0.9 and -0.9, is not
   positive semidefinite: x = (1, -1, -1) gives x^T C0 x = -2.4 < 0.
2. Clipping the eigenvalues of C0 at zero gives a symmetric PSD matrix B. The squared Frobenius distance
   ||C0 - B||_F^2 equals the sum of the squared negative eigenvalues of C0 (Proposition 3.3 of the lesson).
3. Rescaling B to unit diagonal gives a correlation matrix R: symmetric, unit diagonal, PSD (Proposition 3.4).
4. For 40 matrices drawn from a generator seeded with 20261028 (SIMULATED: off-diagonal entries 0.5 plus
   symmetrised Gaussian noise, each raw entry with standard deviation 0.35; unit diagonal; size 5), the
   non-PSD matrices are repaired two ways. Clip-and-rescale gives R. Alternating projections (clip at zero,
   set the diagonal to one, repeat until the change is below 1e-12, at most 500 steps) gives W. The lab counts
   how often W passes is_correlation (symmetric and unit diagonal to 1e-12, smallest eigenvalue at least -1e-8),
   and how often W passes it and ||A - W||_F is strictly less than ||A - R||_F.

Scope: the counts describe these 40 matrices and nothing more. The lab does not show that R or W is the
nearest correlation matrix to any input. It shows, to the tolerance of is_correlation, that R is not the nearest
correlation matrix to A in each instance where W passes is_correlation and is strictly closer to A than R, and it
prints how many instances those are.
Standard library and NumPy only. Fixed seed, no network access.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

FloatMatrix = npt.NDArray[np.float64]

TOL = 1e-12
FEASIBLE_TOL = 1e-8
NONPSD_TOL = 1e-9
MAX_ITER = 500
N_MATRICES = 40
SIZE = 5
SEED = 20261028


def correlation_3x3(a: float, b: float, c: float) -> FloatMatrix:
    """Return the 3x3 matrix with unit diagonal and off-diagonal entries a (1,2), b (1,3) and c (2,3)."""
    return np.array([[1.0, a, b], [a, 1.0, c], [b, c, 1.0]], dtype=np.float64)


def clip_eigenvalues(a: FloatMatrix, floor: float = 0.0) -> FloatMatrix:
    """Return Q max(Lambda, floor) Q^T for the spectral decomposition a = Q Lambda Q^T of a symmetric matrix a."""
    lam, q = np.linalg.eigh(a)
    return np.asarray((q * np.maximum(lam, floor)) @ q.T, dtype=np.float64)


def rescale_to_unit_diagonal(b: FloatMatrix) -> FloatMatrix:
    """Return D^(-1/2) b D^(-1/2), where D is the diagonal of b. Every diagonal entry of b must be positive."""
    d = np.sqrt(np.diag(b))
    if np.any(d <= 0.0):
        raise ValueError("rescaling needs every diagonal entry to be positive")
    return np.asarray(b / np.outer(d, d), dtype=np.float64)


def alternating_projections(a: FloatMatrix) -> FloatMatrix:
    """Clip the eigenvalues at zero, then set the diagonal to one; repeat until the change is below TOL."""
    x = a.copy()
    y = x
    for _ in range(MAX_ITER):
        y = clip_eigenvalues(x)
        np.fill_diagonal(y, 1.0)
        if float(np.max(np.abs(y - x))) < TOL:
            break
        x = y
    return y


def is_correlation(a: FloatMatrix) -> bool:
    """True when a is symmetric and has unit diagonal to TOL, and its smallest eigenvalue is at least -FEASIBLE_TOL."""
    symmetric = float(np.max(np.abs(a - a.T))) < TOL
    unit = float(np.max(np.abs(np.diag(a) - 1.0))) < TOL
    psd = float(np.linalg.eigvalsh(a)[0]) >= -FEASIBLE_TOL
    return bool(symmetric and unit and psd)


def seeded_matrices(count: int, size: int, seed: int) -> list[FloatMatrix]:
    """Return count symmetric size x size matrices with unit diagonal and off-diagonal entries near 0.5."""
    rng = np.random.default_rng(seed)
    out: list[FloatMatrix] = []
    for _ in range(count):
        noise = rng.normal(0.0, 0.35, size=(size, size))
        noise = (noise + noise.T) / 2.0
        a = np.asarray(0.5 + noise, dtype=np.float64)
        np.fill_diagonal(a, 1.0)
        out.append(a)
    return out


def main() -> None:
    c0 = correlation_3x3(0.9, 0.9, -0.9)
    eig0 = np.linalg.eigvalsh(c0)
    x = np.array([1.0, -1.0, -1.0])
    quad = float(x @ c0 @ x)
    print(f"C0 eigenvalues, ascending: {eig0[0]:.6f} {eig0[1]:.6f} {eig0[2]:.6f}")
    print(f"witness x = (1, -1, -1): x^T C0 x = {quad:.6f}; C0 is not PSD: {quad < 0.0}")

    b = clip_eigenvalues(c0)
    dist2 = float(np.sum((c0 - b) ** 2))
    negative_sum = float(np.sum(np.minimum(eig0, 0.0) ** 2))
    b_psd = float(np.linalg.eigvalsh(b)[0]) >= -TOL
    print(f"B = clipped C0 is PSD (smallest eigenvalue at least -1e-12): {b_psd}")
    print(f"||C0 - B||_F^2 = {dist2:.10f}; sum of squared negative eigenvalues = {negative_sum:.10f}")

    r = rescale_to_unit_diagonal(b)
    print(f"R = rescaled B is a correlation matrix: {is_correlation(r)}")
    print("R entries, row by row:")
    for row in r:
        print("  " + " ".join(f"{value: .4f}" for value in row))

    nonpsd = 0
    feasible = 0
    closer = 0
    first = ""
    for index, a in enumerate(seeded_matrices(N_MATRICES, SIZE, SEED)):
        if float(np.linalg.eigvalsh(a)[0]) >= -NONPSD_TOL:
            continue
        nonpsd += 1
        repaired = rescale_to_unit_diagonal(clip_eigenvalues(a))
        alt = alternating_projections(a)
        d_rescale = float(np.linalg.norm(a - repaired))
        d_alt = float(np.linalg.norm(a - alt))
        if is_correlation(alt):
            feasible += 1
            if d_alt < d_rescale:
                closer += 1
        if not first:
            first = f"first non-PSD matrix (index {index}): ||A - R||_F = {d_rescale:.6f}, ||A - W||_F = {d_alt:.6f}"
    print(f"seeded {SIZE}x{SIZE} matrices: {N_MATRICES}; not PSD (smallest eigenvalue below -1e-9): {nonpsd}")
    print(
        "alternating-projection output passes is_correlation "
        f"(symmetric and unit diagonal to 1e-12, smallest eigenvalue at least -1e-8): {feasible} of {nonpsd}"
    )
    print(
        f"alternating-projection output passes is_correlation and is strictly closer to A than R: {closer} of {nonpsd}"
    )
    print(first)


main()
