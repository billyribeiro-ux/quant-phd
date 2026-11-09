"""Round-12 verifier alternative: alt_r12_7_float_objective_over_gamma_scaled_1e-10_polish. Independent solver, validation copied from the reference.
Arithmetic float; activity cutoff 1e-10; drop rule most_negative; ratio ties largest_rate; exact polish True. Stdlib only."""
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


MODE = "float"
ACT_CUT = 1e-10
RATE_CUT = 1e-12
RANK_CUT = 1e-13
DROP = "most_negative"
TIE = "largest_rate"
POLISH = True
SCALE_OBJ = True
ONE = Fraction(1) if MODE == "exact" else 1.0
ZERO = Fraction(0) if MODE == "exact" else 0.0


def _is_zero(v: Any) -> bool:
    return v == 0 if MODE == "exact" else abs(v) <= RATE_CUT


def _dot(a: Any, b: Any) -> Any:
    total = ZERO
    for x, y in zip(a, b, strict=True):
        total = total + x * y
    return total


def _solve_sys(matrix: list[list[Any]], rhs: list[Any]) -> list[Any]:
    size = len(rhs)
    rows = [list(matrix[i]) + [rhs[i]] for i in range(size)]
    for col in range(size):
        if MODE == "exact":
            piv = next((r for r in range(col, size) if rows[r][col] != 0), None)
        else:
            piv = max(range(col, size), key=lambda r: abs(rows[r][col]))
            if abs(rows[piv][col]) <= RANK_CUT:
                piv = None
        if piv is None:
            raise RuntimeError("singular system")
        rows[col], rows[piv] = rows[piv], rows[col]
        for r in range(size):
            if r != col and rows[r][col] != 0:
                f = rows[r][col] / rows[col][col]
                rows[r] = [x - f * y for x, y in zip(rows[r], rows[col], strict=True)]
    return [rows[i][size] / rows[i][i] for i in range(size)]


def _rank(vectors: list[list[Any]]) -> int:
    rows = [list(v) for v in vectors]
    rank = 0
    width = len(rows[0]) if rows else 0
    for col in range(width):
        cands = [r for r in range(rank, len(rows)) if (rows[r][col] != 0 if MODE == "exact" else abs(rows[r][col]) > RANK_CUT)]
        if not cands:
            continue
        piv = max(cands, key=lambda r: abs(rows[r][col]))
        rows[rank], rows[piv] = rows[piv], rows[rank]
        for r in range(rank + 1, len(rows)):
            f = rows[r][col] / rows[rank][col]
            rows[r] = [x - f * y for x, y in zip(rows[r], rows[rank], strict=True)]
        rank += 1
    return rank


def _kkt_direction(hess: list[list[Any]], grad: list[Any], acts: list[list[Any]]) -> tuple[list[Any], list[Any]]:
    n, m = len(grad), len(acts)
    size = n + m
    matrix = [[ZERO] * size for _ in range(size)]
    for i in range(n):
        for j in range(n):
            matrix[i][j] = hess[i][j]
    for k, a in enumerate(acts):
        for i in range(n):
            matrix[i][n + k] = a[i]
            matrix[n + k][i] = a[i]
    sol = _solve_sys(matrix, [-g for g in grad] + [ZERO] * m)
    return sol[:n], sol[n:]


def _rows(problem: Problem) -> list[tuple[list[Any], Any, tuple[object, ...]]]:
    n = problem.n
    out: list[tuple[list[Any], Any, tuple[object, ...]]] = []
    conv = (lambda v: Fraction(v)) if MODE == "exact" else (lambda v: float(v))
    for i in range(n):
        out.append(([-ONE if j == i else ZERO for j in range(n)], conv(-problem.lower[i]), ("lower", i)))
        out.append(([ONE if j == i else ZERO for j in range(n)], conv(problem.upper[i]), ("upper", i)))
    for k, cap in enumerate(problem.caps):
        out.append(([ONE if problem.sector[j] == k else ZERO for j in range(n)], conv(cap), ("sector", k)))
    w0 = [conv(v) for v in problem.w0]
    for signs in product((1, -1), repeat=n):
        a = [ONE if s == 1 else -ONE for s in signs]
        out.append((a, conv(problem.tau) + _dot(a, w0), ("turn", signs)))
    return out


