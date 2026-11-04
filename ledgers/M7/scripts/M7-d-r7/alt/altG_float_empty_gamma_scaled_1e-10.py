"""Alternative G (gamma-scaled variant of D): Hessian Sigma, linear term mu / gamma, multipliers times gamma.
Alternative D: float active set from the empty working set, dropping the latest-added negative multiplier, cutoffs of 1e-10."""

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




EXACT = False
START = "empty"  # "tight": the rows active at w0 (within 1e-9); "empty": none
DROP = "last_added"  # "most_negative": drop the most negative multiplier; "last_added": drop the latest-added negative one
TIE = "last"  # "first" or "last": which of several equal minimal ratios blocks
ZERO = 1e-10  # a pivot, step or residual at or below this size counts as zero
MULT_TOL = 1e-10  # a multiplier below minus this is negative
POLISH = False  # True: after the float search, re-solve the final active set exactly


class _Singular(Exception):
    pass


def _num(x: Fraction) -> Any:
    return x if EXACT else float(x)


def _is_zero(x: Any) -> bool:
    return x == 0 if EXACT else abs(x) <= ZERO


def _pos(x: Any) -> bool:
    return x > 0 if EXACT else x > ZERO


def _neg_mult(x: Any) -> bool:
    return x < 0 if EXACT else x < -MULT_TOL


def _dot(a: Sequence[Any], b: Sequence[Any]) -> Any:
    total: Any = Fraction(0) if EXACT else 0.0
    for x, y in zip(a, b, strict=True):
        total = total + x * y
    return total


def _solve_linear(matrix: list[list[Any]], rhs: list[Any], scale: float = 1.0) -> list[Any]:
    size = len(rhs)
    rows = [[*matrix[i][:], rhs[i]] for i in range(size)]
    for col in range(size):
        if EXACT:
            pivot = next((r for r in range(col, size) if rows[r][col] != 0), None)
        else:
            pivot = max(range(col, size), key=lambda r: abs(rows[r][col]))
            if abs(rows[pivot][col]) <= ZERO * scale:
                pivot = None
        if pivot is None:
            raise _Singular()
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(size):
            if r != col and rows[r][col] != 0:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[col], strict=True)]
    return [rows[i][size] / rows[i][i] for i in range(size)]


def _rank(vectors: list[list[Any]]) -> int:
    rows = [v[:] for v in vectors]
    rank = 0
    scale = max((abs(v) for row in rows for v in row), default=1.0) or 1.0
    width = len(rows[0]) if rows else 0
    for col in range(width):
        if EXACT:
            pivot = next((r for r in range(rank, len(rows)) if rows[r][col] != 0), None)
        else:
            cand = max(range(rank, len(rows)), key=lambda r: abs(rows[r][col]), default=None)
            pivot = cand if cand is not None and abs(rows[cand][col]) > ZERO * scale else None
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(len(rows)):
            if r != rank and rows[r][col] != 0:
                factor = rows[r][col] / rows[rank][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[rank], strict=True)]
        rank += 1
    return rank


def _kkt_step(hessian: list[list[Any]], gradient: list[Any], active: list[list[Any]]) -> tuple[list[Any], list[Any]]:
    n, m = len(gradient), len(active)
    size = n + m
    zero: Any = Fraction(0) if EXACT else 0.0
    matrix = [[zero] * size for _ in range(size)]
    for i in range(n):
        for j in range(n):
            matrix[i][j] = hessian[i][j]
    for k, a in enumerate(active):
        for i in range(n):
            matrix[i][n + k] = a[i]
            matrix[n + k][i] = a[i]
    # pivot cutoffs are relative to the size of the Hessian block, so a small gamma is not read as singular
    scale = max((abs(hessian[i][j]) for i in range(n) for j in range(n)), default=1.0) or 1.0
    solution = _solve_linear(matrix, [-g for g in gradient] + [zero] * m, float(scale))
    return solution[:n], solution[n:]


def _rows_of(problem: Problem, ) -> list[tuple[list[Any], Any, tuple[object, ...]]]:
    n = problem.n
    one: Any = Fraction(1) if EXACT else 1.0
    zero: Any = Fraction(0) if EXACT else 0.0
    rows: list[tuple[list[Any], Any, tuple[object, ...]]] = []
    for i in range(n):
        rows.append(([-one if j == i else zero for j in range(n)], _num(-problem.lower[i]), ("lower", i)))
        rows.append(([one if j == i else zero for j in range(n)], _num(problem.upper[i]), ("upper", i)))
    for k, cap in enumerate(problem.caps):
        rows.append(([one if problem.sector[j] == k else zero for j in range(n)], _num(cap), ("sector", k)))
    w0 = [_num(v) for v in problem.w0]
    for signs in product((1, -1), repeat=n):
        a = [_num(Fraction(s)) for s in signs]
        rows.append((a, _num(problem.tau) + _dot(a, w0), ("turn", signs)))
    return rows


