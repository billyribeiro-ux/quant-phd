"""M3 L07 lab 1: the projection matrix and the normal equations on a SIMULATED regression.

SIMULATED: the 12 observations and the response are generated here from a seeded generator (seed 7). No data
are read. Units: the response and the fitted values are in the same arbitrary units; no unit is claimed.

The design matrix A has full column rank (an intercept and two regressors). The lab checks, to the tolerances
printed, the statements of Theorems 1.2, 1.3 and 2.2 and Remark 1.4: the projection matrix
P = A (A^T A)^{-1} A^T is symmetric and idempotent, Py equals A beta where beta solves the normal equations
A^T A beta = A^T y, the residual is orthogonal to every column of A, and the Pythagorean identity holds. The
coefficients are also compared with NumPy's least-squares routine, used here only as an independent direct solver.
A last part duplicates a column: then A^T A is singular, two different coefficient vectors give the same fitted
values, and the lab reports the rank of A^T A.
Standard library and NumPy only. No network access.
"""

from __future__ import annotations

import numpy as np

TOL = 1e-9


def main() -> None:
    rng = np.random.default_rng(7)
    n = 12
    x1 = rng.normal(size=n)
    x2 = rng.normal(size=n)
    noise = rng.normal(scale=0.3, size=n)
    y = 1.5 + 0.8 * x1 - 0.4 * x2 + noise
    a = np.column_stack([np.ones(n), x1, x2])

    gram = a.T @ a
    p_matrix = a @ np.linalg.solve(gram, a.T)
    beta = np.linalg.solve(gram, a.T @ y)
    fitted = p_matrix @ y
    residual = y - fitted

    print(f"P symmetric to {TOL:g}: {bool(np.max(np.abs(p_matrix - p_matrix.T)) < TOL)}")
    print(f"P idempotent (P P = P) to {TOL:g}: {bool(np.max(np.abs(p_matrix @ p_matrix - p_matrix)) < TOL)}")
    print(f"P y equals A beta to {TOL:g}: {bool(np.max(np.abs(fitted - a @ beta)) < TOL)}")
    print(f"residual orthogonal to every column of A to {TOL:g}: {bool(np.max(np.abs(a.T @ residual)) < TOL)}")
    print(
        f"Pythagorean identity |y|^2 = |Py|^2 + |residual|^2 to {TOL:g}: "
        f"{bool(abs(y @ y - fitted @ fitted - residual @ residual) < TOL)}"
    )

    direct = np.linalg.lstsq(a, y, rcond=None)[0]
    print(
        f"normal-equation coefficients agree with the direct least-squares solver to {TOL:g}: "
        f"{bool(np.max(np.abs(beta - direct)) < TOL)}"
    )
    print(f"coefficients (intercept, x1, x2), printed to 4 decimals: {beta[0]:.4f} {beta[1]:.4f} {beta[2]:.4f}")
    print(f"residual norm, printed to 4 decimals: {np.linalg.norm(residual):.4f}")

    dup = np.column_stack([a[:, 0], a[:, 1], a[:, 1]])
    rank = int(np.linalg.matrix_rank(dup.T @ dup))
    print(f"rank of A^T A with a duplicated column: {rank} (of 3)")
    beta_one = np.linalg.lstsq(dup, y, rcond=None)[0]
    beta_two = beta_one + np.array([0.0, 1.0, -1.0]) * 0.5
    same_fit = bool(np.max(np.abs(dup @ beta_one - dup @ beta_two)) < TOL)
    print(f"two coefficient vectors that differ by a null direction give the same fitted values: {same_fit}")


main()
