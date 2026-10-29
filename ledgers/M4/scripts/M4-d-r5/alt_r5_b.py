"""Verifier round-5 alternative B: gammavariate chi-square with a relative symmetry tolerance of 1e-12, pivots checked
with a relative floor, a heap-based order statistic, and the matched factor applied as sqrt((nu-2)/W)."""

from __future__ import annotations

import heapq
import math
import random


def _whole(x: object) -> bool:
    return type(x) is int


def matched_scale(nu):
    if not _whole(nu) or nu <= 2:
        raise ValueError("nu must be a whole number above 2")
    return (nu - 2) / nu


def simulate_losses(position_cents, cov, n_draws, seed, family, nu):
    if not isinstance(position_cents, list) or not position_cents or not all(_whole(w) for w in position_cents):
        raise ValueError("position_cents must be a non-empty list of whole cents")
    if not _whole(n_draws) or n_draws <= 0:
        raise ValueError("n_draws must be a positive whole number")
    if family not in ("gaussian", "student_t"):
        raise ValueError('family must be "gaussian" or "student_t"')
    if (family == "gaussian") != (nu is None):
        raise ValueError("nu must be None exactly for the gaussian family")
    n = len(position_cents)
    if not isinstance(cov, list) or len(cov) != n or any(not isinstance(r, list) or len(r) != n for r in cov):
        raise ValueError("cov must be a square matrix with one row and one column per position")
    scale_ref = max(abs(cov[i][j]) for i in range(n) for j in range(n)) or 1.0
    for i in range(n):
        for j in range(i):
            if abs(cov[i][j] - cov[j][i]) > 1e-12 * scale_ref:
                raise ValueError("cov must be symmetric")
    # Cholesky in column-oriented (outer product) form
    acc = [[float(cov[i][j]) for j in range(n)] for i in range(n)]
    fac = [[0.0] * n for _ in range(n)]
    for k in range(n):
        piv = acc[k][k]
        if not piv > 1e-300:
            raise ValueError("cov must be positive definite: pivot not above zero")
        fac[k][k] = math.sqrt(piv)
        for i in range(k + 1, n):
            fac[i][k] = acc[i][k] / fac[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                acc[i][j] -= fac[i][k] * fac[j][k]
    rng = random.Random(seed)
    out = []
    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        f = 1.0
        if family == "student_t":
            if not _whole(nu) or nu <= 2:
                raise ValueError("nu must be a whole number above 2")
            w = rng.gammavariate(nu / 2.0, 2.0)
            f = math.sqrt((nu - 2) / w)
        total = 0.0
        for i in range(n):
            total += position_cents[i] * f * sum(fac[i][k] * z[k] for k in range(i + 1))
        out.append(round(-total))
    return out


def quantile_99(losses_cents):
    if not isinstance(losses_cents, list) or not losses_cents:
        raise ValueError("losses must be a non-empty list")
    if any(not _whole(x) for x in losses_cents):
        raise ValueError("losses must be whole cents")
    m = len(losses_cents)
    k = (99 * m + 99) // 100
    return heapq.nsmallest(k, losses_cents)[-1]
