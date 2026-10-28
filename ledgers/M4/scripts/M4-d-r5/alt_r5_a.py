"""Verifier round-5 alternative A: Box-Muller normals from random(), chi-square as a sum of squared normals,
exact-integer quantile via sorted(), explicit sign handling. Correct by the page's stated conditions."""

from __future__ import annotations

import math
import random
from collections.abc import Sequence


def _is_int(x: object) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def matched_scale(nu: int) -> float:
    if not _is_int(nu):
        raise ValueError("nu must be an int")
    if nu <= 2:
        raise ValueError("nu must exceed 2")
    return (nu - 2) / nu


def _chol(cov: Sequence[Sequence[float]], n: int) -> list[list[float]]:
    if len(cov) != n or any(len(r) != n for r in cov):
        raise ValueError("cov must be one row and one column per position")
    for i in range(n):
        for j in range(i + 1, n):
            if cov[i][j] != cov[j][i]:
                raise ValueError("cov must be symmetric")
    fac = [[0.0] * n for _ in range(n)]
    for j in range(n):
        d = cov[j][j] - sum(fac[j][k] ** 2 for k in range(j))
        if not d > 0:
            raise ValueError("cov must be positive definite")
        fac[j][j] = math.sqrt(d)
        for i in range(j + 1, n):
            fac[i][j] = (cov[i][j] - sum(fac[i][k] * fac[j][k] for k in range(j))) / fac[j][j]
    return fac


def simulate_losses(position_cents, cov, n_draws, seed, family, nu):
    if not isinstance(position_cents, list) or len(position_cents) == 0:
        raise ValueError("position_cents must be a non-empty list")
    if any(not _is_int(w) for w in position_cents):
        raise ValueError("position_cents must be whole cents")
    if not _is_int(n_draws) or n_draws < 1:
        raise ValueError("n_draws must be a whole number, 1 or more")
    if family not in ("gaussian", "student_t"):
        raise ValueError("family must be gaussian or student_t")
    if family == "gaussian" and nu is not None:
        raise ValueError("nu must be None for gaussian")
    if family == "student_t" and nu is None:
        raise ValueError("student_t needs nu")
    n = len(position_cents)
    fac = _chol(cov, n)
    rng = random.Random(seed)
    out = []

    def normal() -> float:
        u1 = 1.0 - rng.random()
        u2 = rng.random()
        return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)

    for _ in range(n_draws):
        z = [normal() for _ in range(n)]
        scale = 1.0
        if family == "student_t":
            s = matched_scale(nu)
            w = sum(normal() ** 2 for _ in range(nu))
            scale = math.sqrt(s * nu / w)
        ret = [scale * sum(fac[i][k] * z[k] for k in range(i + 1)) for i in range(n)]
        loss = -sum(position_cents[i] * ret[i] for i in range(n))
        out.append(round(loss))
    return out


def quantile_99(losses_cents):
    if not isinstance(losses_cents, list) or len(losses_cents) == 0:
        raise ValueError("losses must be a non-empty list")
    if any(not _is_int(x) for x in losses_cents):
        raise ValueError("losses must be whole cents")
    k = -(-99 * len(losses_cents) // 100)
    return sorted(losses_cents)[k - 1]
