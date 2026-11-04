"""Alternative 5: float active set, start with no working constraints, cutoffs 1e-13, drop the latest-added negative."""

from __future__ import annotations

import math
from fractions import Fraction
from itertools import product
from typing import Any

EXACT = False
TOL_SLACK = 1e-13  # slack at or below this counts as active when the search starts
TOL_MULT = 1e-13  # a multiplier below minus this is negative; between minus and zero is treated as zero
ZERO = 1e-13  # a step or pivot at or below this in size is zero
START = "empty"  # "tight": start with the constraints active at w0; "empty": start with none
DROP = "last_added"  # "most_negative" drops the most negative multiplier; "last_added" drops the latest-added negative
TOL_START = 1e-9  # the starting-portfolio tolerance the page states


def _num(value: object, name: str) -> Any:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number, not {type(value).__name__}")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    if EXACT:
        return Fraction(repr(value)) if isinstance(value, float) else Fraction(value)
    return float(value)


def _vec(value: object, name: str) -> list[Any]:
    if not isinstance(value, (list, tuple)):
        raise TypeError(f"{name} must be a list")
    return [_num(v, f"{name}[{i}]") for i, v in enumerate(value)]


def _parse(instance: object) -> dict[str, Any]:
    if not isinstance(instance, dict):
        raise ValueError("the instance must be a mapping with the case fields")
    for key in ("gamma", "mu", "sigma", "w0", "lower", "upper", "sector", "sector_caps", "turnover_limit"):
        if key not in instance:
            raise ValueError(f"the instance has no field {key}")
    mu = _vec(instance["mu"], "mu")
    n = len(mu)
    if n == 0:
        raise ValueError("the instance has no assets")
    gamma = _num(instance["gamma"], "gamma")
    if not gamma > 0:
        raise ValueError("gamma must be positive")
    tau = _num(instance["turnover_limit"], "turnover_limit")
    if tau < 0:
        raise ValueError("the turnover limit must not be negative")
    rows = instance["sigma"]
    if not isinstance(rows, (list, tuple)) or len(rows) != n:
        raise ValueError("sigma must have one row per asset")
    sigma = [_vec(r, f"sigma[{i}]") for i, r in enumerate(rows)]
    if any(len(r) != n for r in sigma):
        raise ValueError("sigma must be square")
    if any(sigma[i][j] != sigma[j][i] for i in range(n) for j in range(n)):
        raise ValueError("sigma must be symmetric")
    # positive definiteness by Cholesky-style pivots
    a = [r[:] for r in sigma]
    for k in range(n):
        if not a[k][k] > 0:
            raise ValueError("sigma must be positive definite")
        for i in range(k + 1, n):
            f = a[i][k] / a[k][k]
            for j in range(k + 1, n):
                a[i][j] -= f * a[k][j]
    w0 = _vec(instance["w0"], "w0")
    lower = _vec(instance["lower"], "lower")
    upper = _vec(instance["upper"], "upper")
    if not (len(w0) == len(lower) == len(upper) == n):
        raise ValueError("w0, lower and upper must have one entry per asset")
    if any(lower[i] > upper[i] for i in range(n)):
        raise ValueError("lower bound above upper bound")
    caps = _vec(instance["sector_caps"], "sector_caps")
    if not caps:
        raise ValueError("no sector caps")
    raw = instance["sector"]
    if not isinstance(raw, (list, tuple)) or len(raw) != n:
        raise ValueError("sector must have one label per asset")
    sector: list[int] = []
    for lab in raw:
        if isinstance(lab, bool) or not isinstance(lab, int):
            raise TypeError("sector labels must be integers")
        if not 0 <= lab < len(caps):
            raise ValueError("sector label out of range")
        sector.append(lab)
    for k in range(len(caps)):
        if k not in sector:
            raise ValueError("a sector cap belongs to no asset")
    if abs(sum(w0) - 1) > TOL_START:
        raise ValueError("the starting portfolio does not sum to one")
    if any(w0[i] < lower[i] - TOL_START or w0[i] > upper[i] + TOL_START for i in range(n)):
        raise ValueError("the starting portfolio lies outside a bound")
    for k in range(len(caps)):
        if sum(w0[i] for i in range(n) if sector[i] == k) > caps[k] + TOL_START:
            raise ValueError("the starting portfolio breaks a sector cap")
    return {"n": n, "gamma": gamma, "mu": mu, "sigma": sigma, "w0": w0, "lower": lower, "upper": upper,
            "sector": sector, "caps": caps, "tau": tau}


