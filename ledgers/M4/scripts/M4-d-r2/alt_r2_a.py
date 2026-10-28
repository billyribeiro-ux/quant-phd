"""Verifier round-2 alternative A: a correct implementation with a different random stream order.

Each Student-t draw takes its chi-square variable BEFORE the normals. The Cholesky factor is built column by column,
the 99% index is an integer ceiling by division, and the matched factor is written as 1 - 2 / nu.
"""

from __future__ import annotations

import math
import random
from collections.abc import Sequence


def _int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def matched_scale(nu: int) -> float:
    if not _int(nu):
        raise ValueError("nu must be a whole number")
    if nu <= 2:
        raise ValueError("nu must be greater than 2")
    return 1 - 2 / nu


def _factor(cov: Sequence[Sequence[float]], n: int) -> list[list[float]]:
    if len(cov) != n or any(len(r) != n for r in cov):
        raise ValueError("cov must be square, one row and one column per position")
    for i in range(n):
        for j in range(n):
            if cov[i][j] != cov[j][i]:
                raise ValueError("cov must be symmetric")
    lo = [[0.0] * n for _ in range(n)]
    for j in range(n):
        d = cov[j][j] - sum(lo[j][k] ** 2 for k in range(j))
        if d <= 0:
            raise ValueError("cov must be positive definite")
        lo[j][j] = math.sqrt(d)
        for i in range(j + 1, n):
            lo[i][j] = (cov[i][j] - sum(lo[i][k] * lo[j][k] for k in range(j))) / lo[j][j]
    return lo


def simulate_losses(
    position_cents: list[int],
    cov: list[list[float]],
    n_draws: int,
    seed: int,
    family: str,
    nu: int | None,
) -> list[int]:
    if not isinstance(position_cents, list) or len(position_cents) == 0:
        raise ValueError("position_cents must not be empty")
    if not all(_int(w) for w in position_cents):
        raise ValueError("position_cents must be whole cents")
    if not _int(n_draws) or n_draws <= 0:
        raise ValueError("n_draws must be 1 or more")
    if family not in ("gaussian", "student_t"):
        raise ValueError("unknown family")
    if family == "gaussian" and nu is not None:
        raise ValueError("gaussian takes no nu")
    if family == "student_t" and nu is None:
        raise ValueError("student_t needs nu")
    n = len(position_cents)
    lo = _factor(cov, n)
    s = matched_scale(nu) if family == "student_t" else 1.0
    rng = random.Random(seed)
    out: list[int] = []
    for _ in range(n_draws):
        if family == "student_t":
            w = rng.gammavariate(nu / 2, 2.0)
            scale = math.sqrt(s * nu / w)
        else:
            scale = 1.0
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        loss = 0.0
        for i in range(n):
            r = scale * sum(lo[i][k] * z[k] for k in range(i + 1))
            loss -= position_cents[i] * r
        out.append(round(loss))
    return out


def quantile_99(losses_cents: list[int]) -> int:
    if not isinstance(losses_cents, list) or len(losses_cents) == 0:
        raise ValueError("losses must be a non-empty list")
    if not all(_int(x) for x in losses_cents):
        raise ValueError("losses must be whole cents")
    n = len(losses_cents)
    k = -((-99 * n) // 100)  # integer ceiling of 0.99 n
    return sorted(losses_cents)[k - 1]
