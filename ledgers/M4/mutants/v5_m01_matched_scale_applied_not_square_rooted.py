"""Verifier round-5 student-error mutant. (nu - 2) / nu multiplies the return, not its square root."""

from __future__ import annotations

import math
import random
from collections.abc import Sequence


def _whole(value: object) -> bool:
    """True when value is an int and not a bool: a whole number of its unit."""
    return type(value) is int


def matched_scale(nu: int) -> float:
    """The factor (nu - 2) / nu that matches a Student-t draw's covariance to the target. Requires nu > 2."""
    if not _whole(nu):
        raise ValueError("nu must be a whole number of degrees of freedom")
    if nu <= 2:
        raise ValueError("nu must be greater than 2 for the matched covariance to exist")
    return (nu - 2) / nu


def _cholesky(cov: Sequence[Sequence[float]], n: int) -> list[list[float]]:
    """The lower-triangular factor L with L L^\top = cov, computed row by row. Requires cov to be n x n, symmetric
    and positive definite: every pivot must be strictly positive."""
    if len(cov) != n or any(len(row) != n for row in cov):
        raise ValueError("cov must be a square matrix with one row and one column per position")
    for i in range(n):
        for j in range(i):
            if cov[i][j] != cov[j][i]:
                raise ValueError("cov must be symmetric")
    factor = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            inner = sum(factor[i][k] * factor[j][k] for k in range(j))
            if i == j:
                pivot = cov[i][i] - inner
                if not pivot > 0.0:
                    raise ValueError("cov must be positive definite: every Cholesky pivot must be above zero")
                factor[i][i] = math.sqrt(pivot)
            else:
                factor[i][j] = (cov[i][j] - inner) / factor[j][j]
    return factor


def simulate_losses(
    position_cents: list[int],
    cov: list[list[float]],
    n_draws: int,
    seed: int,
    family: str,
    nu: int | None,
) -> list[int]:
    """One portfolio loss per draw, in integer cents: loss = -sum_i w_i r_i with w_i the position in cents.

    The returns are r = sqrt(s) L Z for the Gaussian family (s = 1) and r = sqrt(s nu / W) L Z for the Student-t
    family, where Z is standard normal, W is chi-square with nu degrees of freedom, s = (nu - 2) / nu, and
    L L^\top = cov.
    """
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
    matched = matched_scale(nu) if student and nu is not None else 1.0
    rng = random.Random(seed)
    losses: list[int] = []
    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        scale = 1.0
        if student and nu is not None:
            chi_square = rng.gammavariate(nu / 2, 2.0)
            scale = matched * math.sqrt(nu / chi_square)
        total = 0.0
        for i in range(n):
            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))
            total += position_cents[i] * ret
        losses.append(round(-total))
    return losses


def quantile_99(losses_cents: list[int]) -> int:
    """The 99% loss: the order statistic with 1-based index ceil(0.99 n), computed in exact integers."""
    if not isinstance(losses_cents, list) or not losses_cents or any(not _whole(x) for x in losses_cents):
        raise ValueError("losses_cents must be a non-empty list of whole numbers of cents")
    index = (99 * len(losses_cents) + 99) // 100
    return sorted(losses_cents)[index - 1]