def _active(problem: Problem) -> tuple[list[Any], dict[tuple[object, ...], Any], Any]:
    n = problem.n
    conv = (lambda v: Fraction(v)) if MODE == "exact" else (lambda v: float(v))
    if SCALE_OBJ:
        hess = [[conv(problem.sigma[i][j]) for j in range(n)] for i in range(n)]
        mu = [conv(v) / conv(problem.gamma) for v in problem.mu]
    else:
        hess = [[conv(problem.gamma) * conv(problem.sigma[i][j]) for j in range(n)] for i in range(n)]
        mu = [conv(v) for v in problem.mu]
    rows = _rows(problem)
    budget = [ONE] * n
    x = [conv(v) for v in problem.w0]

    def act(b: Any) -> Any:
        return ACT_CUT * max(ONE, abs(b)) if MODE != "exact" and True else ACT_CUT

    working: list[int] = []
    for j, (a, b, _) in enumerate(rows):
        slack = b - _dot(a, x)
        if slack <= act(b) and _rank([budget, *(rows[k][0] for k in working), a]) > len(working) + 1:
            working.append(j)
    for _ in range(2000):
        grad = [_dot(hess[i], x) - mu[i] for i in range(n)]
        p, lam = _kkt_direction(hess, grad, [budget, *(rows[j][0] for j in working)])
        if all(_is_zero(v) for v in p):
            negs = [(lam[1 + k], k) for k in range(len(working)) if (lam[1 + k] < 0 if MODE == "exact" else lam[1 + k] < -RATE_CUT)]
            if not negs:
                mults = {rows[j][2]: lam[1 + k] for k, j in enumerate(working)}
                return [xi for xi in x], mults, lam[0], working, rows
            if DROP == "min_index":
                _, k = min(negs, key=lambda t: working[t[1]])
            else:
                _, k = min(negs)
            working.pop(k)
            continue
        step = ONE
        block: int | None = None
        block_rate = ZERO
        for j, (a, b, _) in enumerate(rows):
            if j in working:
                continue
            rate = _dot(a, p)
            if rate > RATE_CUT if MODE != "exact" else rate > 0:
                ratio = max(b - _dot(a, x), ZERO) / rate
                if ratio < step or (TIE == "largest_rate" and block is not None and ratio == step and rate > block_rate):
                    step, block, block_rate = ratio, j, rate
        x = [xi + step * pi for xi, pi in zip(x, p, strict=True)]
        if block is not None:
            if _rank([budget, *(rows[j][0] for j in working), rows[block][0]]) <= len(working) + 1:
                raise RuntimeError("working set dependent")
            working.append(block)
    raise RuntimeError("no convergence")


def _exact_row(problem: Problem, key: tuple[object, ...]) -> tuple[list[Fraction], Fraction]:
    n = problem.n
    if key[0] == "lower":
        i = key[1]
        return [Fraction(-1) if j == i else Fraction(0) for j in range(n)], -problem.lower[i]
    if key[0] == "upper":
        i = key[1]
        return [Fraction(1) if j == i else Fraction(0) for j in range(n)], problem.upper[i]
    if key[0] == "sector":
        k = key[1]
        return [Fraction(1) if problem.sector[j] == k else Fraction(0) for j in range(n)], problem.caps[k]
    signs = key[1]
    return [Fraction(s) for s in signs], problem.tau + sum(
        (Fraction(s) * problem.w0[i] for i, s in enumerate(signs)), Fraction(0)
    )


def _exact_polish(problem: Problem, working: list[int], rows: list[Any]) -> tuple[list[Fraction], list[Fraction]]:
    n = problem.n
    hess = [[problem.gamma * problem.sigma[i][j] for j in range(n)] for i in range(n)]
    exact_rows = [_exact_row(problem, rows[j][2]) for j in working]
    acts = [[Fraction(1)] * n] + [a for a, _ in exact_rows]
    bvals = [Fraction(1)] + [b for _, b in exact_rows]
    size = n + len(acts)
    matrix = [[Fraction(0)] * size for _ in range(size)]
    for i in range(n):
        for j in range(n):
            matrix[i][j] = hess[i][j]
    for k, a in enumerate(acts):
        for i in range(n):
            matrix[i][n + k] = a[i]
            matrix[n + k][i] = a[i]
    sol = _solve_sys(matrix, [problem.mu[i] for i in range(n)] + bvals)
    return sol[:n], sol[n:]