def _rows(p: dict[str, Any]) -> list[tuple[list[Any], Any, tuple[Any, ...]]]:
    n = p["n"]
    out: list[tuple[list[Any], Any, tuple[Any, ...]]] = []
    zero = Fraction(0) if EXACT else 0.0
    one = Fraction(1) if EXACT else 1.0
    for i in range(n):
        out.append(([-one if j == i else zero for j in range(n)], -p["lower"][i], ("lower", i)))
        out.append(([one if j == i else zero for j in range(n)], p["upper"][i], ("upper", i)))
    for k, cap in enumerate(p["caps"]):
        out.append(([one if p["sector"][j] == k else zero for j in range(n)], cap, ("sector", k)))
    for signs in product((1, -1), repeat=n):
        a = [one * s for s in signs]
        out.append((a, p["tau"] + sum(a[i] * p["w0"][i] for i in range(n)), ("turn", signs)))
    return out


def _is_zero(v: Any) -> bool:
    return v == 0 if EXACT else abs(v) <= ZERO


def _solve_kkt(h: list[list[Any]], g: list[Any], act: list[list[Any]]) -> tuple[list[Any], list[Any]]:
    n, m = len(g), len(act)
    size = n + m
    zero = Fraction(0) if EXACT else 0.0
    mat = [[zero] * (size + 1) for _ in range(size)]
    for i in range(n):
        for j in range(n):
            mat[i][j] = h[i][j]
        mat[i][size] = -g[i]
    for k, a in enumerate(act):
        for i in range(n):
            mat[i][n + k] = a[i]
            mat[n + k][i] = a[i]
    # Gauss-Jordan with largest-magnitude pivot in each column
    for col in range(size):
        piv = max(range(col, size), key=lambda r: abs(mat[r][col]))
        if _is_zero(mat[piv][col]):
            raise RuntimeError("singular KKT system")
        mat[col], mat[piv] = mat[piv], mat[col]
        for r in range(size):
            if r != col and not _is_zero(mat[r][col]):
                f = mat[r][col] / mat[col][col]
                mat[r] = [x - f * y for x, y in zip(mat[r], mat[col])]
    sol = [mat[i][size] / mat[i][i] for i in range(size)]
    return sol[:n], sol[n:]


def _dot(a: list[Any], b: list[Any]) -> Any:
    return sum((x * y for x, y in zip(a, b)), Fraction(0) if EXACT else 0.0)


def _rank(vectors: list[list[Any]]) -> int:
    rows_ = [v[:] for v in vectors]
    rank = 0
    width = len(rows_[0]) if rows_ else 0
    for col in range(width):
        piv = max(range(rank, len(rows_)), key=lambda r: abs(rows_[r][col]), default=None)
        if piv is None or _is_zero(rows_[piv][col]):
            continue
        rows_[rank], rows_[piv] = rows_[piv], rows_[rank]
        for r in range(len(rows_)):
            if r != rank and not _is_zero(rows_[r][col]):
                f = rows_[r][col] / rows_[rank][col]
                rows_[r] = [x - f * y for x, y in zip(rows_[r], rows_[rank])]
        rank += 1
    return rank


