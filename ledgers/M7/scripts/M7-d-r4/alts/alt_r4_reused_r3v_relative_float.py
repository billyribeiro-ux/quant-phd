"""Verifier round-3 alternative A6: a float active-set method, written independently of grader/reference.py.

The working set is built from the rows that are active at the starting portfolio, and each row is added only when its
gradient is independent of the working set (relative rank test with cutoff 1e-10). The step is the largest step to the
first blocking row whose rate exceeds 1e-12 (a row whose rate is below that is treated as parallel to the step). A
negative multiplier drops the most recently added row among those with negative multipliers (last in, first out). The
KKT systems are solved by Gaussian elimination with partial pivoting in float arithmetic. The turnover limit enters as
the 2**n sign forms, and the multipliers are mapped back to the linearized form with alpha = (kappa + net) / 2 and
beta = (kappa - net) / 2. Every certificate field is computed from the page's definitions in float arithmetic.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from itertools import product
from typing import Any

FIELDS = ("gamma", "mu", "sigma", "w0", "lower", "upper", "sector", "sector_caps", "turnover_limit")
TOL = 1e-9


def _num(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number, not {type(value).__name__}")
    out = float(value)
    if not math.isfinite(out):
        raise ValueError(f"{name} must be finite")
    return out


def _vec(value: object, name: str) -> list[float]:
    if not isinstance(value, (list, tuple)):
        raise TypeError(f"{name} must be a list of numbers")
    return [_num(v, f"{name}[{i}]") for i, v in enumerate(value)]


def _pd(a: list[list[float]]) -> bool:
    scale = max(abs(v) for row in a for v in row)
    m = [row[:] for row in a]
    n = len(m)
    for k in range(n):
        piv = m[k][k]
        if piv <= 1e-12 * scale:
            return False
        for i in range(k + 1, n):
            f = m[i][k] / piv
            for j in range(k + 1, n):
                m[i][j] -= f * m[k][j]
    return True


def _dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))


def _solve(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    n = len(rhs)
    aug = [matrix[i][:] + [rhs[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(aug[r][c]))
        aug[c], aug[p] = aug[p], aug[c]
        if abs(aug[c][c]) < 1e-30:
            raise RuntimeError("singular KKT system")
        for r in range(n):
            if r != c and aug[r][c] != 0.0:
                f = aug[r][c] / aug[c][c]
                aug[r] = [x - f * y for x, y in zip(aug[r], aug[c], strict=True)]
    return [aug[i][n] / aug[i][i] for i in range(n)]


def _rank(rows: list[list[float]], width: int) -> int:
    a = [r[:] for r in rows]
    rank = 0
    for c in range(width):
        if rank == len(a):
            break
        p = max(range(rank, len(a)), key=lambda r: abs(a[r][c]))
        if abs(a[p][c]) <= 1e-10:
            continue
        a[rank], a[p] = a[p], a[rank]
        for r in range(len(a)):
            if r != rank:
                f = a[r][c] / a[rank][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[rank], strict=True)]
        rank += 1
    return rank


def _parse(instance: object) -> dict[str, Any]:
    if not isinstance(instance, Mapping):
        raise ValueError("the instance must be a mapping with the case fields")
    for key in FIELDS:
        if key not in instance:
            raise ValueError(f"the instance has no {key!r} field")
    mu = _vec(instance["mu"], "mu")
    n = len(mu)
    if n == 0:
        raise ValueError("the instance has no assets")
    gamma = _num(instance["gamma"], "gamma")
    if gamma <= 0:
        raise ValueError("gamma must be positive")
    tau = _num(instance["turnover_limit"], "turnover_limit")
    if tau < 0:
        raise ValueError("the turnover limit must not be negative")
    raw = instance["sigma"]
    if not isinstance(raw, (list, tuple)) or len(raw) != n:
        raise ValueError("sigma must have one row per asset")
    sigma = [_vec(row, f"sigma[{i}]") for i, row in enumerate(raw)]
    if any(len(row) != n for row in sigma):
        raise ValueError("sigma must be square, one column per asset")
    if any(sigma[i][j] != sigma[j][i] for i in range(n) for j in range(n)):
        raise ValueError("sigma must be symmetric")
    if not _pd(sigma):
        raise ValueError("sigma must be positive definite")
    w0 = _vec(instance["w0"], "w0")
    lower = _vec(instance["lower"], "lower")
    upper = _vec(instance["upper"], "upper")
    if len(w0) != n or len(lower) != n or len(upper) != n:
        raise ValueError("w0, lower and upper must have one entry per asset")
    if any(lower[i] > upper[i] for i in range(n)):
        raise ValueError("a lower bound lies above its upper bound")
    caps = _vec(instance["sector_caps"], "sector_caps")
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
    if any(k not in sector for k in range(len(caps))):
        raise ValueError("every sector cap must belong to at least one asset")
    if abs(sum(w0) - 1.0) > TOL:
        raise ValueError("the starting portfolio must sum to one")
    if any(w0[i] < lower[i] - TOL or w0[i] > upper[i] + TOL for i in range(n)):
        raise ValueError("the starting portfolio lies outside a box bound")
    for k, cap in enumerate(caps):
        if sum(w0[i] for i in range(n) if sector[i] == k) > cap + TOL:
            raise ValueError("the starting portfolio breaks a sector cap")
    return {"n": n, "gamma": gamma, "mu": mu, "sigma": sigma, "w0": w0, "lower": lower, "upper": upper,
            "sector": sector, "caps": caps, "tau": tau}


def _qp(p: dict[str, Any]) -> tuple[list[float], dict[tuple[object, ...], float], float]:
    n = p["n"]
    hess = [[p["gamma"] * p["sigma"][i][j] for j in range(n)] for i in range(n)]
    rows: list[tuple[list[float], float, tuple[object, ...]]] = []
    for i in range(n):
        rows.append(([-1.0 if j == i else 0.0 for j in range(n)], -p["lower"][i], ("lower", i)))
    for i in range(n):
        rows.append(([1.0 if j == i else 0.0 for j in range(n)], p["upper"][i], ("upper", i)))
    for k, cap in enumerate(p["caps"]):
        rows.append(([1.0 if p["sector"][j] == k else 0.0 for j in range(n)], cap, ("sector", k)))
    for signs in product((1.0, -1.0), repeat=n):
        rows.append((list(signs), p["tau"] + _dot(signs, p["w0"]), ("turn", signs)))
    budget = [1.0] * n
    x = list(p["w0"])
    working: list[int] = []
    for j, (a, b, _) in enumerate(rows):
        if b - _dot(a, x) <= 1e-9 and _rank([budget] + [rows[k][0] for k in working] + [a], n) == len(working) + 2:
            working.append(j)
    for _ in range(500):
        grad = [_dot(hess[i], x) - p["mu"][i] for i in range(n)]
        m = len(working) + 1
        size = n + m
        kkt = [[0.0] * size for _ in range(size)]
        for i in range(n):
            for j in range(n):
                kkt[i][j] = hess[i][j]
        for col, a in enumerate([budget] + [rows[k][0] for k in working]):
            for i in range(n):
                kkt[i][n + col] = a[i]
                kkt[n + col][i] = a[i]
        rhs = [-g for g in grad] + [0.0] * m
        sol = _solve(kkt, rhs)
        for _pass in range(4):  # iterative refinement of the KKT solve
            resid = [rhs[r] - sum(kkt[r][c] * sol[c] for c in range(size)) for r in range(size)]
            corr = _solve(kkt, resid)
            sol = [s + c for s, c in zip(sol, corr, strict=True)]
        step_dir, lam = sol[:n], sol[n:]
        if max(abs(v) for v in step_dir) <= 1e-12:
            neg = [k for k in range(len(working)) if lam[1 + k] < -1e-12]
            if not neg:
                mult = {rows[j][2]: lam[1 + k] for k, j in enumerate(working)}
                return x, mult, lam[0]
            working.pop(max(neg))  # last in, first out among the negative multipliers
            continue
        step = 1.0
        block: int | None = None
        norm_p = math.sqrt(_dot(step_dir, step_dir))
        for j, (a, b, _) in enumerate(rows):
            if j in working:
                continue
            rate = _dot(a, step_dir)
            if rate > 1e-10 * math.sqrt(_dot(a, a)) * norm_p:
                ratio = max(b - _dot(a, x), 0.0) / rate
                if ratio < step:
                    step, block = ratio, j
        x = [xi + step * pi for xi, pi in zip(x, step_dir, strict=True)]
        if block is not None:
            working.append(block)
    raise RuntimeError("no convergence in the float active-set search")


def allocate(instance: dict[str, Any]) -> dict[str, Any]:
    p = _parse(instance)
    n = p["n"]
    x, mult, nu = _qp(p)
    lower = [mult.get(("lower", i), 0.0) for i in range(n)]
    upper = [mult.get(("upper", i), 0.0) for i in range(n)]
    sector = [mult.get(("sector", k), 0.0) for k in range(len(p["caps"]))]
    signs_mult = {key[1]: value for key, value in mult.items() if key[0] == "turn"}
    kappa = sum(signs_mult.values())
    plus = [0.0] * n
    minus = [0.0] * n
    for i in range(n):
        net = sum(eta * s[i] for s, eta in signs_mult.items())
        plus[i] = (kappa + net) / 2.0
        minus[i] = (kappa - net) / 2.0
    w0 = p["w0"]
    d = [x[i] - w0[i] for i in range(n)]
    t = [abs(v) for v in d]
    sums = [sum(x[i] for i in range(n) if p["sector"][i] == k) for k in range(len(p["caps"]))]
    gaps = []
    for i in range(n):
        gaps += [p["lower"][i] - x[i], x[i] - p["upper"][i], d[i] - t[i], -d[i] - t[i]]
    gaps += [sums[k] - p["caps"][k] for k in range(len(p["caps"]))]
    gaps.append(sum(t) - p["tau"])
    primal = max([0.0, abs(sum(x) - 1.0), *gaps])
    ineq_mult = [*lower, *upper, *sector, *plus, *minus, kappa]
    dual = max(0.0, -min(ineq_mult))
    ineq_gap = [
        *[p["lower"][i] - x[i] for i in range(n)],
        *[x[i] - p["upper"][i] for i in range(n)],
        *[sums[k] - p["caps"][k] for k in range(len(p["caps"]))],
        *[d[i] - t[i] for i in range(n)],
        *[-d[i] - t[i] for i in range(n)],
        sum(t) - p["tau"],
    ]
    comp = max(abs(m * g) for m, g in zip(ineq_mult, ineq_gap, strict=True))
    stat = 0.0
    for i in range(n):
        grad = p["gamma"] * _dot(p["sigma"][i], x) - p["mu"][i]
        r_w = grad + nu - lower[i] + upper[i] + sector[p["sector"][i]] + plus[i] - minus[i]
        r_t = kappa - plus[i] - minus[i]
        stat = max(stat, abs(r_w), abs(r_t))
    return {
        "weights": x,
        "multipliers": {
            "budget": nu,
            "lower": lower,
            "upper": upper,
            "sector": sector,
            "turnover_plus": plus,
            "turnover_minus": minus,
            "turnover_total": kappa,
        },
        "certificate": {
            "primal_residual": primal,
            "stationarity_residual": stat,
            "dual_residual": dual,
            "complementary_slackness": comp,
        },
    }
