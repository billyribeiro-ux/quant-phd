"""Verifier round-5 alternative C: the Gaussian and Student-t families each draw their normals from their own seeded
generator (random.Random(seed) for the Gaussian family and random.Random(seed) reseeded per family), returns built
with numpy-free list arithmetic, and the matched factor applied as a separate multiplier on the returns."""

from __future__ import annotations

import math
import random


def _whole(x: object) -> bool:
    return type(x) is int


def matched_scale(nu: int) -> float:
    if not _whole(nu):
        raise ValueError("nu must be a whole number")
    if nu <= 2:
        raise ValueError("nu must be greater than 2")
    return (nu - 2) / nu


def _factor(cov, n):
    if not isinstance(cov, list) or len(cov) != n or any(not isinstance(r, list) or len(r) != n for r in cov):
        raise ValueError("cov must be one row and one column per position")
    for i in range(n):
        for j in range(n):
            if cov[i][j] != cov[j][i]:
                raise ValueError("cov must be symmetric")
    fac = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(fac[i][k] * fac[j][k] for k in range(j))
            if i == j:
                v = cov[i][i] - s
                if v <= 0.0:
                    raise ValueError("cov must be positive definite")
                fac[i][i] = math.sqrt(v)
            else:
                fac[i][j] = (cov[i][j] - s) / fac[j][j]
    return fac


def simulate_losses(position_cents, cov, n_draws, seed, family, nu):
    if not isinstance(position_cents, list) or not position_cents:
        raise ValueError("position_cents must be non-empty")
    if not all(_whole(w) for w in position_cents):
        raise ValueError("position_cents must be whole cents")
    if not _whole(n_draws) or n_draws < 1:
        raise ValueError("n_draws must be 1 or more")
    if family == "gaussian":
        if nu is not None:
            raise ValueError("nu must be None for the gaussian family")
        mult = 1.0
    elif family == "student_t":
        if nu is None:
            raise ValueError("the student_t family needs nu")
        mult = matched_scale(nu)
    else:
        raise ValueError('family must be "gaussian" or "student_t"')
    n = len(position_cents)
    fac = _factor(cov, n)
    rng = random.Random(seed)
    losses = []
    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        g = 1.0
        if family == "student_t":
            g = math.sqrt(nu / rng.gammavariate(nu / 2, 2.0))
        r = [sum(fac[i][k] * z[k] for k in range(i + 1)) * g * math.sqrt(mult) for i in range(n)]
        losses.append(round(-sum(position_cents[i] * r[i] for i in range(n))))
    return losses


def quantile_99(losses_cents):
    if not isinstance(losses_cents, list) or not losses_cents:
        raise ValueError("losses must be a non-empty list")
    if not all(_whole(x) for x in losses_cents):
        raise ValueError("losses must be whole cents")
    idx = math.ceil(0.99 * len(losses_cents) - 1e-12)
    return sorted(losses_cents)[max(idx, 1) - 1]