def _solve(p: dict[str, Any]) -> dict[str, Any]:
    n = p["n"]
    rows = _rows(p)
    zero = Fraction(0) if EXACT else 0.0
    one = Fraction(1) if EXACT else 1.0
    h = [[p["gamma"] * p["sigma"][i][j] for j in range(n)] for i in range(n)]
    budget = [one] * n
    x = list(p["w0"])
    working: list[int] = []
    if START == "tight":
        for j, (a, b, _) in enumerate(rows):
            slack = b - _dot(a, x)
            if slack <= TOL_SLACK and _rank([budget] + [rows[k][0] for k in working] + [a]) > len(working) + 1:
                working.append(j)
    for _ in range(2000):
        grad = [_dot(h[i], x) - p["mu"][i] for i in range(n)]
        pstep, lam = _solve_kkt(h, grad, [budget] + [rows[j][0] for j in working])
        if all(_is_zero(v) for v in pstep):
            neg = [k for k in range(len(working)) if lam[1 + k] < -(TOL_MULT if not EXACT else 0)]
            if not neg:
                mult = {rows[j][2]: (zero if _is_zero(lam[1 + k]) else lam[1 + k]) for k, j in enumerate(working)}
                return {"x": x, "mult": mult, "budget": lam[0], "rows": rows}
            k = min(neg, key=lambda kk: lam[1 + kk]) if DROP == "most_negative" else max(neg)
            working.pop(k)
            continue
        step = one
        blocking = None
        for j, (a, b, _) in enumerate(rows):
            if j in working:
                continue
            rate = _dot(a, pstep)
            if rate > (0 if EXACT else ZERO):
                ratio = max(b - _dot(a, x), zero) / rate
                if ratio < step:
                    step, blocking = ratio, j
        x = [xi + step * pi for xi, pi in zip(x, pstep)]
        if blocking is not None:
            working.append(blocking)
    raise RuntimeError("no convergence")


def allocate(instance: dict[str, Any]) -> dict[str, Any]:
    p = _parse(instance)
    n = p["n"]
    res = _solve(p)
    x, mult, nu, rows = res["x"], res["mult"], res["budget"], res["rows"]
    zero = Fraction(0) if EXACT else 0.0
    lower = [mult.get(("lower", i), zero) for i in range(n)]
    upper = [mult.get(("upper", i), zero) for i in range(n)]
    sector = [mult.get(("sector", k), zero) for k in range(len(p["caps"]))]
    signs = {key[1]: v for key, v in mult.items() if key[0] == "turn"}
    kappa = sum(signs.values(), zero)
    plus = [(kappa + sum((eta * s[i] for s, eta in signs.items()), zero)) / 2 for i in range(n)]
    minus = [(kappa - sum((eta * s[i] for s, eta in signs.items()), zero)) / 2 for i in range(n)]
    d = [x[i] - p["w0"][i] for i in range(n)]
    t = [abs(v) for v in d]
    sec_sum = [sum((x[i] for i in range(n) if p["sector"][i] == k), zero) for k in range(len(p["caps"]))]
    gaps = [p["lower"][i] - x[i] for i in range(n)] + [x[i] - p["upper"][i] for i in range(n)]
    gaps += [sec_sum[k] - p["caps"][k] for k in range(len(p["caps"]))]
    gaps += [sum(t, zero) - p["tau"]]
    primal = max([zero, abs(sum(x, zero) - 1), *gaps])
    ineq = [*lower, *upper, *sector, *plus, *minus, kappa]
    dual = max(zero, -min(ineq))
    comp = max(
        abs(m * g)
        for m, g in zip(
            ineq,
            [*gaps[:n], *gaps[n : 2 * n], *[sec_sum[k] - p["caps"][k] for k in range(len(p["caps"]))],
             *[d[i] - t[i] for i in range(n)], *[-d[i] - t[i] for i in range(n)], sum(t, zero) - p["tau"]],
        )
    )
    stat = zero
    for i in range(n):
        grad = p["gamma"] * sum((p["sigma"][i][j] * x[j] for j in range(n)), zero) - p["mu"][i]
        rw = grad + nu - lower[i] + upper[i] + sector[p["sector"][i]] + plus[i] - minus[i]
        rt = kappa - plus[i] - minus[i]
        stat = max(stat, abs(rw), abs(rt))
    return {
        "weights": [float(v) for v in x],
        "multipliers": {
            "budget": float(nu),
            "lower": [float(v) for v in lower],
            "upper": [float(v) for v in upper],
            "sector": [float(v) for v in sector],
            "turnover_plus": [float(v) for v in plus],
            "turnover_minus": [float(v) for v in minus],
            "turnover_total": float(kappa),
        },
        "certificate": {
            "primal_residual": float(primal),
            "stationarity_residual": float(stat),
            "dual_residual": float(dual),
            "complementary_slackness": float(comp),
        },
    }
