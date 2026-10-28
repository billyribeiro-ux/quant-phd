"""Verifier-written alternative correct solvers for the M7 project (stdlib only), for over-constraint testing.

Five routes to the same problem: two exact active-set routes started from different points, and three routes that
first find an approximate point by a float penalty method and then polish it to the exact active face. Every route
returns weights, multipliers and a certificate in the page's definitions. The suite must accept all five.
"""

import itertools
import math
from fractions import Fraction as F
from typing import Any


def _f(x: Any) -> F:
    return F(repr(float(x))) if isinstance(x, float) else F(x)


def _setup(c: dict[str, Any]) -> dict[str, Any]:
    """Validation is shared with the reference (the spec fixes it); the solve routes below differ."""
    p = _parse(c)
    return {
        "n": p.n,
        "mu": p.mu,
        "g": p.gamma,
        "S": p.sigma,
        "w0": p.w0,
        "lo": p.lower,
        "up": p.upper,
        "sec": p.sector,
        "caps": p.caps,
        "tau": p.tau,
    }


def _rows(P: dict[str, Any]) -> list[tuple[tuple[Any, ...], list[F], F]]:
    """Rows a.w <= b: bounds, sector caps, and the 2**n sign forms of the turnover limit."""
    n = P["n"]
    R: list[tuple[tuple[Any, ...], list[F], F]] = []
    for i in range(n):
        R.append((("lo", i), [F(-1) if j == i else F(0) for j in range(n)], -P["lo"][i]))
        R.append((("up", i), [F(1) if j == i else F(0) for j in range(n)], P["up"][i]))
    for k, cap in enumerate(P["caps"]):
        R.append((("sec", k), [F(1) if P["sec"][j] == k else F(0) for j in range(n)], cap))
    for s in itertools.product((1, -1), repeat=n):
        R.append((("turn", s), [F(x) for x in s], P["tau"] + sum(F(s[j]) * P["w0"][j] for j in range(n))))
    return R


def _gauss(M: list[list[F]], r: list[F]) -> list[F] | None:
    m = len(r)
    A = [M[i][:] + [r[i]] for i in range(m)]
    for c in range(m):
        p = next((k for k in range(c, m) if A[k][c] != 0), None)
        if p is None:
            return None
        A[c], A[p] = A[p], A[c]
        for k in range(m):
            if k != c and A[k][c] != 0:
                fct = A[k][c] / A[c][c]
                A[k] = [x - fct * y for x, y in zip(A[k], A[c], strict=True)]
    return [A[i][m] / A[i][i] for i in range(m)]


def _kkt(P: dict[str, Any], R: list[Any], active: list[int]) -> tuple[list[F], F, list[F]] | None:
    """Solve stationarity, the budget and the active rows as equalities; unknowns are w, nu and the active multipliers."""
    n, m = P["n"], len(active)
    size = n + 1 + m
    M = [[F(0)] * size for _ in range(size)]
    r = [F(0)] * size
    for i in range(n):
        for j in range(n):
            M[i][j] = P["g"] * P["S"][i][j]
        M[i][n] = F(1)
        for c, j in enumerate(active):
            M[i][n + 1 + c] = R[j][1][i]
        r[i] = P["mu"][i]
    for j in range(n):
        M[n][j] = F(1)
    r[n] = F(1)
    for c, j in enumerate(active):
        for k in range(n):
            M[n + 1 + c][k] = R[j][1][k]
        r[n + 1 + c] = R[j][2]
    x = _gauss(M, r)
    if x is None:
        return None
    return x[:n], x[n], x[n + 1 :]


