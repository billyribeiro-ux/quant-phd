"""Independent recomputation for M7 slice b (L04 to L06). Standard library only; run with python -I.

Each block re-derives a number that a page states, from the definitions, without importing the lab twins.
"""

from fractions import Fraction as F
from itertools import product


def gauss(a, b):
    """Solve a x = b exactly (independent elimination, no pivot search beyond nonzero)."""
    n = len(b)
    m = [list(map(F, row)) + [F(v)] for row, v in zip(a, b)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [x / piv for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] for i in range(n)]


def det(a):
    """Determinant by fraction Gaussian elimination."""
    n = len(a)
    m = [list(map(F, r)) for r in a]
    d = F(1)
    for c in range(n):
        p = next((r for r in range(c, n) if m[r][c] != 0), None)
        if p is None:
            return F(0)
        if p != c:
            m[c], m[p] = m[p], m[c]
            d = -d
        d *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return d


print("== L04")
S = [[F(2), F(1)], [F(1), F(2)]]
mu = [F(3, 2), F(1, 5)]
Sinv = [[F(2, 3), F(-1, 3)], [F(-1, 3), F(2, 3)]]


def g(lam, nu):
    r = [mu[0] + lam[0] - nu, mu[1] + lam[1] - nu]
    q = sum(r[i] * Sinv[i][j] * r[j] for i in range(2) for j in range(2))
    return -q / 2 - nu


def f(w):
    q = sum(w[i] * S[i][j] * w[j] for i in range(2) for j in range(2))
    return q / 2 - (mu[0] * w[0] + mu[1] * w[1])


print("g(0,0) =", g((F(0), F(0)), F(0)), "(page: -199/300)")
print("KKT dual =", g((F(0), F(3, 10)), F(-1, 2)), " f(1,0) =", f((F(1), F(0))))
print("M3 check: mu'Sinv mu =", sum(mu[i] * Sinv[i][j] * mu[j] for i in range(2) for j in range(2)), "(page: 199/150)")
print("E2 difference:", F(-199, 300) - F(-1, 2), "(page: -49/300)", " decimal", float(F(-199, 300)))
# R3: lambda = 0 grid over nu in steps of 1/10 on [-1,0]
grid_nu = [F(j - 10, 10) for j in range(11)]
vals = {nu: g((F(0), F(0)), nu) for nu in grid_nu}
best = max(vals.values())
print("R3 grid max over nu:", best, "at", [str(k) for k, v in vals.items() if v == best], "(page: -157/300 at -3/5 and -7/10)")
print("R3 grid gap:", F(-1, 2) - best, "(page: 7/300)")
# continuous maximiser
print("R3 g(0,-13/20) =", g((F(0), F(0)), F(-13, 20)), "(page: -209/400)")
# attaining count in full dual grid, exact
lams = [F(j, 10) for j in range(11)]
allv = [(g((a, b), nu), (a, b, nu)) for a in lams for b in lams for nu in grid_nu]
mx = max(v for v, _ in allv)
print("full grid max", mx, "attained", sum(1 for v, _ in allv if v == mx))
pts = [F(k, 20) for k in range(21)]
print("full grid weak duality pairs holding:", sum(1 for v, _ in allv for k in range(21) if v <= f((pts[k], 1 - pts[k]))), "of", len(allv) * 21)

print("== L05")
Q = [[F(4), F(1), F(0)], [F(1), F(3), F(1)], [F(0), F(1), F(2)]]
A = [[F(1), F(1), F(1)], [F(0), F(1), F(-1)]]
c = [F(-1), F(0), F(2)]
K = [Q[i] + [A[k][i] for k in range(2)] for i in range(3)] + [A[k] + [F(0), F(0)] for k in range(2)]
print("det K =", det(K), "(page: 19)")
sol = gauss(K, [-x for x in c] + [F(1), F(0)])
print("x =", [str(v) for v in sol[:3]], "lambda =", [str(v) for v in sol[3:]], "(page: 13/19 3/19 3/19; -36/19 11/19)")
xs = sol[:3]
objA = F(1, 2) * sum(xs[i] * Q[i][j] * xs[j] for i in range(3) for j in range(3)) + sum(c[i] * xs[i] for i in range(3))
print("objective A =", objA, float(objA), "(page: 551/722)")
v = [F(-2), F(1), F(1)]
vqv = sum(v[i] * Q[i][j] * v[j] for i in range(3) for j in range(3))
print("v'Qv =", vqv, "(page quiz: 19)")
# Remark 2.4 identity check at random rational points
import random
random.seed(1)
ok = True
for _ in range(200):
    x1, x2, x3 = (F(random.randint(-9, 9), random.randint(1, 5)) for _ in range(3))
    lhs = 4 * x1 * x1 + 3 * x2 * x2 + 2 * x3 * x3 + 2 * x1 * x2 + 2 * x2 * x3
    rhs = (2 * x1 + F(1, 2) * x2) ** 2 + F(11, 4) * (x2 + F(4, 11) * x3) ** 2 + F(18, 11) * x3 * x3
    ok = ok and lhs == rhs