def _cert(problem: Problem, w: list[float], out: dict[str, Any]) -> dict[str, float]:
    n = problem.n
    lo = [float(v) for v in problem.lower]
    up = [float(v) for v in problem.upper]
    w0 = [float(v) for v in problem.w0]
    caps = [float(v) for v in problem.caps]
    tau = float(problem.tau)
    gam = float(problem.gamma)
    sig = [[float(v) for v in row] for row in problem.sigma]
    mu = [float(v) for v in problem.mu]
    sec = problem.sector
    d = [w[i] - w0[i] for i in range(n)]
    t = [abs(v) for v in d]
    ssum = [sum(w[i] for i in range(n) if sec[i] == k) for k in range(len(caps))]
    m = out["multipliers"]
    lower_m, upper_m, sector_m = m["lower"], m["upper"], m["sector"]
    plus, minus, kappa = m["turnover_plus"], m["turnover_minus"], m["turnover_total"]
    gaps = []
    comp_g = []
    for i in range(n):
        gaps += [lo[i] - w[i], w[i] - up[i], d[i] - t[i], -d[i] - t[i]]
    comp_g += [lo[i] - w[i] for i in range(n)] + [w[i] - up[i] for i in range(n)]
    comp_g += [ssum[k] - caps[k] for k in range(len(caps))]
    comp_g += [d[i] - t[i] for i in range(n)] + [-d[i] - t[i] for i in range(n)]
    gaps += [ssum[k] - caps[k] for k in range(len(caps))]
    gaps += [sum(t) - tau]
    comp_g += [sum(t) - tau]
    primal = max([0.0, abs(sum(w) - 1.0), *gaps])
    ineq = [*lower_m, *upper_m, *sector_m, *plus, *minus, kappa]
    dual = max(0.0, -min(ineq))
    comp = max(abs(a * b) for a, b in zip(ineq, comp_g, strict=True))
    stat = 0.0
    for i in range(n):
        grad = gam * sum(sig[i][j] * w[j] for j in range(n)) - mu[i]
        rw = grad + m["budget"] - lower_m[i] + upper_m[i] + sector_m[sec[i]] + plus[i] - minus[i]
        rt = kappa - plus[i] - minus[i]
        stat = max(stat, abs(rw), abs(rt))
    return {
        "primal_residual": primal,
        "stationarity_residual": stat,
        "dual_residual": dual,
        "complementary_slackness": comp,
    }


def allocate(instance: dict[str, Any]) -> dict[str, Any]:
    problem = _parse(instance)
    n = problem.n
    x, mults, budget_mult, working, rows = _active(problem)
    if SCALE_OBJ:
        g = float(problem.gamma)
        budget_mult = budget_mult * g
        mults = {k: v * g for k, v in mults.items()}
    if POLISH:
        xe, lam = _exact_polish(problem, working, rows)
        x = xe
        budget_mult = lam[0]
        mults = {rows[j][2]: lam[1 + k] for k, j in enumerate(working)}
    lower = [mults.get(("lower", i), 0) for i in range(n)]
    upper = [mults.get(("upper", i), 0) for i in range(n)]
    sector = [mults.get(("sector", k), 0) for k in range(len(problem.caps))]
    signs = {key[1]: v for key, v in mults.items() if key[0] == "turn"}
    kappa = sum(signs.values(), ZERO)
    net = [sum((eta * s[i] for s, eta in signs.items()), ZERO) for i in range(n)]
    plus = [(kappa + net[i]) / 2 for i in range(n)]
    minus = [(kappa - net[i]) / 2 for i in range(n)]
    weights = [float(v) for v in x]
    out_mult = {
        "budget": float(budget_mult),
        "lower": [float(v) for v in lower],
        "upper": [float(v) for v in upper],
        "sector": [float(v) for v in sector],
        "turnover_plus": [float(v) for v in plus],
        "turnover_minus": [float(v) for v in minus],
        "turnover_total": float(kappa),
    }
    out = {"weights": weights, "multipliers": out_mult}
    out["certificate"] = _cert(problem, weights, out)
    return out
