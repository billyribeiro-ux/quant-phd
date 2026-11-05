"""Alternative 2 (verifier D, round 10): Marsaglia polar normals for the Student-t family, gamma chi-square drawn in a block before the normals, Cholesky row by row with an exact positive-pivot test, quantile by full sort. Correct implementation of the M4 spec."""

from __future__ import annotations

import math
import random


def _whole(value: object) -> bool:
    return type(value) is int


def matched_scale(nu: int) -> float:
    if not _whole(nu):
        raise ValueError("nu must be a whole number of degrees of freedom")
    if nu <= 2:
        raise ValueError("nu must be greater than 2 for the matched covariance to exist")
    return 1.0 - 2.0 / nu


def _cholesky(cov, n):
    if len(cov) != n or any(len(row) != n for row in cov):
        raise ValueError("cov must be a square matrix with one row and one column per position")
    for i in range(n):
        for j in range(i):
            if cov[i][j] != cov[j][i]:
                raise ValueError("cov must be symmetric")
    factor = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            acc = 0.0
            for k in range(j):
                acc += factor[i][k] * factor[j][k]
            if i == j:
                pivot = cov[i][i] - acc
                if not pivot > 0:
                    raise ValueError("cov must be positive definite: every Cholesky pivot must be above zero")
                factor[i][i] = math.sqrt(pivot)
            else:
                factor[i][j] = (cov[i][j] - acc) / factor[j][j]
    return factor


def _polar(rng):
    while True:
        a = 2.0 * rng.random() - 1.0
        b = 2.0 * rng.random() - 1.0
        s = a * a + b * b
        if 0.0 < s < 1.0:
            return a * math.sqrt(-2.0 * math.log(s) / s)


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
    factor = _cholesky(cov, n)
    student = family == "student_t"
    matched = matched_scale(nu) if student else 1.0
    rng = random.Random(seed)
    chis = [rng.gammavariate(nu / 2.0, 2.0) for _ in range(n_draws)] if student else None
    losses = []
    for d in range(n_draws):
        if student:
            z = [_polar(rng) for _ in range(n)]
            scale = math.sqrt(matched * nu / chis[d])
        else:
            z = [rng.gauss(0.0, 1.0) for _ in range(n)]
            scale = 1.0
        ret = [scale * sum(factor[i][k] * z[k] for k in range(i + 1)) for i in range(n)]
        losses.append(round(-sum(position_cents[i] * ret[i] for i in range(n))))
    return losses


def quantile_99(losses_cents):
    if not isinstance(losses_cents, list) or not losses_cents or any(not _whole(x) for x in losses_cents):
        raise ValueError("losses_cents must be a non-empty list of whole numbers of cents")
    ordered = sorted(losses_cents)
    return ordered[(99 * len(ordered) + 99) // 100 - 1]