def _polish(P: dict[str, Any], R: list[Any], start: list[int], rule: str) -> tuple[list[F], F, dict[tuple[Any, ...], F]]:
    """Active-set loop in exact arithmetic: drop the most negative multiplier, add a violated row (rule: 'worst' or 'first')."""
    active = list(start)
    for _ in range(2000):
        sol = _kkt(P, R, active)
        if sol is None:
            if not active:
                raise RuntimeError("the budget-only system is singular")
            active.pop()
            continue
        w, nu, lam = sol
        neg = [(lam[c], c) for c in range(len(active)) if lam[c] < 0]
        if neg:
            active.pop(min(neg)[1])
            continue
        viol = [
            (sum(a[k] * w[k] for k in range(P["n"])) - b, j)
            for j, (_, a, b) in enumerate(R)
            if j not in active and sum(a[k] * w[k] for k in range(P["n"])) - b > 0
        ]
        if viol:
            pick = max(viol)[1] if rule == "worst" else min(v[1] for v in viol)
            active.append(pick)
            continue
        return w, nu, {R[j][0]: lam[c] for c, j in enumerate(active)}
    raise RuntimeError("the active-set loop did not finish")


def _certificate(P: dict[str, Any], w: list[F], nu: F, mult: dict[tuple[Any, ...], F]) -> dict[str, Any]:
    n = P["n"]
    lo = [mult.get(("lo", i), F(0)) for i in range(n)]
    up = [mult.get(("up", i), F(0)) for i in range(n)]
    sec = [mult.get(("sec", k), F(0)) for k in range(len(P["caps"]))]
    eta = {key[1]: v for key, v in mult.items() if key[0] == "turn"}
    kappa = sum(eta.values(), F(0))
    net = [sum((v * s[i] for s, v in eta.items()), F(0)) for i in range(n)]
    plus = [(kappa + net[i]) / 2 for i in range(n)]
    minus = [(kappa - net[i]) / 2 for i in range(n)]
    d = [w[i] - P["w0"][i] for i in range(n)]
    t = [abs(v) for v in d]
    sector_sum = [sum((w[i] for i in range(n) if P["sec"][i] == k), F(0)) for k in range(len(P["caps"]))]
    gaps = []
    for i in range(n):
        gaps += [P["lo"][i] - w[i], w[i] - P["up"][i], d[i] - t[i], -d[i] - t[i]]
    gaps += [sector_sum[k] - P["caps"][k] for k in range(len(P["caps"]))]
    gaps.append(sum(t) - P["tau"])
    primal = max([F(0), abs(sum(w) - 1), *gaps])
    ineq = [*lo, *up, *sec, *plus, *minus, kappa]
    dual = max(F(0), -min(ineq))
    gvals = [*[P["lo"][i] - w[i] for i in range(n)], *[w[i] - P["up"][i] for i in range(n)], *[sector_sum[k] - P["caps"][k] for k in range(len(P["caps"]))], *[d[i] - t[i] for i in range(n)], *[-d[i] - t[i] for i in range(n)], sum(t) - P["tau"]]
    comp = max(abs(m * g) for m, g in zip(ineq, gvals, strict=True))
    stat = F(0)
    for i in range(n):
        grad = P["g"] * sum((P["S"][i][j] * w[j] for j in range(n)), F(0)) - P["mu"][i]
        rw = grad + nu - lo[i] + up[i] + sec[P["sec"][i]] + plus[i] - minus[i]
        rt = kappa - plus[i] - minus[i]
        stat = max(stat, abs(rw), abs(rt))
    return {
        "primal_residual": float(primal),
        "stationarity_residual": float(stat),
        "dual_residual": float(dual),
        "complementary_slackness": float(comp),
    }


