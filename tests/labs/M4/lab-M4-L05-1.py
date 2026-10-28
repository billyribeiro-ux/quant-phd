"""M4 L05 lab 1: the sample covariance matrix of a seeded two-asset Gaussian draw, against the generating matrix.

Inputs are simulated, not data. Two standard normal streams come from random.Random(20260501).gauss, with the
pair (Z1, Z2) drawn in that order for each observation. Asset 1 has standard deviation S1 = 0.02 and asset 2 has
S2 = 0.03 (returns as decimals), and the correlation is RHO = 0.6. The construction is
X1 = S1 Z1 and X2 = S2 (RHO Z1 + sqrt(1 - RHO^2) Z2), which gives the generating covariance matrix
Sigma = [[S1^2, RHO S1 S2], [RHO S1 S2, S2^2]]. The first 100 observations are a prefix of the 20000-observation run.

Part A: the generating matrix, then the sample covariance matrix with divisor n - 1 for n = 100 and n = 20000, and the
largest absolute entry error |S_ij - Sigma_ij| for each n.
Part B: the sample correlation for n = 20000, against RHO.
Part C: the quadratic form w^T S w for the sample matrix S of n = 20000 and nine directions w = (cos a, sin a), with
a = k pi / 8 for k = 0 to 8. The printed flag says whether every value is nonnegative.
"""

from __future__ import annotations

import math
import random

S1 = 0.02
S2 = 0.03
RHO = 0.6
SEED = 20260501
DIRECTIONS = 9


def draws(n: int, seed: int) -> list[tuple[float, float]]:
    """n observations (X1, X2) of the two-asset Gaussian construction, from a generator seeded with seed."""
    rng = random.Random(seed)
    out: list[tuple[float, float]] = []
    for _ in range(n):
        z1 = rng.gauss(0.0, 1.0)
        z2 = rng.gauss(0.0, 1.0)
        out.append((S1 * z1, S2 * (RHO * z1 + math.sqrt(1.0 - RHO * RHO) * z2)))
    return out


def sample_cov(xs: list[tuple[float, float]]) -> list[list[float]]:
    """The 2 by 2 sample covariance matrix with divisor n - 1, computed from the means."""
    n = len(xs)
    m1 = sum(x for x, _ in xs) / n
    m2 = sum(y for _, y in xs) / n
    s11 = sum((x - m1) ** 2 for x, _ in xs) / (n - 1)
    s22 = sum((y - m2) ** 2 for _, y in xs) / (n - 1)
    s12 = sum((x - m1) * (y - m2) for x, y in xs) / (n - 1)
    return [[s11, s12], [s12, s22]]


def quadratic_form(matrix: list[list[float]], w: tuple[float, float]) -> float:
    """w^T M w for a 2 by 2 matrix M and a vector w."""
    return sum(w[i] * matrix[i][j] * w[j] for i in range(2) for j in range(2))


def max_entry_error(a: list[list[float]], b: list[list[float]]) -> float:
    """The largest absolute difference between corresponding entries of two 2 by 2 matrices."""
    return max(abs(a[i][j] - b[i][j]) for i in range(2) for j in range(2))


def main() -> None:
    """Print Parts A, B and C. The seed is fixed, so every run prints the same lines."""
    sigma = [[S1 * S1, RHO * S1 * S2], [RHO * S1 * S2, S2 * S2]]
    print("Part A: generating matrix and sample covariance matrices")
    print(f"sigma_11 {sigma[0][0]:.8f} sigma_12 {sigma[0][1]:.8f} sigma_22 {sigma[1][1]:.8f}")
    sample_20000: list[tuple[float, float]] = []
    for n in (100, 20000):
        xs = draws(n, SEED)
        if n == 20000:
            sample_20000 = xs
        s = sample_cov(xs)
        print(f"n {n} s_11 {s[0][0]:.8f} s_12 {s[0][1]:.8f} s_22 {s[1][1]:.8f}")
        print(f"n {n} max_entry_error {max_entry_error(s, sigma):.8f}")

    print("Part B: sample correlation at n = 20000 against RHO")
    s = sample_cov(sample_20000)
    corr = s[0][1] / math.sqrt(s[0][0] * s[1][1])
    print(f"n 20000 sample_correlation {corr:.6f} rho {RHO:.6f} error {corr - RHO:.6f}")

    print("Part C: quadratic form w^T S w for nine directions, n = 20000")
    values: list[float] = []
    for k in range(DIRECTIONS):
        angle = k * math.pi / 8
        w = (math.cos(angle), math.sin(angle))
        value = quadratic_form(s, w)
        values.append(value)
        print(f"k {k} w1 {w[0]:.6f} w2 {w[1]:.6f} quadratic_form {value:.10f}")
    print(f"all_nonnegative {all(v >= 0 for v in values)}")


main()
