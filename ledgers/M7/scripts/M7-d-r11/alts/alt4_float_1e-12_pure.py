"""Alt-4 (verifier r11): pure float active set with tolerance 1e-12 and float multipliers, no exact polish.

Reference solution for the M7 constrained allocator (constrained_allocator.py): an exact active-set solver.

The problem is the one the project page states: minimize (gamma / 2) w' Sigma w - mu' w over the budget, the box, the
sector caps and the turnover limit. Turnover is written in the linearized form of the page, with auxiliary variables
t_i = |w_i - w0_i|. The solver works in exact rational arithmetic (fractions.Fraction read from the decimal text of each
input), so every active-set decision is exact. The turnover limit enters the search as the 2**n sign constraints
sum_i s_i (w_i - w0_i) <= tau, whose intersection is the same set; the multipliers of those constraints are then mapped
back to the linearized form. Nothing here is a real portfolio: every input is SIMULATED.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Any, cast

REQUIRED = ("gamma", "mu", "sigma", "w0", "lower", "upper", "sector", "sector_caps", "turnover_limit")
TOL = Fraction(1, 10**9)  # the tolerance on the starting-portfolio checks and on the active-set test


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


def _inequalities(problem: Problem) -> list[tuple[list[Fraction], Fraction, tuple[object, ...]]]:
    """Rows a.w <= b with a key: lower and upper bounds, sector caps, and the 2**n sign forms of the turnover limit."""
    n = problem.n
    rows: list[tuple[list[Fraction], Fraction, tuple[object, ...]]] = []
    for i in range(n):
        rows.append(([Fraction(-1) if j == i else Fraction(0) for j in range(n)], -problem.lower[i], ("lower", i)))
        rows.append(([Fraction(1) if j == i else Fraction(0) for j in range(n)], problem.upper[i], ("upper", i)))
    for k, cap in enumerate(problem.caps):
        rows.append(([Fraction(1) if problem.sector[j] == k else Fraction(0) for j in range(n)], cap, ("sector", k)))
    for signs in product((1, -1), repeat=n):
        a = [Fraction(s) for s in signs]
        rows.append((a, problem.tau + _dot(a, problem.w0), ("turn", signs)))
    return rows



def _fdot(a, b):
    return sum(x * y for x, y in zip(a, b, strict=True))


def _fsolve(matrix, rhs):
    size = len(rhs)
    rows = [[*matrix[i], rhs[i]] for i in range(size)]
    for col in range(size):
        pivot = max(range(col, size), key=lambda r: abs(rows[r][col]))
        if abs(rows[pivot][col]) == 0.0:
            raise RuntimeError("singular float system")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(size):
            if r != col and rows[r][col] != 0.0:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[col], strict=True)]
    return [rows[i][size] / rows[i][i] for i in range(size)]


def _fkkt(hessian, gradient, active):
    n, m = len(gradient), len(active)
    size = n + m
    matrix = [[0.0] * size for _ in range(size)]
    for i in range(n):
        for j in range(n):
            matrix[i][j] = hessian[i][j]
    for k, a in enumerate(active):
        for i in range(n):
            matrix[i][n + k] = a[i]
            matrix[n + k][i] = a[i]
    solution = _fsolve(matrix, [-g for g in gradient] + [0.0] * m)
    return solution[:n], solution[n:]


def _polish(problem, rows, working):
    """Exact KKT solve on the float working set: H x + A' lambda = mu and A_active x = b. Returns None if not valid."""
    n = problem.n
    active = [([Fraction(1)] * n, Fraction(1))] + [(rows[j][0], rows[j][1]) for j in working]
    size = n + len(active)
    matrix = [[Fraction(0)] * size for _ in range(size)]
    rhs = [Fraction(0)] * size
    for i in range(n):
        for j in range(n):
            matrix[i][j] = problem.gamma * problem.sigma[i][j]
        for c, (a, _) in enumerate(active):
            matrix[i][n + c] = a[i]
        rhs[i] = problem.mu[i]
    for c, (a, b) in enumerate(active):
        for j in range(n):
            matrix[n + c][j] = a[j]
        rhs[n + c] = b
    try:
        solution = _solve_linear(matrix, rhs)
    except (StopIteration, ZeroDivisionError):
        return None
    x, lam = solution[:n], solution[n:]
    if any(_dot(a, x) - b > 0 for a, b, _ in rows):
        return None
    if any(lam[1 + k] < 0 for k in range(len(working))):
        return None
    return x, lam


def _active_set_float(problem, rows, tol, polish):
    n = problem.n
    hessian = [[float(problem.gamma * problem.sigma[i][j]) for j in range(n)] for i in range(n)]
    mu = [float(v) for v in problem.mu]
    dense = [[float(v) for v in a] for a, _, _ in rows]
    bounds = [float(b) for _, b, _ in rows]
    budget = [1.0] * n
    x = [float(v) for v in problem.w0]
    working: list[int] = []
    for j in range(len(rows)):
        if bounds[j] - _fdot(dense[j], x) <= tol and _rank([budget, *(rows[k][0] for k in working), rows[j][0]]) > len(working) + 1:
            working.append(j)
    for _ in range(500):
        gradient = [_fdot(hessian[i], x) - mu[i] for i in range(n)]
        p, lam = _fkkt(hessian, gradient, [budget] + [dense[j] for j in working])
        if max(abs(v) for v in p) <= tol:
            negative = [(lam[1 + k], k) for k in range(len(working)) if lam[1 + k] < -tol]
            if not negative:
                if polish:
                    exact = _polish(problem, rows, working)
                    if exact is not None:
                        xe, le = exact
                        mult = {rows[j][2]: le[1 + k] for k, j in enumerate(working)}
                        return xe, mult, le[0]
                mult = {rows[j][2]: Fraction(lam[1 + k]) for k, j in enumerate(working)}
                return [Fraction(v) for v in x], mult, Fraction(lam[0])
            working.pop(min(negative)[1])
            continue
        step, blocking = 1.0, None
        for j in range(len(rows)):
            if j in working:
                continue
            rate = _fdot(dense[j], p)
            if rate > tol:
                ratio = max(bounds[j] - _fdot(dense[j], x), 0.0) / rate
                if ratio < step:
                    step, blocking = ratio, j
        x = [xi + step * pi for xi, pi in zip(x, p, strict=True)]
        if blocking is not None:
            working.append(blocking)
    raise RuntimeError("the float active-set search did not converge")


