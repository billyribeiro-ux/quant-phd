"""Alternative (verifier round 9, slice d): correct implementation using an LDL^T factorisation, a heap-based 99% order
statistic and an exact Fraction index. Chi-square is the sum of nu squared standard normals, not gammavariate.
All inputs are SIMULATED.
"""

from __future__ import annotations

import heapq
import math
import random
from fractions import Fraction


def matched_scale(nu: int) -> float:
    if type(nu) is not int:
        raise ValueError("nu must be a whole number")
    if nu <= 2:
        raise ValueError("nu must be greater than 2")
    return (nu - 2) / nu


def _ldl_factor(cov: list[list[float]], n: int) -> list[list[float]]:
    if len(cov) != n or any(len(r) != n for r in cov):
        raise ValueError("cov must be a square matrix with one row and one column per position")
    for i in range(n):
        for j in range(i):
            if cov[i][j] != cov[j][i]:
                raise ValueError("cov must be symmetric")
    d = [0.0] * n
    lower = [[0.0] * n for _ in range(n)]
    for j in range(n):
        dj = cov[j][j] - sum(lower[j][k] ** 2 * d[k] for k in range(j))
        if not dj > 0.0:
            raise ValueError("cov must be positive definite")
        d[j] = dj
        lower[j][j] = 1.0
        for i in range(j + 1, n):
            lower[i][j] = (cov[i][j] - sum(lower[i][k] * lower[j][k] * d[k] for k in range(j))) / dj
    # L = unit lower * sqrt(D): column j scaled by sqrt(d_j)
    return [[lower[i][j] * math.sqrt(d[j]) if j <= i else 0.0 for j in range(n)] for i in range(n)]


def simulate_losses(
    position_cents: list[int],
    cov: list[list[float]],
    n_draws: int,
    seed: int,
    family: str,
    nu: int | None,
) -> list[int]:
    if not isinstance(position_cents, list) or not position_cents or any(type(w) is not int for w in position_cents):
        raise ValueError("position_cents must be a non-empty list of whole numbers of cents")
    if type(n_draws) is not int or n_draws < 1:
        raise ValueError("n_draws must be a whole number, 1 or more")
    if family not in ("gaussian", "student_t"):
        raise ValueError('family must be "gaussian" or "student_t"')
    if family == "gaussian" and nu is not None:
        raise ValueError("gaussian takes no degrees of freedom")
    if family == "student_t" and nu is None:
        raise ValueError("student_t needs degrees of freedom")
    n = len(position_cents)
    L = _ldl_factor(cov, n)
    student = family == "student_t"
    s = matched_scale(nu) if student else 1.0
    rng = random.Random(seed)
    out: list[int] = []
    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        scale = 1.0
        if student:
            w = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(nu))  # chi-square with nu degrees of freedom
            scale = math.sqrt(s * nu / w)
        loss = 0.0
        for i in range(n):
            loss += position_cents[i] * scale * sum(L[i][k] * z[k] for k in range(i + 1))
        out.append(round(-loss))
    return out


def quantile_99(losses_cents: list[int]) -> int:
    if not isinstance(losses_cents, list) or not losses_cents or any(type(x) is not int for x in losses_cents):
        raise ValueError("losses_cents must be a non-empty list of whole numbers of cents")
    n = len(losses_cents)
    k = math.ceil(Fraction(99, 100) * n)
    return heapq.nsmallest(k, losses_cents)[-1]
