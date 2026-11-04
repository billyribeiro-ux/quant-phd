"""Round-8 generic alternative solver for the M7 allocator (verifier-written). Config constants are set per variant file.

"absolute" (1e-12 everywhere). SCALE_BY_GAMMA: solve with Sigma and -g/gamma, then multiply the multipliers by gamma.
DROP: which negative working multiplier leaves the set ("most_negative" or "first_negative"). TIE: which blocking row
wins a tie of step ratios ("first" or "last"). Validation is the spec's, copied from the reference (instance checks).
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from fractions import Fraction
from itertools import product
from typing import Any

CUT = "relative"
SCALE_BY_GAMMA = True
DROP = "first_negative"
TIE = "last"
REQUIRED = ("gamma", "mu", "sigma", "w0", "lower", "upper", "sector", "sector_caps", "turnover_limit")
TOL = 1e-9


class _Singular(Exception):
    pass


def _num(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number, not {type(value).__name__}")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return float(Fraction(repr(value))) if isinstance(value, float) else float(value)


def _vec(value: object, name: str) -> list[float]:
    if not isinstance(value, (list, tuple)):
        raise TypeError(f"{name} must be a list of numbers")
    return [_num(v, f"{name}[{i}]") for i, v in enumerate(value)]


def _check(instance: object) -> dict[str, Any]:
    if not isinstance(instance, Mapping):
        raise ValueError("the instance must be a mapping with the case fields")
    for key in REQUIRED:
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
    sigma = [_vec(r, f"sigma[{i}]") for i, r in enumerate(raw)]
    if any(len(r) != n for r in sigma):
        raise ValueError("sigma must be square, one column per asset")
    for i in range(n):
        for j in range(n):
            if Fraction(repr(sigma[i][j])) != Fraction(repr(sigma[j][i])):
                raise ValueError("sigma must be symmetric")
    # exact positive-definiteness check on the decimal values
    ex = [[Fraction(repr(x)) for x in r] for r in sigma]
    for k in range(n):
        if ex[k][k] <= 0:
            raise ValueError("sigma must be positive definite")
        for i in range(k + 1, n):
            f = ex[i][k] / ex[k][k]
            for j in range(k + 1, n):
                ex[i][j] -= f * ex[k][j]
    if any(ex[k][k] <= 0 for k in range(n)):
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
    raw_s = instance["sector"]
    if not isinstance(raw_s, (list, tuple)) or len(raw_s) != n:
        raise ValueError("sector must give one label per asset")
    sector: list[int] = []
    for lab in raw_s:
        if isinstance(lab, bool) or not isinstance(lab, int):
            raise TypeError("a sector label must be an integer")
        if not 0 <= lab < len(caps):
            raise ValueError("a sector label lies outside 0 to the number of caps minus one")
        sector.append(lab)
    if any(k not in sector for k in range(len(caps))):
        raise ValueError("every sector cap must belong to at least one asset")
    if abs(sum(Fraction(repr(x)) for x in w0) - 1) > Fraction(1, 10**9):
        raise ValueError("the starting portfolio must sum to one")
    tol = Fraction(1, 10**9)
    if any(Fraction(repr(w0[i])) < Fraction(repr(lower[i])) - tol or Fraction(repr(w0[i])) > Fraction(repr(upper[i])) + tol for i in range(n)):
        raise ValueError("the starting portfolio lies outside a box bound")
    for k, c in enumerate(caps):
        if sum(Fraction(repr(w0[i])) for i in range(n) if sector[i] == k) > Fraction(repr(c)) + tol:
            raise ValueError("the starting portfolio breaks a sector cap")
    return {"n": n, "gamma": gamma, "mu": mu, "sigma": sigma, "w0": w0, "lower": lower, "upper": upper,
            "sector": sector, "caps": caps, "tau": tau}


def _cut(scale: float) -> float:
    if CUT == "absolute":
        return 1e-12
    return 1e-13 * max(scale, 1e-300)


def _solve_lin(mat: list[list[float]], rhs: list[float], cut: float) -> list[float]:
    size = len(rhs)
    rows = [mat[i][:] + [rhs[i]] for i in range(size)]
    for c in range(size):
        p = max(range(c, size), key=lambda r: abs(rows[r][c]))
        if abs(rows[p][c]) <= cut:
            raise _Singular()
        rows[c], rows[p] = rows[p], rows[c]
        for r in range(size):
            if r != c and rows[r][c] != 0.0:
                f = rows[r][c] / rows[c][c]
                rows[r] = [x - f * y for x, y in zip(rows[r], rows[c])]
    return [rows[i][size] / rows[i][i] for i in range(size)]


def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _rows(p: dict[str, Any]) -> list[tuple[list[float], float, tuple[object, ...]]]:
    n = p["n"]
    out: list[tuple[list[float], float, tuple[object, ...]]] = []
    for i in range(n):
        out.append(([-1.0 if j == i else 0.0 for j in range(n)], -p["lower"][i], ("lower", i)))
        out.append(([1.0 if j == i else 0.0 for j in range(n)], p["upper"][i], ("upper", i)))
    for k, c in enumerate(p["caps"]):
        out.append(([1.0 if p["sector"][j] == k else 0.0 for j in range(n)], c, ("sector", k)))
    for s in product((1, -1), repeat=n):
        a = [float(x) for x in s]
        out.append((a, p["tau"] + _dot(a, p["w0"]), ("turn", s)))
    return out


def _search(p: dict[str, Any]) -> tuple[list[float], dict[object, float], float]:
    n = p["n"]
    H = [[p["gamma"] * p["sigma"][i][j] for j in range(n)] for i in range(n)]
    budget = [1.0] * n
    rows = _rows(p)
    x = list(p["w0"])
    scale_h = max(abs(v) for r in H for v in r)
    cutm = 1e-12  # step-rate and blocking cutoff: constraint rows have entries of order one, whatever gamma is
    work: list[int] = []
    for j, (a, b, _) in enumerate(rows):
        if b - _dot(a, x) <= 1e-9 and len(work) < n - 1:
            trial = [budget] + [rows[k][0] for k in work] + [a]
            if _rank(trial) > len(work) + 1:
                work.append(j)
    for _ in range(400):
        g = [_dot(H[i], x) - p["mu"][i] for i in range(n)]
        if SCALE_BY_GAMMA:
            Hs = [[p["sigma"][i][j] for j in range(n)] for i in range(n)]
            gs = [v / p["gamma"] for v in g]
        else:
            Hs, gs = H, g
        act = [budget] + [rows[j][0] for j in work]
        m = len(act)
        size = n + m
        mat = [[0.0] * size for _ in range(size)]
        for i in range(n):
            for j in range(n):
                mat[i][j] = Hs[i][j]
        for k, a in enumerate(act):
            for i in range(n):
                mat[i][n + k] = a[i]
                mat[n + k][i] = a[i]
        cut_k = _cut(max(abs(v) for r in mat for v in r))
        sol = _solve_lin(mat, [-v for v in gs] + [0.0] * m, cut_k)
        pvec, lam = sol[:n], sol[n:]
        if SCALE_BY_GAMMA:
            lam = [v * p["gamma"] for v in lam]
        if max(abs(v) for v in pvec) <= max(cutm, 1e-12) * max(1.0, max(abs(v) for v in x)):
            neg = [(lam[1 + k], k) for k in range(len(work)) if lam[1 + k] < -1e-12]
            if not neg:
                mult = {rows[j][2]: lam[1 + k] for k, j in enumerate(work)}
                return _polish(x, [(budget, 1.0)] + [(rows[j][0], rows[j][1]) for j in work]), mult, lam[0]
            if DROP == "most_negative":
                work.pop(min(neg)[1])
            else:
                work.pop(neg[0][1])
            continue
        step, block = 1.0, None
        cands = []
        for j, (a, b, _) in enumerate(rows):
            if j in work:
                continue
            rate = _dot(a, pvec)
            if rate > (1e-12 * max(1.0, max(abs(v) for v in pvec)) if CUT == "relative" else cutm):
                cands.append((max(b - _dot(a, x), 0.0) / rate, j))
        for ratio, j in cands:
            if ratio < step or (TIE == "last" and ratio == step and block is not None):
                step, block = ratio, j
        x = [xi + step * pi for xi, pi in zip(x, pvec)]
        if block is not None and _rank([budget] + [rows[k][0] for k in work] + [rows[block][0]]) > len(work) + 1:
            work.append(block)
    raise RuntimeError("no convergence")


def _polish(x: list[float], active: list[tuple[list[float], float]]) -> list[float]:
    """Minimum-norm correction of x onto the active equalities a.x = b (budget and the working rows)."""
    n = len(x)
    gram = [[_dot(a, c) for c, _ in active] for a, _ in active]
    resid = [b - _dot(a, x) for a, b in active]
    y = _solve_lin(gram, resid, 1e-300)
    return [x[i] + sum(a[i] * yk for (a, _), yk in zip(active, y)) for i in range(n)]


def _rank(vecs: list[list[float]]) -> int:
    m = [v[:] for v in vecs]
    r = 0
    for c in range(len(m[0]) if m else 0):
        piv = next((i for i in range(r, len(m)) if abs(m[i][c]) > 1e-12), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r and m[i][c] != 0.0:
                f = m[i][c] / m[r][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[r])]
        r += 1
    return r


def allocate(instance: dict[str, Any]) -> dict[str, Any]:
    p = _check(instance)
    n = p["n"]
    x, mult, budget = _search(p)
    lower = [float(mult.get(("lower", i), 0.0)) for i in range(n)]
    upper = [float(mult.get(("upper", i), 0.0)) for i in range(n)]
    sector = [float(mult.get(("sector", k), 0.0)) for k in range(len(p["caps"]))]
    signs = {key[1]: float(v) for key, v in mult.items() if key[0] == "turn"}
    kappa = sum(signs.values())
    plus = [0.0] * n
    minus = [0.0] * n
    for i in range(n):
        net = sum(eta * s[i] for s, eta in signs.items())
        plus[i] = (kappa + net) / 2
        minus[i] = (kappa - net) / 2
    w = x
    d = [w[i] - p["w0"][i] for i in range(n)]
    t = [abs(v) for v in d]
    ssum = [sum(w[i] for i in range(n) if p["sector"][i] == k) for k in range(len(p["caps"]))]
    gaps = []
    for i in range(n):
        gaps += [p["lower"][i] - w[i], w[i] - p["upper"][i], d[i] - t[i], -d[i] - t[i]]
    gaps += [ssum[k] - p["caps"][k] for k in range(len(p["caps"]))] + [sum(t) - p["tau"]]
    primal = max([0.0, abs(sum(w) - 1.0)] + gaps)
    ineq = lower + upper + sector + plus + minus + [kappa]
    dual = max(0.0, -min(ineq))
    gvals = ([p["lower"][i] - w[i] for i in range(n)] + [w[i] - p["upper"][i] for i in range(n)]
             + [ssum[k] - p["caps"][k] for k in range(len(p["caps"]))] + [d[i] - t[i] for i in range(n)]
             + [-d[i] - t[i] for i in range(n)] + [sum(t) - p["tau"]])
    comp = max(abs(m * g) for m, g in zip(ineq, gvals))
    stat = 0.0
    for i in range(n):
        grad = p["gamma"] * _dot(p["sigma"][i], w) - p["mu"][i]
        rw = grad + budget - lower[i] + upper[i] + sector[p["sector"][i]] + plus[i] - minus[i]
        rt = kappa - plus[i] - minus[i]
        stat = max(stat, abs(rw), abs(rt))
    return {
        "weights": [float(v) for v in w],
        "multipliers": {"budget": float(budget), "lower": lower, "upper": upper, "sector": sector,
                        "turnover_plus": plus, "turnover_minus": minus, "turnover_total": float(kappa)},
        "certificate": {"primal_residual": primal, "stationarity_residual": stat,
                        "dual_residual": dual, "complementary_slackness": comp},
    }