def _output(P: dict[str, Any], w: list[F], nu: F, mult: dict[tuple[Any, ...], F]) -> dict[str, Any]:
    n = P["n"]
    eta = {key[1]: v for key, v in mult.items() if key[0] == "turn"}
    kappa = sum(eta.values(), F(0))
    net = [sum((v * s[i] for s, v in eta.items()), F(0)) for i in range(n)]
    return {
        "weights": [float(v) for v in w],
        "multipliers": {
            "budget": float(nu),
            "lower": [float(mult.get(("lo", i), F(0))) for i in range(n)],
            "upper": [float(mult.get(("up", i), F(0))) for i in range(n)],
            "sector": [float(mult.get(("sec", k), F(0))) for k in range(len(P["caps"]))],
            "turnover_plus": [float((kappa + net[i]) / 2) for i in range(n)],
            "turnover_minus": [float((kappa - net[i]) / 2) for i in range(n)],
            "turnover_total": float(kappa),
        },
        "certificate": _certificate(P, w, nu, mult),
    }


def _active_from(P: dict[str, Any], R: list[Any], x: list[F], tol: F) -> list[int]:
    return [j for j, (_, a, b) in enumerate(R) if b - sum(a[k] * x[k] for k in range(P["n"])) <= tol]


def _penalty_point(P: dict[str, Any], R: list[Any], start: list[float], rho: float, iters: int) -> list[float]:
    """Float gradient descent on f plus a quadratic penalty for every row and for the budget."""
    n = P["n"]
    S = [[float(v) for v in row] for row in P["S"]]
    g = float(P["g"])
    mu = [float(v) for v in P["mu"]]
    rows = [([float(v) for v in a], float(b)) for _, a, b in R]
    lip = g * sum(abs(v) for row in S for v in row) + rho * (2 * sum(sum(v * v for v in a) for a, _ in rows) + 2 * n)
    step = 1.0 / lip
    w = list(start)
    for _ in range(iters):
        grad = [g * sum(S[i][j] * w[j] for j in range(n)) - mu[i] for i in range(n)]
        for a, b in rows:
            slack = sum(a[k] * w[k] for k in range(n)) - b
            if slack > 0:
                for k in range(n):
                    grad[k] += 2 * rho * slack * a[k]
        resid = sum(w) - 1.0
        for k in range(n):
            grad[k] += 2 * rho * resid
        w = [w[k] - step * grad[k] for k in range(n)]
    return w


def _budget_only(P: dict[str, Any]) -> list[F]:
    """Budget-only solution: the starting point of route 2 (not feasible in general)."""
    R: list[Any] = []
    w, _, _ = _polish(P, R, [], "first")
    return w


def _independent(vectors: list[list[F]]) -> bool:
    """True when the vectors are linearly independent (Gauss elimination in exact arithmetic)."""
    rows = [v[:] for v in vectors]
    rank = 0
    for col in range(len(rows[0])):
        p = next((r for r in range(rank, len(rows)) if rows[r][col] != 0), None)
        if p is None:
            continue
        rows[rank], rows[p] = rows[p], rows[rank]
        for r in range(len(rows)):
            if r != rank and rows[r][col] != 0:
                fct = rows[r][col] / rows[rank][col]
                rows[r] = [x - fct * y for x, y in zip(rows[r], rows[rank], strict=True)]
        rank += 1
    return rank == len(vectors)


