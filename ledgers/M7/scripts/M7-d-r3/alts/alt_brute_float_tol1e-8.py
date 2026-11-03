"""Verifier round-3 alternative A-brute: exhaustive enumeration of working sets in float arithmetic.

Validation and the case parser are the reference's (copied unchanged below); the solver is a different method: it
enumerates every set of up to n-1 inequality rows (bounds, sector caps and the 2**n sign forms of the turnover limit),
solves the equality-constrained KKT system for each set in floats, and returns the first set whose primal point is
feasible and whose multipliers are non-negative. The certificate is recomputed with the page's definitions in floats.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from typing import Any, cast

REQUIRED = ("gamma", "mu", "sigma", "w0", "lower", "upper", "sector", "sector_caps", "turnover_limit")
TOL = Fraction(1, 10**9)
FLOAT_TOL = 1e-8  # feasibility slack for the float working-set test  # the tolerance on the starting-portfolio checks and on the active-set test


@dataclass(frozen=True)
class Problem:
    n: int
    gamma: Fraction
    mu: list[Fraction]
    sigma: list[list[Fraction]]
    w0: list[Fraction]
    lower: list[Fraction]
    upper: list[Fraction]
    sector: list[int]
    caps: list[Fraction]
    tau: Fraction


def _scalar(value: object, name: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number, not {type(value).__name__}")
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite")
        return Fraction(repr(value))  # the decimal text the case carries, read exactly
    return Fraction(value)


def _vector(value: object, name: str) -> list[Fraction]:
    if not isinstance(value, (list, tuple)):
        raise TypeError(f"{name} must be a list of numbers")
    return [_scalar(item, f"{name}[{i}]") for i, item in enumerate(value)]


def _parse(instance: object) -> Problem:
    if not isinstance(instance, Mapping):
        raise ValueError("the instance must be a mapping with the case fields")
    for key in REQUIRED:
        if key not in instance:
            raise ValueError(f"the instance has no {key!r} field")
    mu = _vector(instance["mu"], "mu")
    n = len(mu)
    if n == 0:
        raise ValueError("the instance has no assets")
    gamma = _scalar(instance["gamma"], "gamma")
    if gamma <= 0:
        raise ValueError("gamma must be positive")
    tau = _scalar(instance["turnover_limit"], "turnover_limit")
    if tau < 0:
        raise ValueError("the turnover limit must not be negative")
    raw_sigma = instance["sigma"]
    if not isinstance(raw_sigma, (list, tuple)) or len(raw_sigma) != n:
        raise ValueError("sigma must have one row per asset")
    sigma = [_vector(row, f"sigma[{i}]") for i, row in enumerate(raw_sigma)]
    if any(len(row) != n for row in sigma):
        raise ValueError("sigma must be square, one column per asset")
    if any(sigma[i][j] != sigma[j][i] for i in range(n) for j in range(n)):
        raise ValueError("sigma must be symmetric")
    if not _positive_definite(sigma):
        raise ValueError("sigma must be positive definite")
    w0 = _vector(instance["w0"], "w0")
    lower = _vector(instance["lower"], "lower")
    upper = _vector(instance["upper"], "upper")
    if len(w0) != n or len(lower) != n or len(upper) != n:
        raise ValueError("w0, lower and upper must have one entry per asset")
    if any(lower[i] > upper[i] for i in range(n)):
        raise ValueError("a lower bound lies above its upper bound")
    caps = _vector(instance["sector_caps"], "sector_caps")
    if not caps:
        raise ValueError("the instance has no sector caps")
    raw_sector = instance["sector"]
    if not isinstance(raw_sector, (list, tuple)) or len(raw_sector) != n:
        raise ValueError("sector must give one label per asset")
    sector: list[int] = []
    for label in raw_sector:
        if isinstance(label, bool) or not isinstance(label, int):
            raise TypeError("a sector label must be an integer")
        if not 0 <= label < len(caps):
            raise ValueError("a sector label lies outside 0 to the number of caps minus one")
        sector.append(label)
    if any(label not in sector for label in range(len(caps))):
        raise ValueError("every sector cap must belong to at least one asset")
    if abs(sum(w0, Fraction(0)) - 1) > TOL:
        raise ValueError("the starting portfolio must sum to one")
    if any(w0[i] < lower[i] - TOL or w0[i] > upper[i] + TOL for i in range(n)):
        raise ValueError("the starting portfolio lies outside a box bound")
    for k, cap in enumerate(caps):
        if sum(w0[i] for i in range(n) if sector[i] == k) > cap + TOL:
            raise ValueError("the starting portfolio breaks a sector cap")
    return Problem(n, gamma, mu, sigma, w0, lower, upper, sector, caps, tau)


def _positive_definite(matrix: list[list[Fraction]]) -> bool:
    """Symmetric positive definite, by the LDL' pivots of exact arithmetic: every pivot must be positive."""
    n = len(matrix)
    a = [row[:] for row in matrix]
    for k in range(n):
        pivot = a[k][k]
        if pivot <= 0:
            return False
        for i in range(k + 1, n):
            factor = a[i][k] / pivot
            for j in range(k + 1, n):
                a[i][j] -= factor * a[k][j]
    return True


