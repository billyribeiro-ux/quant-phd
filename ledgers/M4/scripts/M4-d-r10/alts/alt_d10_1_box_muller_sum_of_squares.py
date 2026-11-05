"""Alternative 1 (verifier D, round 10): Box-Muller normals for the Student-t family, chi-square as a sum of nu squared normals, Cholesky by LDL^T, quantile by heapq.nsmallest. Correct implementation of the M4 spec."""

from __future__ import annotations

import heapq
import math
import random


def _whole(value: object) -> bool:
    return type(value) is int


def matched_scale(nu: int) -> float:
    if not _whole(nu):
        raise ValueError("nu must be a whole number of degrees of freedom")
    if nu <= 2:
        raise ValueError("nu must be greater than 2 for the matched covariance to exist")
    return (nu - 2) / nu


def _ldl_lower(cov, n):
    if len(cov) != n or any(len(row) != n for row in cov):
        raise ValueError("cov must be a square matrix with one row and one column per position")
    for i in range(n):
        for j in range(i):
            if cov[i][j] != cov[j][i]:
                raise ValueError("cov must be symmetric")
    d = [0.0] * n
    lower = [[0.0] * n for _ in range(n)]
    for j in range(n):
        d[j] = cov[j][j] - sum(lower[j][k] ** 2 * d[k] for k in range(j))
        if not d[j] > 0.0:
            raise ValueError("cov must be positive definite: every Cholesky pivot must be above zero")
        lower[j][j] = 1.0
        for i in range(j + 1, n):
            lower[i][j] = (cov[i][j] - sum(lower[i][k] * lower[j][k] * d[k] for k in range(j))) / d[j]
    return [[lower[i][j] * math.sqrt(d[j]) for j in range(n)] for i in range(n)]


def _box_muller(rng):
    u1 = 1.0 - rng.random()
    u2 = rng.random()
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def simulate_losses(position_cents, cov, n_draws, seed, family, nu):
    if not isinstance(position_cents, list) or not position_cents or any(not _whole(w) for w in position_cents):
        raise ValueError("position_cents must be a non-empty list of whole numbers of cents")
    if not _whole(n_draws) or n_draws < 1:
        raise ValueError("n_draws must be a whole number of draws, 1 or more")
    if family not in ("gaussian", "student_t"):
        raise ValueError('family must be "gaussian" or "student_t"')
    if family == "gaussian" and nu is not None:
        raise ValueError("nu must be None for the gaussian family")
    if family == "student_t" and nu is None:
        raise ValueError("nu is required for the student_t family")
    n = len(position_cents)
    factor = _ldl_lower(cov, n)
    student = family == "student_t"
    matched = matched_scale(nu) if student else 1.0
    rng = random.Random(seed)
    losses = []
    for _ in range(n_draws):
        if student:
            z = [_box_muller(rng) for _ in range(n)]
            chi_square = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(nu))
            scale = math.sqrt(matched * nu / chi_square)
        else:
            z = [rng.gauss(0.0, 1.0) for _ in range(n)]
            scale = 1.0
        total = 0.0
        for i in range(n):
            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))
            total += position_cents[i] * ret
        losses.append(round(-total))
    return losses


def quantile_99(losses_cents):
    if not isinstance(losses_cents, list) or not losses_cents or any(not _whole(x) for x in losses_cents):
        raise ValueError("losses_cents must be a non-empty list of whole numbers of cents")
    index = math.ceil(0.99 * len(losses_cents))
    return heapq.nsmallest(index, losses_cents)[-1]
