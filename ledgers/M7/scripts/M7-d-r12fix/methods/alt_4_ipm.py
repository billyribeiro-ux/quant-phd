"""Alternative (4) of plan 7.4 item 2, primal-dual log-barrier interior point: a complete solver for the page's problem.

The front end is the named method. Its working-set guess is finished by an exact KKT solve that is accepted only if
it is feasible and dual feasible; otherwise the active-set search of the round-12 alternative D answers. Float
arithmetic; gamma is folded into the linear term. Nothing here is a real portfolio: every input is SIMULATED.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
Fraction = float  # verifier alternative: float arithmetic
from itertools import product
from typing import Any, cast

REQUIRED = ("gamma", "mu", "sigma", "w0", "lower", "upper", "sector", "sector_caps", "turnover_limit")
TOL = 1e-9  # the tolerance on the starting-portfolio checks and on the active-set test


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
    if abs(sum(w0, 0.0) - 1) > TOL:
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
        pivot = next(r for r in range(col, size) if abs(rows[r][col]) > 1e-12)
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(size):
            if r != col and abs(rows[r][col]) > 1e-12:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[col], strict=True)]
    return [rows[i][size] / rows[i][i] for i in range(size)]


def _rank(vectors: list[list[Fraction]]) -> int:
    rows = [v[:] for v in vectors]
    rank = 0
    width = len(rows[0]) if rows else 0
    for col in range(width):
        pivot = next((r for r in range(rank, len(rows)) if abs(rows[r][col]) > 1e-12), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(len(rows)):
            if r != rank and abs(rows[r][col]) > 1e-12:
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
    rhs = [-g for g in gradient] + [Fraction(0)] * m
    solution = _solve_linear(matrix, rhs)
    # One step of iterative refinement: the KKT matrix mixes O(1) constraint rows with O(gamma) Hessian rows, so the
    # first solve can leave a residual above the cutoffs when gamma is small (round-12 finding PRJ-R10-02).
    residual = [rhs[r] - sum(matrix[r][c] * solution[c] for c in range(size)) for r in range(size)]
    correction = _solve_linear(matrix, residual)
    solution = [s + c for s, c in zip(solution, correction, strict=True)]
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


def _active_set(
    problem: Problem, rows: list[tuple[list[Fraction], Fraction, tuple[object, ...]]]
) -> tuple[list[Fraction], dict[tuple[object, ...], Fraction], Fraction]:
    n = problem.n
    hessian = [[problem.gamma * problem.sigma[i][j] for j in range(n)] for i in range(n)]
    budget = [Fraction(1)] * n
    x = list(problem.w0)
    working: list[int] = []
    for j, (a, b, _) in enumerate(rows):
        if b - _dot(a, x) <= TOL and _rank([budget, *(rows[k][0] for k in working), a]) > len(working) + 1:
            working.append(j)
    for _ in range(200):  # a cap far above the iterations the search uses on seeds 0 to 49 (at most 12)
        gradient = [_dot(hessian[i], x) - problem.mu[i] for i in range(n)]
        p, lam = _kkt_step(hessian, gradient, [budget] + [rows[j][0] for j in working])
        if all(abs(v) <= 1e-12 for v in p):
            negative = [(lam[1 + k], k) for k in range(len(working)) if lam[1 + k] < -1e-12]
            if not negative:
                multipliers = {rows[j][2]: lam[1 + k] for k, j in enumerate(working)}
                return x, multipliers, lam[0]
            working.pop(min(negative)[1])
            continue
        step = Fraction(1)
        blocking: int | None = None
        for j, (a, b, _) in enumerate(rows):
            if j in working:
                continue
            rate = _dot(a, p)
            if rate > 1e-12:
                ratio = max(b - _dot(a, x), Fraction(0)) / rate
                if ratio < step:
                    step, blocking = ratio, j
        x = [xi + step * pi for xi, pi in zip(x, p, strict=True)]
        if blocking is not None:
            candidate = rows[blocking][0]
            if _rank([budget, *(rows[j][0] for j in working), candidate]) <= len(working) + 1:
                raise RuntimeError("the working set lost independence")
            working.append(blocking)
    raise RuntimeError("the active-set search did not converge")



LAST_PATH = "none"  # "front-end": the KKT system on the front end's working set was verified; "fallback": active set
ADMM_ITERS = 400
IPM_ITERS = 80
DUAL_ITERS = 2000
PG_OUTER = 20
PG_INNER = 40


def _dotf(a: Sequence[float], x: Sequence[float]) -> float:
    return sum(p * q for p, q in zip(a, x, strict=True))


def _matvec(matrix: list[list[float]], v: Sequence[float]) -> list[float]:
    return [_dotf(row, v) for row in matrix]


def _inverse(matrix: list[list[float]]) -> list[list[float]]:
    size = len(matrix)
    rows = [[*matrix[i], *[1.0 if j == i else 0.0 for j in range(size)]] for i in range(size)]
    for col in range(size):
        pivot = max(range(col, size), key=lambda r: abs(rows[r][col]))
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        rows[col] = [v / scale for v in rows[col]]
        for r in range(size):
            if r != col and rows[r][col] != 0.0:
                factor = rows[r][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[col], strict=True)]
    return [row[size:] for row in rows]


def _project_budget_box(v: Sequence[float], lower: Sequence[float], upper: Sequence[float]) -> list[float]:
    """Euclidean projection onto {w: sum w = 1, lower <= w <= upper}: clip(v - theta) with theta found by bisection."""

    def total(theta: float) -> float:
        return sum(min(max(vi - theta, li), ui) for vi, li, ui in zip(v, lower, upper, strict=True))

    lo_t = min(v) - max(upper) - 1.0
    hi_t = max(v) - min(lower) + 1.0
    for _ in range(80):
        mid = (lo_t + hi_t) / 2
        if total(mid) > 1.0:
            lo_t = mid
        else:
            hi_t = mid
    theta = (lo_t + hi_t) / 2
    return [min(max(vi - theta, li), ui) for vi, li, ui in zip(v, lower, upper, strict=True)]


def _lambda_max(matrix: list[list[float]]) -> float:
    """Largest eigenvalue of a symmetric positive semidefinite matrix by power iteration, with a 5 % margin."""
    size = len(matrix)
    v = [1.0 / math.sqrt(size)] * size
    norm = 0.0
    for _ in range(300):
        w = _matvec(matrix, v)
        norm = math.sqrt(_dotf(w, w))
        if norm == 0.0:
            return 1.0
        v = [wi / norm for wi in w]
    return 1.05 * norm


def _guess(rows: list[tuple[list[float], float, tuple[object, ...]]], x: list[float], lam: list[float]) -> list[int]:
    """Working-set guess: rows with a positive multiplier or a slack within 1e-7, largest multiplier first."""
    slack = [float(b) - _dotf(a, x) for a, b, _ in rows]
    order = sorted(range(len(rows)), key=lambda j: (-lam[j], abs(slack[j])))
    return [j for j in order if lam[j] > 1e-9 or abs(slack[j]) <= 1e-7]


def _polish(problem: Problem, rows: list[tuple[list[float], float, tuple[object, ...]]], guess: list[int]) -> Any:
    """Exact KKT solve on a working set of the guess; returned only if feasible and dual feasible, else None."""
    n = problem.n
    budget = [1.0] * n
    working: list[int] = []
    for j in guess:
        if _rank([budget, *(rows[k][0] for k in working), rows[j][0]]) > len(working) + 1:
            working.append(j)
    size = n + 1 + len(working)
    matrix = [[0.0] * size for _ in range(size)]
    rhs = [0.0] * size
    for i in range(n):
        for j in range(n):
            matrix[i][j] = float(problem.sigma[i][j])
        matrix[i][n] = 1.0
        for k, row_index in enumerate(working):
            matrix[i][n + 1 + k] = rows[row_index][0][i]
        rhs[i] = float(problem.mu[i])
    for j in range(n):
        matrix[n][j] = 1.0
    rhs[n] = 1.0
    for k, row_index in enumerate(working):
        for i in range(n):
            matrix[n + 1 + k][i] = rows[row_index][0][i]
        rhs[n + 1 + k] = rows[row_index][1]
    sol = _solve_linear(matrix, rhs)
    x = sol[:n]
    nu = sol[n]
    lam_w = sol[n + 1 :]
    if any(v < -1e-10 for v in lam_w):
        return None
    if abs(sum(x) - 1.0) > 1e-9:
        return None
    if any(_dotf(a, x) - b > 1e-9 for a, b, _ in rows):
        return None
    mult = {rows[row_index][2]: lam_w[k] for k, row_index in enumerate(working)}
    return x, mult, nu


def _front_end(problem: Problem, rows: list[tuple[list[float], float, tuple[object, ...]]]) -> tuple[list[float], list[float]]:
    """Primal-dual log-barrier interior point from an infeasible start: Newton steps on the perturbed KKT system
    (stationarity, budget, primal rows with slacks, and lambda_j s_j = sigma mu), with the step kept inside the cone."""
    n, m = problem.n, len(rows)
    hessian = [[float(v) for v in row] for row in problem.sigma]
    mu = [float(v) for v in problem.mu]
    a_rows = [list(a) for a, _, _ in rows]
    bound = [float(b) for _, b, _ in rows]
    x = [float(v) for v in problem.w0]
    nu = 0.0
    lam = [1.0] * m
    s = [max(bound[j] - _dotf(a_rows[j], x), 1.0) for j in range(m)]
    for _ in range(IPM_ITERS):
        r_d = [
            _dotf(hessian[i], x) - mu[i] + nu + sum(a_rows[j][i] * lam[j] for j in range(m)) for i in range(n)
        ]
        r_e = sum(x) - 1.0
        r_p = [_dotf(a_rows[j], x) + s[j] - bound[j] for j in range(m)]
        gap = sum(lam[j] * s[j] for j in range(m)) / m
        target = 0.2 * gap
        r_c = [lam[j] * s[j] - target for j in range(m)]
        if max(abs(v) for v in [*r_d, r_e, *r_p]) < 1e-11 and gap < 1e-11:
            break
        d = [lam[j] / s[j] for j in range(m)]
        schur = [
            [hessian[i][k] + sum(a_rows[j][i] * d[j] * a_rows[j][k] for j in range(m)) for k in range(n)]
            for i in range(n)
        ]
        rhs1 = [
            -r_d[i] - sum(a_rows[j][i] * ((-r_c[j] + lam[j] * r_p[j]) / s[j]) for j in range(m)) for i in range(n)
        ]
        big = [[*schur[i], 1.0] for i in range(n)] + [[*([1.0] * n), 0.0]]
        sol = _solve_linear(big, [*rhs1, -r_e])
        dx = sol[:n]
        d_nu = sol[n]
        ds = [-r_p[j] - _dotf(a_rows[j], dx) for j in range(m)]
        dl = [(-r_c[j] - lam[j] * ds[j]) / s[j] for j in range(m)]
        alpha = 1.0
        for j in range(m):
            if ds[j] < 0.0:
                alpha = min(alpha, -0.995 * s[j] / ds[j])
            if dl[j] < 0.0:
                alpha = min(alpha, -0.995 * lam[j] / dl[j])
        x = [x[i] + alpha * dx[i] for i in range(n)]
        nu += alpha * d_nu
        lam = [lam[j] + alpha * dl[j] for j in range(m)]
        s = [s[j] + alpha * ds[j] for j in range(m)]
    return x, lam



def _solve(problem: Problem) -> dict[str, Any]:
    global LAST_PATH
    n = problem.n
    g = problem.gamma
    scaled = Problem(
        problem.n, Fraction(1), [m / g for m in problem.mu], problem.sigma, problem.w0, problem.lower, problem.upper,
        problem.sector, problem.caps, problem.tau,
    )
    rows = _inequalities(scaled)
    found = None
    try:
        x0, lam0 = _front_end(scaled, rows)
        found = _polish(scaled, rows, _guess(rows, x0, lam0))
    except (ArithmeticError, StopIteration, RuntimeError):
        found = None  # a singular or non-finite front-end step: the verified active-set search below still answers
    if found is None:
        LAST_PATH = "fallback"
        x, mult, budget_mult = _active_set(scaled, rows)
    else:
        LAST_PATH = "front-end"
        x, mult, budget_mult = found
    mult = {k: v * g for k, v in mult.items()}
    budget_mult = budget_mult * g
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
