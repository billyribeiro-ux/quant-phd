"""Build five independent alternative correct allocators for the M7 project (round 4).

Each alternative is the grader's reference.py with its _parse, _certificate and allocate kept, and with _solve
replaced by a different active-set search (appended after the original definitions, so the later definition is the
one called). The alternatives differ in arithmetic (exact Fraction or float), in the pivot rule that drops a working
constraint (most negative multiplier or Bland's smallest index), in the start (the constraints active at w0, or an
empty working set), and in the numerical cutoffs (drop, block, step and rank tolerances). Each file is stdlib only.
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD4-M7-d")
REF = ROOT / "course/modules/M/M7/grader/reference.py"
OUT = ROOT / "ledgers/M7/scripts/M7-d-r4/alts"

GENERIC = '''

# ---- round-4 alternative: generic active-set search (appended; overrides the reference _solve) ----
from fractions import Fraction as _F


def _alt_solve(problem, arith, drop_tol, block_tol, rank_tol, step_tol, rule, start):
    exact = arith == "exact"

    def cv(q):
        return q if exact else float(q)

    n = problem.n
    H = [[cv(problem.gamma * problem.sigma[i][j]) for j in range(n)] for i in range(n)]
    mu = [cv(v) for v in problem.mu]
    w0 = [cv(v) for v in problem.w0]
    lo = [cv(v) for v in problem.lower]
    up = [cv(v) for v in problem.upper]
    caps = [cv(v) for v in problem.caps]
    tau = cv(problem.tau)
    one = cv(_F(1))
    zero = cv(_F(0))
    rows = []
    for i in range(n):
        rows.append(([(-one if j == i else zero) for j in range(n)], -lo[i], ("lower", i)))
        rows.append(([(one if j == i else zero) for j in range(n)], up[i], ("upper", i)))
    for k, cap in enumerate(caps):
        rows.append(([(one if problem.sector[j] == k else zero) for j in range(n)], cap, ("sector", k)))
    from itertools import product as _p

    for signs in _p((1, -1), repeat=n):
        a = [cv(_F(s)) for s in signs]
        rows.append((a, tau + sum((x * y for x, y in zip(a, w0)), zero), ("turn", signs)))

    def dot(a, b):
        return sum((x * y for x, y in zip(a, b)), zero)

    def solve_sys(M, r):
        size = len(r)
        A = [list(M[i]) + [r[i]] for i in range(size)]
        for c in range(size):
            if exact:
                piv = next((q for q in range(c, size) if A[q][c] != 0), None)
            else:
                piv = max(range(c, size), key=lambda q: abs(A[q][c]))
                if abs(A[piv][c]) <= 1e-300:
                    piv = None
            if piv is None:
                raise RuntimeError("singular KKT system")
            A[c], A[piv] = A[piv], A[c]
            for q in range(size):
                if q != c and A[q][c] != 0:
                    f = A[q][c] / A[c][c]
                    A[q] = [x - f * y for x, y in zip(A[q], A[c])]
        return [A[i][size] / A[i][i] for i in range(size)]

    def rank(vecs):
        M = [list(v) for v in vecs]
        rk = 0
        width = len(M[0]) if M else 0
        for c in range(width):
            if exact:
                piv = next((q for q in range(rk, len(M)) if M[q][c] != 0), None)
            else:
                cand = max(range(rk, len(M)), key=lambda q: abs(M[q][c])) if rk < len(M) else None
                piv = cand if cand is not None and abs(M[cand][c]) > rank_tol else None
            if piv is None:
                continue
            M[rk], M[piv] = M[piv], M[rk]
            for q in range(len(M)):
                if q != rk and M[q][c] != 0:
                    f = M[q][c] / M[rk][c]
                    M[q] = [x - f * y for x, y in zip(M[q], M[rk])]
            rk += 1
        return rk

    x = list(w0)
    working = []
    if start == "active":
        for j, (a, b, _) in enumerate(rows):
            if b - dot(a, x) <= (zero if exact else block_tol) and rank([[one] * n, *(rows[k][0] for k in working), a]) > len(working) + 1:
                working.append(j)
    for _ in range(2000):
        g = [dot(H[i], x) - mu[i] for i in range(n)]
        act = [[one] * n] + [rows[j][0] for j in working]
        size = n + len(act)
        M = [[zero] * size for _ in range(size)]
        for i in range(n):
            for j in range(n):
                M[i][j] = H[i][j]
        for k, a in enumerate(act):
            for i in range(n):
                M[i][n + k] = a[i]
                M[n + k][i] = a[i]
        sol = solve_sys(M, [-v for v in g] + [zero] * len(act))
        p, lam = sol[:n], sol[n:]
        if all(abs(v) <= (zero if exact else step_tol) for v in p):
            neg = [(lam[1 + k], k) for k in range(len(working)) if lam[1 + k] < -(zero if exact else drop_tol)]
            if not neg:
                mult = {rows[j][2]: lam[1 + k] for k, j in enumerate(working)}
                return x, mult, lam[0]
            if rule == "min":
                drop = min(neg)[1]
            else:
                drop = min(k for _, k in neg)
            working.pop(drop)
            continue
        step, blocking = one, None
        for j, (a, b, key) in enumerate(rows):
            if j in working:
                continue
            rate = dot(a, p)
            if rate > (zero if exact else step_tol):
                ratio = max(b - dot(a, x), zero) / rate
                better = ratio < step if rule == "min" else (ratio < step or (ratio == step and blocking is None))
                if better:
                    step, blocking = ratio, j
        x = [xi + step * pi for xi, pi in zip(x, p)]
        if blocking is not None:
            cand = rows[blocking][0]
            if rank([[one] * n, *(rows[j][0] for j in working), cand]) <= len(working) + 1:
                raise RuntimeError("working set dependent")
            working.append(blocking)
    raise RuntimeError("no convergence")


def _solve(problem):
    from types import SimpleNamespace
    n = problem.n
    if SCALE:
        # objective scaling: divide the objective and its linear term by s, solve, then multiply the multipliers by s
        s = max(abs(float(problem.gamma * problem.sigma[i][j])) for i in range(n) for j in range(n))
        scaled = SimpleNamespace(n=n, gamma=problem.gamma / _F(s), sigma=problem.sigma, mu=[m / _F(s) for m in problem.mu],
                                 w0=problem.w0, lower=problem.lower, upper=problem.upper, sector=problem.sector,
                                 caps=problem.caps, tau=problem.tau)
        x, mult, budget_mult = _alt_solve(scaled, ARITH, DROP, BLOCK, RANK, STEP, RULE, START)
        mult = {key: v * s for key, v in mult.items()}
        budget_mult = budget_mult * s
    else:
        x, mult, budget_mult = _alt_solve(problem, ARITH, DROP, BLOCK, RANK, STEP, RULE, START)
    lower = [mult.get(("lower", i), 0) for i in range(n)]
    upper = [mult.get(("upper", i), 0) for i in range(n)]
    sector = [mult.get(("sector", k), 0) for k in range(len(problem.caps))]
    signs = {key[1]: v for key, v in mult.items() if key[0] == "turn"}
    kappa = sum(signs.values(), 0)
    plus = [0] * n
    minus = [0] * n
    for i in range(n):
        net = sum((eta * s[i] for s, eta in signs.items()), 0)
        plus[i] = (kappa + net) / 2
        minus[i] = (kappa - net) / 2
    return {"w": x, "budget": budget_mult, "lower": lower, "upper": upper, "sector": sector,
            "plus": plus, "minus": minus, "kappa": kappa}
'''

VARIANTS = {
    # name: (arith, drop_tol, block_tol, rank_tol, step_tol, rule, start)
    "alt_r4_exact_empty_start_min": ("exact", 0, 0, 0, 0, "min", "empty", False),
    "alt_r4_float_1e-12_active_start": ("float", 1e-12, 1e-12, 1e-12, 1e-12, "min", "active", False),
    "alt_r4_float_lax_bland_empty": ("float", 1e-7, 1e-10, 1e-9, 1e-10, "bland", "empty", False),
    "alt_r4_exact_bland_active": ("exact", 0, 0, 0, 0, "bland", "active", False),
    "alt_r4_float_1e-9_min_empty": ("float", 1e-9, 1e-9, 1e-9, 1e-9, "min", "empty", False),
    "alt_r4_float_scaled_1e-12_min_active": ("float", 1e-12, 1e-12, 1e-12, 1e-12, "min", "active", True),
}


def main() -> int:
    base = REF.read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (arith, drop, block, rank, step, rule, start, scale) in VARIANTS.items():
        head = (
            f"\nARITH = {arith!r}\nDROP = {drop!r}\nBLOCK = {block!r}\nRANK = {rank!r}\nSTEP = {step!r}\n"
            f"RULE = {rule!r}\nSTART = {start!r}\nSCALE = {scale!r}\n"
        )
        text = base + GENERIC + head
        (OUT / f"{name}.py").write_text(text, encoding="utf-8")
        print("wrote", name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