def _primal_active_set(
    P: dict[str, Any], R: list[Any], drop: str = "bland", order: str = "forward"
) -> tuple[list[F], F, dict[tuple[Any, ...], F]]:
    """Primal active-set method from the feasible starting portfolio. drop: bland (lowest index) or dantzig (most negative)."""
    n = P["n"]
    H = [[P["g"] * P["S"][i][j] for j in range(n)] for i in range(n)]
    x = list(P["w0"])
    W: list[int] = []
    indices = list(range(len(R)))
    if order == "reverse":
        indices.reverse()
    for j in indices:
        _, a, b = R[j]
        if False:
            pass
        if b - sum(a[k] * x[k] for k in range(n)) == 0 and _independent([[F(1)] * n] + [R[k][1] for k in W] + [a]):
            W.append(j)
    for _ in range(2000):
        grad = [sum(H[i][j] * x[j] for j in range(n)) - P["mu"][i] for i in range(n)]
        eq = [[F(1)] * n] + [R[j][1] for j in W]
        m = len(eq)
        M = [[F(0)] * (n + m) for _ in range(n + m)]
        r = [F(0)] * (n + m)
        for i in range(n):
            for j in range(n):
                M[i][j] = H[i][j]
            for c in range(m):
                M[i][n + c] = eq[c][i]
            r[i] = -grad[i]
        for c in range(m):
            for j in range(n):
                M[n + c][j] = eq[c][j]
        sol = _gauss(M, r)
        if sol is None:
            raise RuntimeError("singular working set")
        p, mu_eq = sol[:n], sol[n:]
        if all(v == 0 for v in p):
            neg = [c for c in range(1, m) if mu_eq[c] < 0]
            if not neg:
                mult = {R[j][0]: mu_eq[1 + c] for c, j in enumerate(W)}
                return x, mu_eq[0], mult
            pick = min(neg, key=lambda c: W[c - 1]) if drop == "bland" else min(neg, key=lambda c: mu_eq[c])
            W.pop(pick - 1)
            continue
        step, block = F(1), None
        for j, (_, a, b) in enumerate(R):
            if j in W:
                continue
            rate = sum(a[k] * p[k] for k in range(n))
            if rate > 0:
                ratio = max(b - sum(a[k] * x[k] for k in range(n)), F(0)) / rate
                if ratio < step:
                    step, block = ratio, j
        x = [x[i] + step * p[i] for i in range(n)]
        if block is not None:
            W.append(block)
    raise RuntimeError("the primal active-set loop did not finish")


def allocate_alt1(instance: dict[str, Any]) -> dict[str, Any]:
    """Route 1: textbook primal active-set from the starting portfolio (its tight rows), Bland's rule for drops."""
    P = _setup(instance)
    R = _rows(P)
    w, nu, mult = _primal_active_set(P, R, "bland", "forward")
    return _output(P, w, nu, mult)


def allocate_alt2(instance: dict[str, Any]) -> dict[str, Any]:
    """Route 2: primal active-set from the starting portfolio with the most-negative-multiplier (Dantzig) drop rule."""
    P = _setup(instance)
    R = _rows(P)
    w, nu, mult = _primal_active_set(P, R, "dantzig", "forward")
    return _output(P, w, nu, mult)


def _penalty_then_polish(instance: dict[str, Any], rho: float, iters: int, tol: F, rule: str) -> dict[str, Any]:
    """Float penalty descent, then exact polish of the rows within tol of tight; if the polish cycles, the primal route."""
    P = _setup(instance)
    R = _rows(P)
    approx = _penalty_point(P, R, [float(v) for v in P["w0"]], rho, iters)
    x = [_f(v) for v in approx]
    try:
        w, nu, mult = _polish(P, R, _active_from(P, R, x, tol), rule)
    except RuntimeError:
        w, nu, mult = _primal_active_set(P, R, "bland", "forward")
    return _output(P, w, nu, mult)


def allocate_alt3(instance: dict[str, Any]) -> dict[str, Any]:
    """Route 3: float quadratic-penalty descent (rho 1e4), then exact polish of the rows within 1e-4 of tight."""
    return _penalty_then_polish(instance, 1e4, 6000, F(1, 10**4), "worst")


def allocate_alt4(instance: dict[str, Any]) -> dict[str, Any]:
    """Route 4: float penalty descent with a stronger penalty (rho 1e6), polish with a 1e-4 active cutoff."""
    return _penalty_then_polish(instance, 1e6, 6000, F(1, 10**4), "worst")


def allocate_alt5(instance: dict[str, Any]) -> dict[str, Any]:
    """Route 5: primal active-set with Bland's drops but the starting working set built in reverse row order."""
    P = _setup(instance)
    R = _rows(P)
    w, nu, mult = _primal_active_set(P, R, "bland", "reverse")
    return _output(P, w, nu, mult)