print("Remark 2.4 completed-square identity holds on 200 rational points:", ok)
# Part B: active-set candidates for Q2=[[2,1],[1,2]], c=(-3,1), x>=0
Q2 = [[F(2), F(1)], [F(1), F(2)]]
c2 = [F(-3), F(1)]
f2 = lambda x: F(1, 2) * sum(x[i] * Q2[i][j] * x[j] for i in range(2) for j in range(2)) + sum(c2[i] * x[i] for i in range(2))
for mask in product((0, 1), repeat=2):
    free = [i for i in range(2) if not mask[i]]
    x = [F(0), F(0)]
    if free:
        sub = [[Q2[i][j] for j in free] for i in free]
        s = gauss(sub, [-c2[i] for i in free])
        for p, val in zip(free, s):
            x[p] = val
    grad = [sum(Q2[i][j] * x[j] for j in range(2)) + c2[i] for i in range(2)]
    print("mask", mask, "x", [str(t) for t in x], "primal", all(t >= 0 for t in x), "dual", all(grad[i] >= 0 for i in range(2) if mask[i]))
print("Example 3.6 f(3/2,0) =", f2([F(3, 2), F(0)]))
bad = sum(1 for a in range(33) for b in range(33) if f2([F(a, 16), F(b, 16)]) < f2([F(3, 2), F(0)]))
print("grid points below candidate (independent):", bad, "(page: 0 of 1089)")

print("== L06")
gen = {"s": 2026}


def draw(mod):
    gen["s"] = (1103515245 * gen["s"] + 12345) % 2**31
    return gen["s"] % mod


M = [[F(draw(7) - 3) for _ in range(4)] for _ in range(4)]
mu6 = [F(draw(13) + 2, 100) for _ in range(4)]
Sig = [[sum(M[k][i] * M[k][j] for k in range(4)) / 16 + (F(1, 10) if i == j else F(0)) for j in range(4)] for i in range(4)]
print("mu", [str(t) for t in mu6], "(page: 7/100 1/20 3/25 1/50)")
print("Sigma diag", [str(Sig[i][i]) for i in range(4)], "(page: 49/40 27/20 103/80 103/80)")


def var(w):
    return sum(w[i] * Sig[i][j] * w[j] for i in range(4) for j in range(4))


def ret(w):
    return sum(mu6[i] * w[i] for i in range(4))


def closed(gam):
    one = [F(1)] * 4
    a = gauss(Sig, mu6)
    b = gauss(Sig, one)
    lam = (sum(a) - gam) / sum(b)
    return [(a[i] - lam * b[i]) / gam for i in range(4)], sum(b)


def eq_solve(gam):
    w, _ = closed(gam)
    return w


out = {}
for gam in [F(1), F(2), F(4), F(8), F(16)]:
    w = eq_solve(gam)
    obj = gam / 2 * var(w) - ret(w)
    out[gam] = (w, obj)
    print("eq gamma", gam, "return %.6f var %.6f obj %.6f" % (float(ret(w)), float(var(w)), float(obj)), "weights", ["%.6f" % float(t) for t in w])
print("1'b > 0 check:", closed(F(1))[1] > 0)
print("E2: eq obj 16 =", float(out[F(16)][1]))
# independent nonnegative solve by enumerating active sets with exact arithmetic
best = {}
for gam in [F(1), F(2), F(4), F(8), F(16)]:
    cands = []
    for zmask in product((0, 1), repeat=4):
        free = [i for i in range(4) if not zmask[i]]
        if not free:
            continue
        sub = [[gam * Sig[i][j] for j in free] for i in free]
        kkt = [row + [F(1)] for row in sub] + [[F(1)] * len(free) + [F(0)]]
        sol = gauss(kkt, [mu6[i] for i in free] + [F(1)])
        wf, lam = sol[:-1], sol[-1]
        w = [F(0)] * 4
        for p, val in zip(free, wf):
            w[p] = val
        sw = [sum(Sig[i][j] * w[j] for j in range(4)) for i in range(4)]
        nu = [gam * sw[i] - mu6[i] + lam for i in range(4)]
        if all(t >= 0 for t in w) and all(nu[i] >= 0 for i in range(4) if zmask[i]):
            cands.append((zmask, w))
    obj_of = lambda w: gam / 2 * var(w) - ret(w)
    zmask, w = min(cands, key=lambda t: obj_of(t[1]))
    best[gam] = (zmask, w)
    print("nonneg gamma", gam, "kept", len(cands), "zero set", zmask, "return %.6f var %.6f obj %.6f" % (float(ret(w)), float(var(w)), float(obj_of(w))), ["%.6f" % float(t) for t in w])
print("E2: nonneg obj 16 =", float(best[F(16)][1] and (F(16) / 2 * var(best[F(16)][1]) - ret(best[F(16)][1]))))
d16 = float(F(16) / 2 * var(best[F(16)][1]) - ret(best[F(16)][1])) - float(out[F(16)][1])
exact_diff = (F(16) / 2 * var(best[F(16)][1]) - ret(best[F(16)][1])) - out[F(16)][1]
print("E2 difference exact:", float(exact_diff), "rounded to 6 places:", "%.6f" % float(exact_diff), "(page: 0.572255)")
# E3 unrounded turnover at gamma=4
w4 = best[F(4)][1]
w0 = [F(1, 4)] * 4
tov = sum(abs(w4[i] - w0[i]) for i in range(4))
print("turnover gamma 4 exact:", float(tov), "(page: 0.558861; quoted exact 0.5588607)")
print("printed-weights turnover:", 0.139219 + 0.029430 + 0.140211 + 0.250000)
# Part C monotonicity, Part D perturbations
print("variance nonincreasing eq:", all(var(out[F(GAMMAS_NEXT)][0]) <= var(out[F(GAMMAS_NEXT_PREV)][0]) for GAMMAS_NEXT, GAMMAS_NEXT_PREV in [(2, 1), (4, 2), (8, 4), (16, 8)]))
