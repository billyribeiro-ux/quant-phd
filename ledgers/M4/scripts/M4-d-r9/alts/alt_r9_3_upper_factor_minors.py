"""Alternative (verifier round 9, slice d): correct implementation that factors the upper-triangular U with U^T U = cov
(then L = U^T), checks positive definiteness with leading principal minors, and computes each loss with a plain
two-level loop. The Student-t chi-square is gammavariate(nu / 2, 2.0). All inputs are SIMULATED.
"""

from __future__ import annotations

import math
import random


def matched_scale(nu: int) -> float:
    if type(nu) is not int:
        raise ValueError("nu must be an int")
    if nu <= 2:
        raise ValueError("nu must be greater than 2")
    return (nu - 2) / nu


def _lower_from_upper(cov: list[list[float]], n: int) -> list[list[float]]:
    if len(cov) != n or any(len(r) != n for r in cov):
        raise ValueError("cov must be a square matrix with one row and one column per position")
    if any(cov[i][j] != cov[j][i] for i in range(n) for j in range(n)):
        raise ValueError("cov must be symmetric")
    # leading principal minors must all be positive (Sylvester); computed through the factor below
    u = [[0.0] * n for _ in range(n)]
    for j in range(n):
        for i in range(j + 1):
            s = cov[i][j] - sum(u[k][i] * u[k][j] for k in range(i))
            if i == j:
                if not s > 0.0:
                    raise ValueError("cov must be positive definite")
                u[j][j] = math.sqrt(s)
            else:
                u[i][j] = s / u[i][i]
    return [[u[j][i] for j in range(n)] for i in range(n)]  # L = U^T


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
    if not all(type(w) is int for w in position_cents):
        raise ValueError("position_cents must be whole numbers of cents")
    if type(n_draws) is not int or n_draws < 1:
        raise ValueError("n_draws must be a whole number of draws, at least 1")
    if family not in ("gaussian", "student_t"):
        raise ValueError('family must be "gaussian" or "student_t"')
    if family == "gaussian" and nu is not None:
        raise ValueError("nu must be None for gaussian")
    if family == "student_t" and nu is None:
        raise ValueError("nu is required for student_t")
    n = len(position_cents)
    lo = _lower_from_upper(cov, n)
    rng = random.Random(seed)
    s = matched_scale(nu) if family == "student_t" else None
    result = []
    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        scale = 1.0
        if s is not None:
            chi = rng.gammavariate(nu / 2, 2.0)
            scale = math.sqrt(s * nu / chi)
        loss = 0.0
        for i in range(n):
            acc = 0.0
            for k in range(i + 1):
                acc += lo[i][k] * z[k]
            loss -= position_cents[i] * scale * acc
        result.append(round(loss))
    return result


def quantile_99(losses_cents: list[int]) -> int:
    if not isinstance(losses_cents, list) or not losses_cents:
        raise ValueError("quantile_99 needs at least one loss")
    if not all(type(x) is int for x in losses_cents):
        raise ValueError("quantile_99 needs whole numbers of cents")
    ordered = sorted(losses_cents)
    idx = math.ceil(0.99 * len(ordered) - 1e-9)  # tolerance in the float product: the page's index is exact
    return ordered[idx - 1]