def _search(problem: Problem, rows: list[tuple[list[Any], Any, tuple[object, ...]]]) -> tuple[list[Any], list[int], Any]:
    n = problem.n
    one: Any = Fraction(1) if EXACT else 1.0
    hessian = [[_num(problem.sigma[i][j]) for j in range(n)] for i in range(n)]
    mu = [_num(v / problem.gamma) for v in problem.mu]
    budget = [one] * n
    x = [_num(v) for v in problem.w0]
    working: list[int] = []
    if START == "tight":
        tight_tol = Fraction(1, 10**9) if EXACT else 1e-9
        for j, (a, b, _) in enumerate(rows):
            slack = b - _dot(a, x)
            if slack <= tight_tol and _rank([budget, *(rows[k][0] for k in working), a]) > len(working) + 1:
                working.append(j)
    for _ in range(500):
        gradient = [_dot(hessian[i], x) - mu[i] for i in range(n)]
        p, lam = _kkt_step(hessian, gradient, [budget] + [rows[j][0] for j in working])
        if all(_is_zero(v) for v in p):
            negative = [(lam[1 + k], k) for k in range(len(working)) if _neg_mult(lam[1 + k])]
            if not negative:
                return x, list(working), lam[0]
            idx = min(negative)[1] if DROP == "most_negative" else negative[-1][1]
            working.pop(idx)
            continue
        step: Any = one
        blocking: int | None = None
        for j, (a, b, _) in enumerate(rows):
            if j in working:
                continue
            rate = _dot(a, p)
            if _pos(rate):
                slack = b - _dot(a, x)
                if EXACT:
                    ratio = max(slack, Fraction(0)) / rate
                else:
                    ratio = max(slack, 0.0) / rate
                if ratio < step or (TIE == "last" and blocking is not None and ratio == step):
                    step, blocking = ratio, j
        x = [xi + step * pi for xi, pi in zip(x, p, strict=True)]
        if blocking is not None:
            working.append(blocking)
    raise RuntimeError("the active-set search did not converge")


def _polish(problem: Problem, rows: list[tuple[list[Any], Any, tuple[object, ...]]], working: list[int]) -> tuple[list[Fraction], list[Fraction], Fraction]:
    """Exact re-solve of the equality system: the budget and the working rows held with equality."""
    n = problem.n
    hessian = [[problem.gamma * problem.sigma[i][j] for j in range(n)] for i in range(n)]
    active = [([Fraction(1)] * n, Fraction(1))] + [
        ([Fraction(v) for v in rows[j][0]], Fraction(0) if False else _exact_rhs(rows[j][1])) for j in working
    ]
    m = len(active)
    size = n + m
    matrix = [[Fraction(0)] * size for _ in range(size)]
    rhs = [Fraction(0)] * size
    for i in range(n):
        for j in range(n):
            matrix[i][j] = hessian[i][j]
        rhs[i] = problem.mu[i]
    for k, (a, b) in enumerate(active):
        for i in range(n):
            matrix[i][n + k] = -a[i]
            matrix[n + k][i] = a[i]
        rhs[n + k] = b
    solution = _solve_exact(matrix, rhs)
    # stationarity was written as H x - sum a_k y_k = mu, so the Lagrangian multiplier is -y_k
    return solution[:n], [-v for v in solution[n + 1 :]], -solution[n]


def _exact_rhs(value: Any) -> Fraction:
    return Fraction(value) if not isinstance(value, Fraction) else value


