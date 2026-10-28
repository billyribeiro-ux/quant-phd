"""Alternative A (verifier round 1): Box-Muller normals, chi-square as a sum of squared normals, LDL factor, heapq quantile."""

from __future__ import annotations

import heapq
import math
import random
from collections.abc import Sequence


def _whole(value: object) -> bool:
    return type(value) is int


def matched_scale(nu: int) -> float:
    if not _whole(nu):
        raise ValueError("nu must be a whole number of degrees of freedom")
    if nu <= 2:
        raise ValueError("nu must be greater than 2 for the matched covariance to exist")
    return 1.0 - 2.0 / nu


def _ldl(cov: Sequence[Sequence[float]], n: int) -> list[list[float]]:
    if len(cov) != n or any(len(row) != n for row in cov):
        raise ValueError("cov must be a square matrix with one row and one column per position")
    scale = max(abs(x) for row in cov for x in row) or 1.0
    for i in range(n):
        for j in range(i):
            if abs(cov[i][j] - cov[j][i]) > 1e-12 * scale:
                raise ValueError("cov must be symmetric")
    d = [0.0] * n
    lower = [[0.0] * n for _ in range(n)]
    for j in range(n):
        d[j] = cov[j][j] - sum(lower[j][k] ** 2 * d[k] for k in range(j))
        if not d[j] > 1e-18:
            raise ValueError("cov must be positive definite: every LDL pivot must be above zero")
        lower[j][j] = 1.0
        for i in range(j + 1, n):
            lower[i][j] = (cov[i][j] - sum(lower[i][k] * lower[j][k] * d[k] for k in range(j))) / d[j]
    return [[lower[i][j] * math.sqrt(d[j]) for j in range(n)] for i in range(n)]


def _normal(rng: random.Random) -> float:
    u1 = 1.0 - rng.random()
    u2 = rng.random()
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def simulate_losses(
    position_cents: list[int],
    cov: list[list[float]],
    n_draws: int,
    seed: int,
    family: str,
    nu: int | None,
) -> list[int]:
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
    lf = _ldl(cov, n)
    rng = random.Random(seed)
    out: list[int] = []
    for _ in range(n_draws):
        z = [_normal(rng) for _ in range(n)]
        scale = 1.0
        if family == "student_t":
            assert nu is not None
            w = sum(_normal(rng) ** 2 for _ in range(nu))
            scale = math.sqrt(matched_scale(nu) * nu / w)
        loss = 0.0
        for i in range(n):
            loss -= position_cents[i] * scale * sum(lf[i][k] * z[k] for k in range(n))
        out.append(round(loss))
    return out


def quantile_99(losses_cents: list[int]) -> int:
    if not isinstance(losses_cents, list) or not losses_cents or any(not _whole(x) for x in losses_cents):
        raise ValueError("losses_cents must be a non-empty list of whole numbers of cents")
    k = -((-99 * len(losses_cents)) // 100)
    return heapq.nsmallest(k, losses_cents)[-1]