def _dot(a: Sequence[Fraction], b: Sequence[Fraction]) -> Fraction:
    return sum((x * y for x, y in zip(a, b, strict=True)), Fraction(0))


def _solve_linear(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    """Gauss-Jordan elimination in exact arithmetic, with the first non-zero pivot in each column."""
    size = len(rhs)
    rows = [[*matrix[i][:], rhs[i]] for i in range(size)]
    for col in range(size):
        pivot = next(r for r in range(col, size) if rows[r][col] != 0)
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(size):
            if r != col and rows[r][col] != 0:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[col], strict=True)]
    return [rows[i][size] / rows[i][i] for i in range(size)]


def _rank(vectors: list[list[Fraction]]) -> int:
    rows = [v[:] for v in vectors]
    rank = 0
    width = len(rows[0]) if rows else 0
    for col in range(width):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][col] != 0), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(len(rows)):
            if r != rank and rows[r][col] != 0:
                factor = rows[r][col] / rows[rank][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[rank], strict=True)]
        rank += 1
    return rank


def _kkt_step(
    hessian: list[list[Fraction]], gradient: list[Fraction], active: list[list[Fraction]]
) -> tuple[list[Fraction], list[Fraction]]:
    """Solve the equality-constrained subproblem: H p + g + A' lambda = 0 and A p = 0, for the step p and lambda."""
    n, m = len(gradient), len(active)
    size = n + m
    matrix = [[Fraction(0)] * size for _ in range(size)]
    for i in range(n):
        for j in range(n):
            matrix[i][j] = hessian[i][j]
    for k, a in enumerate(active):
        for i in range(n):
            matrix[i][n + k] = a[i]
            matrix[n + k][i] = a[i]
    solution = _solve_linear(matrix, [-g for g in gradient] + [Fraction(0)] * m)
    return solution[:n], solution[n:]




def _rows(problem: Problem) -> list[tuple[list[float], float, tuple[object, ...]]]:
    """Rows a.w <= b: bounds, sector caps, and the 2**n sign forms of the turnover limit (floats)."""
    n = problem.n
    rows: list[tuple[list[float], float, tuple[object, ...]]] = []
    for i in range(n):
        rows.append(([-1.0 if j == i else 0.0 for j in range(n)], -float(problem.lower[i]), ("lower", i)))
        rows.append(([1.0 if j == i else 0.0 for j in range(n)], float(problem.upper[i]), ("upper", i)))
    for k, cap in enumerate(problem.caps):
        rows.append(([1.0 if problem.sector[j] == k else 0.0 for j in range(n)], float(cap), ("sector", k)))
    w0 = [float(v) for v in problem.w0]
    tau = float(problem.tau)
    for signs in product((1.0, -1.0), repeat=n):
        rows.append((list(signs), tau + sum(s * x for s, x in zip(signs, w0, strict=True)), ("turn", signs)))
    return rows


def _solve_float(matrix: list[list[float]], rhs: list[float]) -> list[float] | None:
    """Gauss elimination with partial pivoting; None when a pivot is numerically zero."""
    size = len(rhs)
    m = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    for c in range(size):
        p = max(range(c, size), key=lambda r: abs(m[r][c]))
        if abs(m[p][c]) < 1e-12:
            return None
        m[c], m[p] = m[p], m[c]
        for r in range(size):
            if r != c and m[r][c] != 0.0:
                factor = m[r][c] / m[c][c]
                m[r] = [x - factor * y for x, y in zip(m[r], m[c], strict=True)]
    return [m[i][size] / m[i][i] for i in range(size)]


def _kkt_for_set(
    hessian: list[list[float]],
    gradient_constant: list[float],
    rows: list[tuple[list[float], float, tuple[object, ...]]],
    chosen: tuple[int, ...],
) -> tuple[list[float], float, list[float]] | None:
    """Solve P w + q + nu 1 + sum_c lam_c a_c = 0, 1'w = 1, a_c'w = b_c for the chosen rows (unknowns w, nu, lam)."""
    n = len(gradient_constant)
    k = len(chosen)
    size = n + 1 + k
    matrix = [[0.0] * size for _ in range(size)]
    rhs = [0.0] * size
    for i in range(n):
        for j in range(n):
            matrix[i][j] = hessian[i][j]
        matrix[i][n] = 1.0
        for c, idx in enumerate(chosen):
            matrix[i][n + 1 + c] = rows[idx][0][i]
        rhs[i] = -gradient_constant[i]
    for j in range(n):
        matrix[n][j] = 1.0
    rhs[n] = 1.0
    for c, idx in enumerate(chosen):
        a, b, _ = rows[idx]
        for j in range(n):
            matrix[n + 1 + c][j] = a[j]
        rhs[n + 1 + c] = b
    solution = _solve_float(matrix, rhs)
    if solution is None:
        return None
    return solution[:n], solution[n], solution[n + 1 :]


