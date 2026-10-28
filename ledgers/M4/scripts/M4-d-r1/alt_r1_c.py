"""Alternative C (verifier round 1): Box-Muller pairs with a spare value, Cholesky by rows with a 1e-300 cutoff, nu via 1 - 2/nu, full sort quantile."""

from __future__ import annotations

import math
import random


def _whole(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def matched_scale(nu: int) -> float:
    if not _whole(nu):
        raise ValueError("nu must be a whole number of degrees of freedom")
    if nu <= 2:
        raise ValueError("nu must be greater than 2 for the matched covariance to exist")
    return 1.0 - 2.0 / nu


def _factor(cov: list[list[float]], n: int) -> list[list[float]]:
    if len(cov) != n or any(len(r) != n for r in cov):
        raise ValueError("cov must be a square matrix with one row and one column per position")
    for i in range(n):
        for j in range(i):
            if cov[i][j] != cov[j][i]:
                raise ValueError("cov must be symmetric")
    lf = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            acc = cov[i][j] - sum(lf[i][k] * lf[j][k] for k in range(j))
            if i == j:
                if acc <= 1e-300:
                    raise ValueError("cov must be positive definite: every Cholesky pivot must be above zero")
                lf[i][i] = math.sqrt(acc)
            else:
                lf[i][j] = acc / lf[j][j]
    return lf


class _Pairs:
    def __init__(self, rng: random.Random) -> None:
        self.rng = rng
        self.spare: float | None = None

    def next(self) -> float:
        if self.spare is not None:
            value, self.spare = self.spare, None
            return value
        r = math.sqrt(-2.0 * math.log(1.0 - self.rng.random()))
        theta = 2.0 * math.pi * self.rng.random()
        self.spare = r * math.sin(theta)
        return r * math.cos(theta)


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
    lf = _factor(cov, n)
    gen = _Pairs(random.Random(seed))
    out: list[int] = []
    for _ in range(n_draws):
        z = [gen.next() for _ in range(n)]
        s = 1.0
        if family == "student_t" and nu is not None:
            chi = sum(gen.next() ** 2 for _ in range(nu))
            s = math.sqrt(matched_scale(nu) * nu / chi)
        loss = 0.0
        for i in range(n):
            loss -= position_cents[i] * s * sum(lf[i][k] * z[k] for k in range(i + 1))
        out.append(round(loss))
    return out


def quantile_99(losses_cents: list[int]) -> int:
    if not isinstance(losses_cents, list) or not losses_cents or any(not _whole(x) for x in losses_cents):
        raise ValueError("losses_cents must be a non-empty list of whole numbers of cents")
    ordered = sorted(losses_cents)
    return ordered[(99 * len(ordered) + 99) // 100 - 1]
