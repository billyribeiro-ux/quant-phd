"""Reference solution for the M7 constrained allocator (constrained_allocator.py): an exact active-set solver.

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
from itertools import product
import math


# ---------------------------------------------------------------------------------------------------------------------
# Independent solver (verifier alternative). Configurable: numeric type, variable space, drop rule, pre-pass.
# ---------------------------------------------------------------------------------------------------------------------

class _Cfg:
    def __init__(self, space, exact, drop, prepass, eps):
        self.space, self.exact, self.drop, self.prepass, self.eps = space, exact, drop, prepass, eps


def _num(cfg, x):
    return Fraction(x) if cfg.exact else float(x)


def _zero(cfg):
    return Fraction(0) if cfg.exact else 0.0


def _gauss(cfg, M, rhs):
    size = len(rhs)
    A = [list(M[i]) + [rhs[i]] for i in range(size)]
    scale = max([abs(x) for row in M for x in row] + [1e-300])  # relative pivot cutoff (other cutoff than reference)
    for col in range(size):
        if cfg.exact:
            piv = next((r for r in range(col, size) if A[r][col] != 0), None)
        else:
            piv = max(range(col, size), key=lambda r: abs(A[r][col]))
            if abs(A[piv][col]) <= cfg.eps * scale:
                piv = None
        if piv is None:
            raise RuntimeError("singular KKT system")
        A[col], A[piv] = A[piv], A[col]
        for r in range(size):
            if r != col and A[r][col] != 0:
                f = A[r][col] / A[col][col]
                A[r] = [x - f * y for x, y in zip(A[r], A[col])]
    return [A[i][size] / A[i][i] for i in range(size)]


def _rank(cfg, vecs):
    rows = [list(v) for v in vecs]
    scale = max([abs(x) for row in rows for x in row] + [1e-300])
    rank = 0
    width = len(rows[0]) if rows else 0
    for col in range(width):
        cand = [r for r in range(rank, len(rows))]
        if cfg.exact:
            piv = next((r for r in cand if rows[r][col] != 0), None)
        else:
            best = max(cand, key=lambda r: abs(rows[r][col])) if cand else None
            piv = best if best is not None and abs(rows[best][col]) > cfg.eps * scale else None
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        for r in range(len(rows)):
            if r != rank and rows[r][col] != 0:
                f = rows[r][col] / rows[rank][col]
                rows[r] = [x - f * y for x, y in zip(rows[r], rows[rank])]
        rank += 1
    return rank


def _dotv(a, b):
    s = 0.0 if not isinstance(a[0] if a else 0.0, Fraction) else Fraction(0)
    for x, y in zip(a, b):
        s = s + x * y
    return s


def _eqp(cfg, H, g, A):
    """KKT step for min 1/2 p'Hp + g'p s.t. A p = 0; returns (p, lam) with H p + g + A'lam = 0."""
    nv, m = len(g), len(A)
    size = nv + m
    M = [[_zero(cfg)] * size for _ in range(size)]
    for i in range(nv):
        for j in range(nv):
            M[i][j] = H[i][j]
    for k, a in enumerate(A):
        for i in range(nv):
            M[i][nv + k] = a[i]
            M[nv + k][i] = a[i]
    rhs = [-x for x in g] + [_zero(cfg)] * m
    sol = _gauss(cfg, M, rhs)
    if not cfg.exact:  # two rounds of iterative refinement on the float KKT solve
        for _ in range(2):
            resid = [rhs[r] - sum((M[r][c] * sol[c] for c in range(size)), 0.0) for r in range(size)]
            corr = _gauss(cfg, M, resid)
            sol = [a + b for a, b in zip(sol, corr)]
    return sol[:nv], sol[nv:]