def _enumerate(problem: Problem) -> tuple[list[float], float, dict[tuple[object, ...], float]]:
    """The first working set (smallest first) whose primal point is feasible and whose multipliers are non-negative."""
    n = problem.n
    rows = _rows(problem)
    hessian = [[float(problem.gamma) * float(problem.sigma[i][j]) for j in range(n)] for i in range(n)]
    gradient_constant = [-float(v) for v in problem.mu]
    for size in range(0, n):
        for chosen in combinations(range(len(rows)), size):
            found = _kkt_for_set(hessian, gradient_constant, rows, chosen)
            if found is None:
                continue
            w, nu, lam = found
            if not all(math.isfinite(v) for v in w):
                continue
            if any(sum(a[j] * w[j] for j in range(n)) - b > FLOAT_TOL for a, b, _ in rows):
                continue
            if any(v < -FLOAT_TOL for v in lam):
                continue
            return w, nu, {rows[idx][2]: max(lam[c], 0.0) for c, idx in enumerate(chosen)}
    raise RuntimeError("no working set satisfies the KKT conditions")


def _certificate_float(
    problem: Problem,
    w: list[float],
    budget: float,
    lower: list[float],
    upper: list[float],
    sector: list[float],
    plus: list[float],
    minus: list[float],
    kappa: float,
) -> dict[str, float]:
    n = problem.n
    w0 = [float(v) for v in problem.w0]
    lo = [float(v) for v in problem.lower]
    up = [float(v) for v in problem.upper]
    caps = [float(v) for v in problem.caps]
    tau = float(problem.tau)
    d = [w[i] - w0[i] for i in range(n)]
    t = [abs(x) for x in d]
    sums = [sum(w[i] for i in range(n) if problem.sector[i] == k) for k in range(len(caps))]
    gaps_bounds = [lo[i] - w[i] for i in range(n)] + [w[i] - up[i] for i in range(n)]
    gaps_sector = [sums[k] - caps[k] for k in range(len(caps))]
    gaps_turn = [d[i] - t[i] for i in range(n)] + [-d[i] - t[i] for i in range(n)]
    gaps_total = [sum(t) - tau]
    primal = max([0.0, abs(sum(w) - 1.0)] + gaps_bounds + gaps_sector + gaps_turn + gaps_total)
    mults = lower + upper + sector + plus + minus + [kappa]
    gaps = gaps_bounds + gaps_sector + gaps_turn + gaps_total
    dual = max(0.0, -min(mults))
    comp = max(abs(m * g) for m, g in zip(mults, gaps, strict=True))
    stat = 0.0
    for i in range(n):
        grad = float(problem.gamma) * sum(float(problem.sigma[i][j]) * w[j] for j in range(n)) - float(problem.mu[i])
        r_w = grad + budget - lower[i] + upper[i] + sector[problem.sector[i]] + plus[i] - minus[i]
        r_t = kappa - plus[i] - minus[i]
        stat = max(stat, abs(r_w), abs(r_t))
    return {
        "primal_residual": primal,
        "stationarity_residual": stat,
        "dual_residual": dual,
        "complementary_slackness": comp,
    }


def allocate(instance: dict[str, Any]) -> dict[str, Any]:
    problem = _parse(instance)
    n = problem.n
    w, nu, mult = _enumerate(problem)
    lower = [mult.get(("lower", i), 0.0) for i in range(n)]
    upper = [mult.get(("upper", i), 0.0) for i in range(n)]
    sector = [mult.get(("sector", k), 0.0) for k in range(len(problem.caps))]
    signs = {key[1]: value for key, value in mult.items() if key[0] == "turn"}
    kappa = sum(signs.values())
    plus = [(kappa + sum(eta * s[i] for s, eta in signs.items())) / 2 for i in range(n)]
    minus = [(kappa - sum(eta * s[i] for s, eta in signs.items())) / 2 for i in range(n)]
    certificate = _certificate_float(problem, w, nu, lower, upper, sector, plus, minus, kappa)
    return {
        "weights": w,
        "multipliers": {
            "budget": nu,
            "lower": lower,
            "upper": upper,
            "sector": sector,
            "turnover_plus": plus,
            "turnover_minus": minus,
            "turnover_total": kappa,
        },
        "certificate": certificate,
    }