def _solve_exact(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
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


def _solve(problem: Problem) -> dict[str, Any]:
    n = problem.n
    rows = _rows_of(problem)
    x, working, budget_mult = _search(problem, rows)
    if POLISH:
        x_exact, lam_exact, budget_exact = _polish(problem, rows, working)
        x = [float(v) for v in x_exact]
        budget_mult = budget_exact
        lam_values = [float(v) for v in lam_exact]
    else:
        lam_values = None
    mult_by_key: dict[tuple[object, ...], Any] = {}
    # Multipliers of the search: solve the stationarity with the final working set (float or exact as configured).
    hessian = [[_num(problem.sigma[i][j]) for j in range(n)] for i in range(n)]
    mu = [_num(v / problem.gamma) for v in problem.mu]
    one: Any = Fraction(1) if EXACT else 1.0
    xs = [_num(v) for v in x]
    gradient = [_dot(hessian[i], xs) - mu[i] for i in range(n)]
    p, lam = _kkt_step(hessian, gradient, [[one] * n] + [rows[j][0] for j in working])
    for k, j in enumerate(working):
        mult_by_key[rows[j][2]] = float(lam[1 + k]) * float(problem.gamma) if lam_values is None else lam_values[k]
    budget_value = (float(lam[0]) if budget_mult is None else float(budget_mult)) * float(problem.gamma)
    lower = [mult_by_key.get(("lower", i), 0.0) for i in range(n)]
    upper = [mult_by_key.get(("upper", i), 0.0) for i in range(n)]
    sector = [mult_by_key.get(("sector", k), 0.0) for k in range(len(problem.caps))]
    sign_multipliers = {key[1]: value for key, value in mult_by_key.items() if key[0] == "turn"}
    kappa = sum(sign_multipliers.values(), 0.0)
    plus = [0.0] * n
    minus = [0.0] * n
    for i in range(n):
        net = sum(eta * s[i] for s, eta in sign_multipliers.items())
        plus[i] = (kappa + net) / 2
        minus[i] = (kappa - net) / 2
    return {"w": x, "budget": budget_value, "lower": lower, "upper": upper, "sector": sector,
            "plus": plus, "minus": minus, "kappa": kappa}


def _certificate(case: Problem, out: dict[str, Any]) -> dict[str, float]:
    n = case.n
    w = [float(v) for v in out["w"]]
    w0 = [float(v) for v in case.w0]
    lower = [float(v) for v in case.lower]
    upper = [float(v) for v in case.upper]
    caps = [float(v) for v in case.caps]
    d = [w[i] - w0[i] for i in range(n)]
    t = [abs(v) for v in d]
    sums = [sum(w[i] for i in range(n) if case.sector[i] == k) for k in range(len(caps))]
    gaps = []
    for i in range(n):
        gaps += [lower[i] - w[i], w[i] - upper[i], d[i] - t[i], -d[i] - t[i]]
    gaps += [sums[k] - caps[k] for k in range(len(caps))]
    gaps.append(sum(t) - float(case.tau))
    primal = max([0.0, abs(sum(w) - 1.0), *gaps])
    ineq = [*out["lower"], *out["upper"], *out["sector"], *out["plus"], *out["minus"], out["kappa"]]
    dual = max(0.0, -min(ineq))
    gvals = [*[lower[i] - w[i] for i in range(n)], *[w[i] - upper[i] for i in range(n)],
             *[sums[k] - caps[k] for k in range(len(caps))], *[d[i] - t[i] for i in range(n)],
             *[-d[i] - t[i] for i in range(n)], sum(t) - float(case.tau)]
    comp = max(abs(m * g) for m, g in zip(ineq, gvals, strict=True))
    stat = 0.0
    gamma = float(case.gamma)
    for i in range(n):
        grad = gamma * sum(float(case.sigma[i][j]) * w[j] for j in range(n)) - float(case.mu[i])
        rw = grad + out["budget"] - out["lower"][i] + out["upper"][i] + out["sector"][case.sector[i]]
        rw += out["plus"][i] - out["minus"][i]
        rt = out["kappa"] - out["plus"][i] - out["minus"][i]
        stat = max(stat, abs(rw), abs(rt))
    return {"primal_residual": primal, "stationarity_residual": stat, "dual_residual": dual,
            "complementary_slackness": comp}


def allocate(instance: dict[str, Any]) -> dict[str, Any]:
    problem = _parse(instance)
    out = _solve(problem)
    multipliers = {
        "budget": float(out["budget"]),
        "lower": [float(v) for v in out["lower"]],
        "upper": [float(v) for v in out["upper"]],
        "sector": [float(v) for v in out["sector"]],
        "turnover_plus": [float(v) for v in out["plus"]],
        "turnover_minus": [float(v) for v in out["minus"]],
        "turnover_total": float(out["kappa"]),
    }
    return {"weights": [float(v) for v in out["w"]], "multipliers": multipliers,
            "certificate": _certificate(problem, out)}