def _active_set(problem, rows):
    return _active_set_float(problem, rows, 1e-12, False)


def _solve(problem: Problem) -> dict[str, Any]:
    n = problem.n
    rows = _inequalities(problem)
    x, mult, budget_mult = _active_set(problem, rows)
    lower = [mult.get(("lower", i), Fraction(0)) for i in range(n)]
    upper = [mult.get(("upper", i), Fraction(0)) for i in range(n)]
    sector = [mult.get(("sector", k), Fraction(0)) for k in range(len(problem.caps))]
    sign_multipliers = {cast(tuple[int, ...], key[1]): value for key, value in mult.items() if key[0] == "turn"}
    kappa = sum(sign_multipliers.values(), Fraction(0))
    plus = [Fraction(0)] * n
    minus = [Fraction(0)] * n
    for i in range(n):
        net = sum((eta * s[i] for s, eta in sign_multipliers.items()), Fraction(0))
        plus[i] = (kappa + net) / 2
        minus[i] = (kappa - net) / 2
    return {
        "w": x,
        "budget": budget_mult,
        "lower": lower,
        "upper": upper,
        "sector": sector,
        "plus": plus,
        "minus": minus,
        "kappa": kappa,
    }


def _certificate(problem: Problem, sol: dict[str, Any]) -> dict[str, float]:
    """The four residuals of the page, in exact arithmetic, then rounded to float."""
    n, w, w0 = problem.n, sol["w"], problem.w0
    d = [w[i] - w0[i] for i in range(n)]
    t = [abs(v) for v in d]
    sector_sum = [
        sum((w[i] for i in range(n) if problem.sector[i] == k), Fraction(0)) for k in range(len(problem.caps))
    ]
    gaps: list[Fraction] = []
    for i in range(n):
        gaps.append(problem.lower[i] - w[i])
        gaps.append(w[i] - problem.upper[i])
        gaps.append(d[i] - t[i])
        gaps.append(-d[i] - t[i])
    gaps.extend(sector_sum[k] - problem.caps[k] for k in range(len(problem.caps)))
    gaps.append(sum(t, Fraction(0)) - problem.tau)
    primal = max([Fraction(0), abs(sum(w, Fraction(0)) - 1), *gaps])
    mult_ineq: list[Fraction] = [
        *sol["lower"],
        *sol["upper"],
        *sol["sector"],
        *sol["plus"],
        *sol["minus"],
        sol["kappa"],
    ]
    dual = max(Fraction(0), -min(mult_ineq))
    complementary = max(
        abs(m * g)
        for m, g in zip(
            [*sol["lower"], *sol["upper"], *sol["sector"], *sol["plus"], *sol["minus"], sol["kappa"]],
            [
                *[problem.lower[i] - w[i] for i in range(n)],
                *[w[i] - problem.upper[i] for i in range(n)],
                *[sector_sum[k] - problem.caps[k] for k in range(len(problem.caps))],
                *[d[i] - t[i] for i in range(n)],
                *[-d[i] - t[i] for i in range(n)],
                sum(t, Fraction(0)) - problem.tau,
            ],
            strict=True,
        )
    )
    stationarity = Fraction(0)
    for i in range(n):
        gradient = problem.gamma * _dot(problem.sigma[i], w) - problem.mu[i]
        r_w = gradient + sol["budget"] - sol["lower"][i] + sol["upper"][i] + sol["sector"][problem.sector[i]]
        r_w += sol["plus"][i] - sol["minus"][i]
        r_t = sol["kappa"] - sol["plus"][i] - sol["minus"][i]
        stationarity = max(stationarity, abs(r_w), abs(r_t))
    return {
        "primal_residual": float(primal),
        "stationarity_residual": float(stationarity),
        "dual_residual": float(dual),
        "complementary_slackness": float(complementary),
    }


def allocate(instance: dict[str, Any]) -> dict[str, Any]:
    problem = _parse(instance)
    sol = _solve(problem)
    multipliers = {
        "budget": float(sol["budget"]),
        "lower": [float(v) for v in sol["lower"]],
        "upper": [float(v) for v in sol["upper"]],
        "sector": [float(v) for v in sol["sector"]],
        "turnover_plus": [float(v) for v in sol["plus"]],
        "turnover_minus": [float(v) for v in sol["minus"]],
        "turnover_total": float(sol["kappa"]),
    }
    return {
        "weights": [float(v) for v in sol["w"]],
        "multipliers": multipliers,
        "certificate": _certificate(problem, sol),
    }
