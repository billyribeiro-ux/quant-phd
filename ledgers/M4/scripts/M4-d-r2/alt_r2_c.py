"""Verifier round-2 alternative C: a correct implementation with its own normal generator and other cutoffs.

Normals come from Box-Muller on random.random(), so the stream differs from the reference. The symmetry check uses a
relative tolerance of 1e-15, the pivot cutoff is a strictly positive pivot, and the 99% index is the exact
ceiling of a Fraction.
"""

from __future__ import annotations

import math
import random
from collections.abc import Sequence
from fractions import Fraction


def _whole(x: object) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def matched_scale(nu: int) -> float:
    if not _whole(nu):
        raise ValueError("nu must be an int")
    if nu <= 2:
        raise ValueError("nu must be above 2")
    return 1.0 - 2.0 / nu


def _normal(rng: random.Random) -> float:
    u1 = 1.0 - rng.random()  # in (0, 1], so the logarithm is finite
    u2 = rng.random()
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def _chol(cov: Sequence[Sequence[float]], n: int) -> list[list[float]]:
    if len(cov) != n or any(len(row) != n for row in cov):
        raise ValueError("cov must be square, with one row and one column per position")
    for i in range(n):
        for j in range(n):
            if abs(cov[i][j] - cov[j][i]) > 1e-15 * max(1.0, abs(cov[i][j])):
                raise ValueError("cov must be symmetric")
    lower = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = cov[i][j] - sum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                if s <= 0.0:
                    raise ValueError("cov must be positive definite")
                lower[i][i] = math.sqrt(s)
            else:
                lower[i][j] = s / lower[j][j]
    return lower


def simulate_losses(
    position_cents: list[int],
    cov: list[list[float]],
    n_draws: int,
    seed: int,
    family: str,
    nu: int | None,
) -> list[int]:
    if not isinstance(position_cents, list) or len(position_cents) < 1:
        raise ValueError("position_cents must not be empty")
    if not all(_whole(p) for p in position_cents):
        raise ValueError("position_cents must be whole numbers of cents")
    if not _whole(n_draws) or n_draws < 1:
        raise ValueError("n_draws must be a whole number, 1 or more")
    if family not in ("gaussian", "student_t"):
        raise ValueError("family must be gaussian or student_t")
    if family == "gaussian" and nu is not None:
        raise ValueError("the gaussian family takes no nu")
    if family == "student_t" and nu is None:
        raise ValueError("the student_t family requires nu")
    n = len(position_cents)
    lower = _chol(cov, n)
    rng = random.Random(seed)
    out: list[int] = []
    for _ in range(n_draws):
        if family == "student_t":
            assert nu is not None
            w = rng.gammavariate(nu / 2.0, 2.0)
            factor = math.sqrt(matched_scale(nu) * nu / w)
        else:
            factor = 1.0
        z = [_normal(rng) for _ in range(n)]
        ret = [factor * sum(lower[i][k] * z[k] for k in range(i + 1)) for i in range(n)]
        out.append(round(-sum(position_cents[i] * ret[i] for i in range(n))))
    return out


def quantile_99(losses_cents: list[int]) -> int:
    if not isinstance(losses_cents, list) or not losses_cents:
        raise ValueError("losses must be a non-empty list")
    if not all(_whole(x) for x in losses_cents):
        raise ValueError("losses must be whole numbers of cents")
    n = len(losses_cents)
    k = math.ceil(Fraction(99 * n, 100))
    return sorted(losses_cents)[k - 1]
