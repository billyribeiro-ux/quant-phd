"""M3 lab L05: positive semidefiniteness tested by eigenvalues and by sampled quadratic forms.

SIMULATED: partly. Part A and Part B use fixed matrices and a fixed grid of angles, with no randomness.
Part C uses 500 Gram matrices B^T B and 200 sampled vectors per matrix, drawn from numpy's seeded
generator (seed 2604). A sample supports only the seeds and vectors it tests, so the statements printed
for Part C are about those 500 matrices and those 100000 quadratic forms, and about no other matrix or vector.

The verdicts use numpy.linalg.eigvalsh, a floating-point solver, with tolerance 1e-10. For a singular
matrix the computed smallest eigenvalue is a floating-point number near zero, so every test allows the tolerance.
The lab prints verdicts, counts and eigenvalues rounded to four decimals. For the singular matrix, a value within
1e-10 of zero is printed as 0.0000, so its unrounded value and its sign are never shown.
Standard library apart from numpy. No network access.
"""

from __future__ import annotations

import math

import numpy as np

SEED = 2604
TOL = 1e-10
N_GRAM = 500
N_VECTORS = 200
ANGLES = 360

# Part A: a symmetric matrix with positive diagonal that is not positive semidefinite.
COUNTER: list[list[int]] = [[1, 2], [2, 1]]
# Part D: B has rank 2, so the Gram matrix B^T B has a zero eigenvalue.
GRAM_RANK_DEFICIENT_FACTOR: list[list[float]] = [[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]]


def quadratic_form_int(a: list[list[int]], x: list[int]) -> int:
    """x^T A x for an integer matrix a and integer vector x, computed exactly."""
    n = len(x)
    return sum(x[i] * a[i][j] * x[j] for i in range(n) for j in range(n))


def gram(b: np.ndarray) -> np.ndarray:
    """The Gram matrix B^T B, which is symmetric."""
    product: np.ndarray = b.T @ b
    return product


def part_a() -> None:
    form = quadratic_form_int(COUNTER, [1, -1])
    print(f"quadratic form of [[1, 2], [2, 1]] at (1, -1), exact integer value: {form}")
    diagonal_positive = all(COUNTER[i][i] > 0 for i in range(2))
    print(f"diagonal entries of [[1, 2], [2, 1]] are both positive: {diagonal_positive}")
    values = np.linalg.eigvalsh(np.array(COUNTER, dtype=float))
    print(f"eigenvalues of [[1, 2], [2, 1]], sorted: {values[0]:.4f} {values[1]:.4f}")
    print(f"the eigenvalue test rejects it, since its smallest eigenvalue is below -1e-10: {values[0] < -TOL}")


def part_b() -> None:
    """Quadratic form of [[1, 2], [2, 1]] at the unit vector (cos t, sin t), over 360 equally spaced angles t.

    The form equals 1 + 2 sin(2t). Its exact minimum on the circle is -1, at t = 135 and t = 315 degrees, and it is
    zero at t = 105, 165, 285 and 345 degrees.
    """
    values = []
    for k in range(ANGLES):
        t = 2.0 * math.pi * k / ANGLES
        c, s = math.cos(t), math.sin(t)
        values.append(1.0 * c * c + 2.0 * 2.0 * c * s + 1.0 * s * s)
    negative = sum(v < -TOL for v in values)
    zero = sum(abs(v) <= TOL for v in values)
    print(f"grid angles with a negative form value: {negative} of {ANGLES}")
    print(f"grid angles with a form value of zero to 1e-10: {zero} of {ANGLES}")
    print(f"smallest form value on the grid: {min(values):.4f}")


def part_c() -> None:
    rng = np.random.default_rng(SEED)
    eigen_pass = form_pass = 0
    forms_checked = 0
    for _ in range(N_GRAM):
        b = rng.standard_normal((4, 3))
        a = gram(b)
        smallest = float(np.linalg.eigvalsh(a)[0])
        eigen_pass += smallest >= -TOL
        x = rng.standard_normal((N_VECTORS, 3))
        forms = np.einsum("ij,jk,ik->i", x, a, x)
        norms = np.einsum("ij,ij->i", x, x)
        forms_checked += N_VECTORS
        form_pass += int(np.sum(forms >= -TOL * norms))
    print(
        f"Gram matrices B^T B (B is 4 by 3, seeded) with smallest eigenvalue at least -1e-10: {eigen_pass} of {N_GRAM}"
    )
    print(f"sampled quadratic forms x^T A x at least -1e-10 times |x|^2: {form_pass} of {forms_checked}")


def part_d() -> None:
    b = np.array(GRAM_RANK_DEFICIENT_FACTOR)
    a = gram(b)
    values = np.linalg.eigvalsh(a)
    zero_count = int(np.sum(np.abs(values) <= TOL))
    print(
        f"Gram matrix of the rank 2 factor, eigenvalues sorted: "
        f"{0.0 if abs(values[0]) <= TOL else values[0]:.4f} {values[1]:.4f} {values[2]:.4f}"
    )
    print(f"eigenvalues with absolute value at most 1e-10: {zero_count}")
    print(f"the tolerance test accepts it as positive semidefinite: {bool(values[0] >= -TOL)}")


def main() -> None:
    part_a()
    part_b()
    part_c()
    part_d()


main()
