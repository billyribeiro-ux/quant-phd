"""Verifier round-2 alternative B: a correct implementation with a different algorithm.

The Student-t chi-square variable is the sum of nu squared normals (nu is a whole number), drawn per draw from the same
generator. Normals come from the stdlib gauss. The quantile is read from the top of a descending sort. The
validation cutoffs use NaN-safe comparisons.
"""

from __future__ import annotations

import math
import random
from collections.abc import Sequence


def _whole(x: object) -> bool:
    return type(x) is int


def matched_scale(nu: int) -> float:
    if not _whole(nu) or nu < 3:
        if not _whole(nu):
            raise ValueError("nu must be a whole number of degrees of freedom")
        raise ValueError("nu must be greater than 2")
    return (nu - 2) / nu


def _lower(cov: Sequence[Sequence[float]], n: int) -> list[list[float]]:
    if len(cov) != n or any(len(row) != n for row in cov):
        raise ValueError("cov must be an n by n matrix")
    for i in range(n):
        for j in range(i + 1, n):
            if not (cov[i][j] == cov[j][i]):
                raise ValueError("cov must be symmetric")
    lower = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            acc = sum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                piv = cov[i][i] - acc
                if math.isnan(piv) or piv <= 0.0:
                    raise ValueError("cov must be positive definite")
                lower[i][i] = math.sqrt(piv)
            else:
                lower[i][j] = (cov[i][j] - acc) / lower[j][j]
    return lower


def simulate_losses(
    position_cents: list[int],
    cov: list[list[float]],
    n_draws: int,
    seed: int,
    family: str,
    nu: int | None,
) -> list[int]:
    if not isinstance(position_cents, list) or not position_cents:
        raise ValueError("position_cents must hold at least one position")
    if any(not _whole(w) for w in position_cents):
        raise ValueError("position_cents must be whole cents")
    if not _whole(n_draws) or n_draws < 1:
        raise ValueError("n_draws must be 1 or more")
    if family not in {"gaussian", "student_t"}:
        raise ValueError("family must be gaussian or student_t")
    if (family == "gaussian") != (nu is None):
        raise ValueError("nu is given for the student_t family only")
    n = len(position_cents)
    lower = _lower(cov, n)
    rng = random.Random(seed)
    losses: list[int] = []
    for _ in range(n_draws):
        if family == "student_t":
            assert nu is not None
            m = matched_scale(nu)
            w = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(nu))
            scale = math.sqrt(m * nu / w)
        else:
            scale = 1.0
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        returns = [scale * sum(lower[i][k] * z[k] for k in range(n)) for i in range(n)]
        losses.append(round(-sum(position_cents[i] * returns[i] for i in range(n))))
    return losses


def quantile_99(losses_cents: list[int]) -> int:
    if not isinstance(losses_cents, list) or not losses_cents:
        raise ValueError("losses must be a non-empty list of whole cents")
    if any(not _whole(x) for x in losses_cents):
        raise ValueError("losses must be whole cents")
    n = len(losses_cents)
    rank_from_top = n - ((99 * n + 99) // 100) + 1
    return sorted(losses_cents, reverse=True)[rank_from_top - 1]
