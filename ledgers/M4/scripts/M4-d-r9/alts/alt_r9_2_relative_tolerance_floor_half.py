"""Alternative (verifier round 9, slice d): correct implementation with a relative symmetry tolerance of 1e-12, a
Cholesky pivot test of pivot > 0, round-half-up written as floor(x + 1/2), and a chi-square built with gammavariate
scale 2 at shape nu / 2 (as the page states). All inputs are SIMULATED.
"""

from __future__ import annotations

import math
import random


def matched_scale(nu: int) -> float:
    if type(nu) is not int or nu <= 2:
        raise ValueError("matched_scale needs a whole number nu greater than 2")
    return (nu - 2) / nu


def _lower(cov: list[list[float]], n: int) -> list[list[float]]:
    if len(cov) != n or any(len(r) != n for r in cov):
        raise ValueError("cov must be a square matrix with one row and one column per position")
    for i in range(n):
        for j in range(i):
            a, b = cov[i][j], cov[j][i]
            if abs(a - b) > 1e-12 * max(abs(a), abs(b)):
                raise ValueError("cov must be symmetric")
    f = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            acc = math.fsum(f[i][k] * f[j][k] for k in range(j))
            if i == j:
                piv = cov[i][i] - acc
                if not piv > 0.0:
                    raise ValueError("cov must be positive definite")
                f[i][i] = math.sqrt(piv)
            else:
                f[i][j] = (cov[i][j] - acc) / f[j][j]
    return f


def simulate_losses(
    position_cents: list[int],
    cov: list[list[float]],
    n_draws: int,
    seed: int,
    family: str,
    nu: int | None,
) -> list[int]:
    if not isinstance(position_cents, list) or not position_cents:
        raise ValueError("position_cents must be a non-empty list")
    if any(type(w) is not int for w in position_cents):
        raise ValueError("position_cents must be whole numbers of cents")
    if type(n_draws) is not int or n_draws <= 0:
        raise ValueError("n_draws must be a whole number of at least 1")
    if family == "gaussian":
        if nu is not None:
            raise ValueError("the gaussian family takes nu = None")
    elif family == "student_t":
        if nu is None:
            raise ValueError("the student_t family needs nu")
    else:
        raise ValueError('family must be "gaussian" or "student_t"')
    n = len(position_cents)
    f = _lower(cov, n)
    rng = random.Random(seed)
    m = matched_scale(nu) if family == "student_t" else None
    out = []
    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        if m is not None:
            chi = rng.gammavariate(nu / 2, 2.0)
            sc = math.sqrt(m * nu / chi)
        else:
            sc = 1.0
        total = 0.0
        for i in range(n):
            total += position_cents[i] * sc * math.fsum(f[i][k] * z[k] for k in range(i + 1))
        out.append(math.floor(-total + 0.5))
    return out


def quantile_99(losses_cents: list[int]) -> int:
    if not isinstance(losses_cents, list) or not losses_cents:
        raise ValueError("quantile_99 needs a non-empty list of losses")
    if any(type(x) is not int for x in losses_cents):
        raise ValueError("quantile_99 needs whole numbers of cents")
    s = sorted(losses_cents)
    n = len(s)
    k = -((-99 * n) // 100)  # ceil(0.99 n) in exact integers
    return s[k - 1]