def _solve_space(cfg, prob):
    """Active-set method on the space given by cfg.space: 'w' (turnover as 2**n sign forms) or 'wt' (explicit t)."""
    n = prob.n
    gam = _num(cfg, prob.gamma)
    sig = [[_num(cfg, prob.sigma[i][j]) for j in range(n)] for i in range(n)]
    mu = [_num(cfg, prob.mu[i]) for i in range(n)]
    w0 = [_num(cfg, prob.w0[i]) for i in range(n)]
    lo = [_num(cfg, prob.lower[i]) for i in range(n)]
    up = [_num(cfg, prob.upper[i]) for i in range(n)]
    tau = _num(cfg, prob.tau)
    caps = [_num(cfg, c) for c in prob.caps]
    nz = n if cfg.space == "w" else 2 * n
    H = [[_zero(cfg)] * nz for _ in range(nz)]
    for i in range(n):
        for j in range(n):
            H[i][j] = gam * sig[i][j]
    budget = [_num(cfg, 1)] * n + [_zero(cfg)] * (nz - n)
    rows = []  # (a, b, key): a.z <= b
    for i in range(n):
        a = [_zero(cfg)] * nz; a[i] = _num(cfg, -1); rows.append((a, -lo[i], ("lower", i)))
        a = [_zero(cfg)] * nz; a[i] = _num(cfg, 1); rows.append((a, up[i], ("upper", i)))
    for k, cap in enumerate(caps):
        a = [_zero(cfg)] * nz
        for j in range(n):
            if prob.sector[j] == k:
                a[j] = _num(cfg, 1)
        rows.append((a, cap, ("sector", k)))
    if cfg.space == "w":
        for signs in product((1, -1), repeat=n):
            a = [_num(cfg, s) for s in signs]
            b = tau + sum((a[i] * w0[i] for i in range(n)), _zero(cfg))
            rows.append((a, b, ("turn", signs)))
    else:
        for i in range(n):
            a = [_zero(cfg)] * nz; a[i] = _num(cfg, 1); a[n + i] = _num(cfg, -1); rows.append((a, w0[i], ("plus", i)))
            a = [_zero(cfg)] * nz; a[i] = _num(cfg, -1); a[n + i] = _num(cfg, -1); rows.append((a, -w0[i], ("minus", i)))
        a = [_zero(cfg)] * nz
        for i in range(n):
            a[n + i] = _num(cfg, 1)
        rows.append((a, tau, ("total", None)))
    z = [w0[i] for i in range(n)] + [_zero(cfg)] * (nz - n)
    def slack(a, b):
        return b - sum((x * y for x, y in zip(a, z)), _zero(cfg))
    tol = _num(cfg, 0) if cfg.exact else cfg.eps
    working = []
    if cfg.prepass:
        for j, (a, b, _) in enumerate(rows):
            if slack(a, b) <= tol and _rank(cfg, [budget] + [rows[k][0] for k in working] + [a]) > len(working) + 1:
                working.append(j)
    for _ in range(500):
        g = [sum((H[i][j] * z[j] for j in range(nz)), _zero(cfg)) for i in range(nz)]
        g = [g[i] - (mu[i] if i < n else _zero(cfg)) for i in range(nz)]
        A = [budget] + [rows[j][0] for j in working]
        p, lam = _eqp(cfg, H, g, A)
        pnorm = max(abs(x) for x in p) if p else 0.0
        if pnorm <= (tol if not cfg.exact else 0):
            ineq = [(lam[1 + k], k) for k in range(len(working))]
            neg = [(v, k) for v, k in ineq if v < (0 if cfg.exact else -cfg.eps)]
            if not neg:
                mult = {rows[j][2]: lam[1 + k] for k, j in enumerate(working)}
                return z, mult, lam[0]
            if cfg.drop == "most_negative":
                _, k = min(neg)
            else:
                k = min(neg, key=lambda t: rows[working[t[1]]][2])[1]
            working.pop(k)
            continue
        step, block = _num(cfg, 1), None
        pn = math.sqrt(sum(float(x) * float(x) for x in p))
        for j, (a, b, _) in enumerate(rows):
            if j in working:
                continue
            rate = sum((x * y for x, y in zip(a, p)), _zero(cfg))
            an = math.sqrt(sum(float(x) * float(x) for x in a))
            # relative threshold: float noise in p is proportional to |p| (large when gamma is tiny)
            if rate > (0 if cfg.exact else 1e-12 * an * pn):
                ratio = max(slack(a, b), _zero(cfg)) / rate
                if ratio < step:
                    step, block = ratio, j
        z = [zi + step * pi for zi, pi in zip(z, p)]
        if block is not None:
            working.append(block)
    raise RuntimeError("no convergence")


