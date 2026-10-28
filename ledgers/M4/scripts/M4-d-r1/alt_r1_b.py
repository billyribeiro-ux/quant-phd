"""Alternative B (verifier round 1): Marsaglia polar normals, gamma chi-square, floor(x + 0.5) rounding, sorted quantile via math.ceil on a Fraction."""

from __future__ import annotations

import math
import random
from fractions import Fraction


def _whole(value: object) -> bool:
    return type(value) is int and not isinstance(value, bool)


def matched_scale(nu: int) -> float:
    if not _whole(nu):
        raise ValueError("nu must be a whole number of degrees of freedom")
    if nu <= 2:
        raise ValueError("nu must be greater than 2 for the matched covariance to exist")
    return (nu - 2) / nu


def _cholesky_cols(cov: list[list[float]], n: int) -> list[list[float]]:
    if len(cov) != n or any(len(r) != n for r in cov):
        raise ValueError("cov must be a square matrix with one row and one column per position")
    for i in range(n):
        for j in range(n):
            if not math.isclose(cov[i][j], cov[j][i], rel_tol=1e-12, abs_tol=0.0):
                raise ValueError("cov must be symmetric")
    lo = [[0.0] * n for _ in range(n)]
    for j in range(n):
        s = cov[j][j] - sum(lo[j][k] ** 2 for k in range(j))
        if s <= 1e-30:
            raise ValueError("cov must be positive definite: every Cholesky pivot must be above zero")
        lo[j][j] = math.sqrt(s)
        for i in range(j + 1, n):
            lo[i][j] = (cov[i][j] - sum(lo[i][k] * lo[j][k] for k in range(j))) / lo[j][j]
    return lo


def _polar(rng: random.Random) -> float:
    while True:
        u = 2.0 * rng.random() - 1.0
        v = 2.0 * rng.random() - 1.0
        s = u * u + v * v
        if 0.0 < s < 1.0:
            return u * math.sqrt(-2.0 * math.log(s) / s)


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
    lo = _cholesky_cols(cov, n)
    rng = random.Random(seed)
    out: list[int] = []
    for _ in range(n_draws):
        z = [_polar(rng) for _ in range(n)]
        scale = 1.0
        if family == "student_t" and nu is not None:
            w = rng.gammavariate(nu / 2.0, 2.0)
            scale = math.sqrt(matched_scale(nu) * nu / w)
        total = sum(position_cents[i] * scale * sum(lo[i][k] * z[k] for k in range(i + 1)) for i in range(n))
        out.append(math.floor(-total + 0.5))
    return out


def quantile_99(losses_cents: list[int]) -> int:
    if not isinstance(losses_cents, list) or not losses_cents or any(not _whole(x) for x in losses_cents):
        raise ValueError("losses_cents must be a non-empty list of whole numbers of cents")
    k = math.ceil(Fraction(99, 100) * len(losses_cents))
    return sorted(losses_cents)[k - 1]
