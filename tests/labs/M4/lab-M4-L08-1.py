"""M4 lab L08: a linear image of a standard normal vector, checked against its covariance A A^T.

SIMULATED: the draws come from a seeded generator; no data is used.
Standard library only (random). The mean is mu = (1, -2) and the factor is A = [[2, 0], [1, 1]], so the
target covariance is Sigma = A A^T = [[4, 2], [2, 2]]. Part A uses exact integer matrix arithmetic. It checks
that A A^T equals Sigma, that B = A Q, with Q the rotation [[0, -1], [1, 0]], also has B B^T equal to Sigma,
and that A^T A is a different matrix. Part B draws n = 20000 standard normal vectors Z (two random.gauss(0, 1)
values per draw, seed 2026), forms X = mu + A Z and Y = mu + B Z from the same Z, and prints the sample mean of X
beside mu, the sample covariance matrix of X (divisor n - 1) beside Sigma, the largest entry gaps of that matrix
from Sigma and from A^T A, and the sample covariance matrix of Y with its largest entry gap from Sigma.
A sample is one random run, so its entries estimate the exact entries and are not equal to them.
"""

from __future__ import annotations

import random
from collections.abc import Sequence

Matrix = tuple[tuple[int, ...], ...]

SEED = 2026
N_DRAWS = 20000
MU: tuple[float, float] = (1.0, -2.0)
A: Matrix = ((2, 0), (1, 1))
Q: Matrix = ((0, -1), (1, 0))


def matmul(x: Matrix, y: Matrix) -> Matrix:
    """Exact product of two integer matrices given as tuples of rows."""
    inner = len(y)
    return tuple(tuple(sum(x[i][k] * y[k][j] for k in range(inner)) for j in range(len(y[0]))) for i in range(len(x)))


def transpose(x: Matrix) -> Matrix:
    """Transpose of an integer matrix given as tuples of rows."""
    return tuple(tuple(row[j] for row in x) for j in range(len(x[0])))


def affine(x: Matrix, z: Sequence[float], mu: Sequence[float]) -> list[float]:
    """The vector mu + x z, where x is a 2 by 2 integer matrix and z has two coordinates."""
    return [mu[i] + sum(x[i][k] * z[k] for k in range(len(z))) for i in range(len(x))]


def sample_mean(rows: Sequence[Sequence[float]]) -> list[float]:
    """Coordinate-wise sample mean of a list of vectors."""
    n = len(rows)
    return [sum(r[i] for r in rows) / n for i in range(len(rows[0]))]


def sample_covariance(rows: Sequence[Sequence[float]]) -> list[list[float]]:
    """Sample covariance matrix of a list of vectors, with divisor n - 1."""
    n = len(rows)
    mean = sample_mean(rows)
    d = len(mean)
    return [[sum((r[i] - mean[i]) * (r[j] - mean[j]) for r in rows) / (n - 1) for j in range(d)] for i in range(d)]


def largest_gap(sample: Sequence[Sequence[float]], exact: Matrix) -> float:
    """Largest absolute entry-wise difference between a sample matrix and an exact integer matrix."""
    return max(abs(sample[i][j] - exact[i][j]) for i in range(len(exact)) for j in range(len(exact)))


def fmt(m: Sequence[Sequence[float]]) -> str:
    """Format a 2 by 2 matrix with four decimals per entry."""
    return "((" + f"{m[0][0]:.4f}, {m[0][1]:.4f}" + "), (" + f"{m[1][0]:.4f}, {m[1][1]:.4f}" + "))"


def main() -> None:
    sigma = matmul(A, transpose(A))
    b = matmul(A, Q)
    print(f"part A: A A^T = {sigma} = Sigma")
    print(f"part A: B = A Q = {b}, and B B^T equals Sigma: {matmul(b, transpose(b)) == sigma}")
    ata = matmul(transpose(A), A)
    print(f"part A: A^T A = {ata}, and A^T A equals Sigma: {ata == sigma}")

    rng = random.Random(SEED)
    rows_a: list[list[float]] = []
    rows_b: list[list[float]] = []
    for _ in range(N_DRAWS):
        z = [rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0)]
        rows_a.append(affine(A, z, MU))
        rows_b.append(affine(b, z, MU))
    mean_a = sample_mean(rows_a)
    cov_a = sample_covariance(rows_a)
    cov_b = sample_covariance(rows_b)
    print(f"part B: sample mean of X = ({mean_a[0]:.4f}, {mean_a[1]:.4f}), against mu = (1, -2)")
    print(f"part B: sample covariance of X = {fmt(cov_a)}, against Sigma = {sigma}")
    print(f"part B: largest entry gap of X's sample covariance from Sigma = {largest_gap(cov_a, sigma):.4f}")
    print(f"part B: largest entry gap of X's sample covariance from A^T A = {largest_gap(cov_a, ata):.4f}")
    print(f"part B: sample covariance of Y = {fmt(cov_b)}")
    print(f"part B: largest entry gap of Y's sample covariance from Sigma = {largest_gap(cov_b, sigma):.4f}")


main()