def _sign_multipliers(prob, cfg, z, mult, budget_mult):
    n = prob.n
    if cfg.space == "w":
        lower = [mult.get(("lower", i), 0.0) for i in range(n)]
        upper = [mult.get(("upper", i), 0.0) for i in range(n)]
        sector = [mult.get(("sector", k), 0.0) for k in range(len(prob.caps))]
        signs = {key[1]: v for key, v in mult.items() if key[0] == "turn"}
        kappa = sum(signs.values(), 0.0 * 1) if signs else 0.0
        plus, minus = [], []
        for i in range(n):
            net = sum((eta * s[i] for s, eta in signs.items()), 0.0 * 1)
            plus.append((kappa + net) / 2)
            minus.append((kappa - net) / 2)
    else:
        lower = [mult.get(("lower", i), 0.0) for i in range(n)]
        upper = [mult.get(("upper", i), 0.0) for i in range(n)]
        sector = [mult.get(("sector", k), 0.0) for k in range(len(prob.caps))]
        plus = [mult.get(("plus", i), 0.0) for i in range(n)]
        minus = [mult.get(("minus", i), 0.0) for i in range(n)]
        kappa = mult.get(("total", None), 0.0)
    return {
        "budget": float(budget_mult),
        "lower": [float(v) for v in lower],
        "upper": [float(v) for v in upper],
        "sector": [float(v) for v in sector],
        "turnover_plus": [float(v) for v in plus],
        "turnover_minus": [float(v) for v in minus],
        "turnover_total": float(kappa),
    }


def _float_certificate(prob, w, m):
    """Independent float certificate from the page definitions, with t_i = |d_i|."""
    n = prob.n
    w = [float(x) for x in w]
    w0 = [float(x) for x in prob.w0]
    d = [w[i] - w0[i] for i in range(n)]
    t = [abs(x) for x in d]
    sec = [sum(w[i] for i in range(n) if prob.sector[i] == k) for k in range(len(prob.caps))]
    gaps = []
    for i in range(n):
        gaps += [float(prob.lower[i]) - w[i], w[i] - float(prob.upper[i]), d[i] - t[i], -d[i] - t[i]]
    gaps += [sec[k] - float(prob.caps[k]) for k in range(len(prob.caps))]
    gaps += [sum(t) - float(prob.tau)]
    primal = max([0.0, abs(sum(w) - 1.0)] + gaps)
    ineq = (m["lower"] + m["upper"] + m["sector"] + m["turnover_plus"] + m["turnover_minus"] + [m["turnover_total"]])
    dual = max(0.0, -min(ineq))
    comp_pairs = (
        [(m["lower"][i], float(prob.lower[i]) - w[i]) for i in range(n)]
        + [(m["upper"][i], w[i] - float(prob.upper[i])) for i in range(n)]
        + [(m["sector"][k], sec[k] - float(prob.caps[k])) for k in range(len(prob.caps))]
        + [(m["turnover_plus"][i], d[i] - t[i]) for i in range(n)]
        + [(m["turnover_minus"][i], -d[i] - t[i]) for i in range(n)]
        + [(m["turnover_total"], sum(t) - float(prob.tau))]
    )
    comp = max(abs(a * b) for a, b in comp_pairs)
    stat = 0.0
    for i in range(n):
        grad = float(prob.gamma) * sum(float(prob.sigma[i][j]) * w[j] for j in range(n)) - float(prob.mu[i])
        rw = grad + m["budget"] - m["lower"][i] + m["upper"][i] + m["sector"][prob.sector[i]]
        rw += m["turnover_plus"][i] - m["turnover_minus"][i]
        rt = m["turnover_total"] - m["turnover_plus"][i] - m["turnover_minus"][i]
        stat = max(stat, abs(rw), abs(rt))
    return {"primal_residual": primal, "stationarity_residual": stat, "dual_residual": dual,
            "complementary_slackness": comp}


def allocate(instance):
    prob = _parse(instance)
    z, mult, bmult = _solve_space(CFG, prob)
    n = prob.n
    if CFG.space == "w":
        w = [float(z[i]) for i in range(n)]
    else:
        w = [float(z[i]) for i in range(n)]
    m = _sign_multipliers(prob, CFG, z, mult, bmult)
    return {"weights": w, "multipliers": m, "certificate": _float_certificate(prob, w, m)}


CFG = _Cfg('wt', False, 'most_negative', True, 1e-14)
