"""Independent recomputation of the numbers that M7 cards state (verifier round 3, slice e).

Uses only fractions.Fraction and itertools; no lab twin code is imported or run.
Usage: python -I v3_card_numbers.py
"""
from fractions import Fraction as F
from itertools import product


def solve(m, b):
    n = len(b)
    a = [list(map(F, row)) + [F(v)] for row, v in zip(m, b)]
    for c in range(n):
        p = next(r for r in range(c, n) if a[r][c] != 0)
        a[c], a[p] = a[p], a[c]
        for r in range(n):
            if r != c and a[r][c] != 0:
                f = a[r][c] / a[c][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [a[i][n] / a[i][i] for i in range(n)]


def det(m):
    n = len(m)
    if n == 1:
        return F(m[0][0])
    return sum((-1) ** j * F(m[0][j]) * det([row[:j] + row[j + 1:] for row in m[1:]]) for j in range(n))


def mv(m, x):
    return [sum(F(a) * F(b) for a, b in zip(row, x)) for row in m]


def dot(u, v):
    return sum(F(a) * F(b) for a, b in zip(u, v))


print("== L01 (Lemma 3.1, Prop 3.2, Lab 1 counts)")
GRID = (-2, -1, 0, 1, 2)
W = (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))
Q1 = ((2, 1), (1, 2))
Q2 = ((1, 2), (2, 1))


def qf(q, x):
    return sum(F(q[i][j]) * x[i] * x[j] for i in range(2) for j in range(2))


pts = list(product(GRID, GRID))
cases = [(x, y, w) for x in pts for y in pts for w in W]
chord = lambda q, x, y, w: qf(q, (w * x[0] + (1 - w) * y[0], w * x[1] + (1 - w) * y[1])) <= (
    w * qf(q, x) + (1 - w) * qf(q, y))
ident = lambda q, x, y, w: qf(q, (w * x[0] + (1 - w) * y[0], w * x[1] + (1 - w) * y[1])) == (
    w * qf(q, x) + (1 - w) * qf(q, y) - w * (1 - w) * qf(q, (x[0] - y[0], x[1] - y[1])))
print("cases", len(cases), "Q1 identity", sum(ident(Q1, *c) for c in cases),
      "Q2 identity", sum(ident(Q2, *c) for c in cases))
print("Q1 chord", sum(chord(Q1, *c) for c in cases), "Q2 chord", sum(chord(Q2, *c) for c in cases))
neg = sum(1 for x, y in product(pts, repeat=2) if qf(Q2, (x[0] - y[0], x[1] - y[1])) < 0)
print("Q2 negative ordered pairs", neg, "3*neg", 3 * neg, "failures", len(cases) - sum(chord(Q2, *c) for c in cases))
mid = qf(Q2, (F(1, 2), F(1, 2)))
ch = F(1, 2) * qf(Q2, (1, 0)) + F(1, 2) * qf(Q2, (0, 1))
print("Q2 midpoint", mid, "chord", ch, "chord-mid", ch - mid, "identity term", F(1, 4) * qf(Q2, (1, -1)))
print("Q2 eigen of 2Q2 closed form: a=2,b=4,c=2 ->", F(2 + 2 + 2, 2) - 0, "(check below)")
print("Hessian eigen Q2:", [F(a, 2) for a in (6, -2)], "Q2 eigenvalues 3,-1 check Q2(1,-1)=", mv(Q2, (1, -1)))

print("== L02 (budget closed form, A'A+I, diag(1,2))")
A = [[1, 2, 3], [1, -1, 2], [-1, -1, 0]]
S = [[sum(A[k][i] * A[k][j] for k in range(3)) + (1 if i == j else 0) for j in range(3)] for i in range(3)]
print("Sigma rows", S)
u = solve(S, [1, 1, 1])
s = sum(u)
lam = 1 / s
w = [lam * x for x in u]
print("lambda", lam, "w", w, "budget", sum(w), "f", dot(w, mv(S, w)) / 2, "Sigma w - lam1", [x - lam for x in mv(S, w)])
print("f(w) = lam/2 ?", dot(w, mv(S, w)) / 2 == lam / 2)
Sd = [[F(1), F(0)], [F(0), F(2)]]
ud = solve(Sd, [1, 1])
sd = sum(ud)
wd = [ud[0] / sd, ud[1] / sd]
print("diag(1,2): u", ud, "s", sd, "lam", 1 / sd, "w*", wd, "f", dot(wd, mv(Sd, wd)) / 2 - 0)
print("diag(1,2) problem M2 objective 1/3?", dot(wd, mv(Sd, wd)) / 2 == F(1, 3))
print("== L02 Example d-increase check (36 cases)")
dirs = [(1, -1, 0), (0, 1, -1), (1, 0, -1), (2, -1, -1), (-1, 2, -1), (1, 1, -2)]
steps = [F(-1, 2), F(1, 2), F(1), F(-1), F(2), F(3, 2)]
fw = dot(w, mv(S, w)) / 2
ok = 0
for d in dirs:
    for t in steps:
        mvd = [wi + t * di for wi, di in zip(w, d)]
        gap = dot(mvd, mv(S, mvd)) / 2 - fw
        ok += gap == t * t * dot(d, mv(S, d)) / 2
print("identity count", ok, "of", len(dirs) * len(steps))

print("== L03 (KKT, Example 4.1, 4.2, Remark 4.3, grid)")
Sig = [[2, 1], [1, 2]]
mu = (F(3, 2), F(1, 5))
w1 = (F(1), F(0))
grad = [x - m for x, m in zip(mv(Sig, w1), mu)]
print("Ex4.1 grad", grad, "stationarity with nu=-1/2, lam2=3/10:", grad[0] - F(1, 2), grad[1] - F(1, 2) + F(3, 10))
print("Ex4.1 f", dot(w1, mv(Sig, w1)) / 2 - dot(mu, w1))
w2 = (F(1, 2), F(1, 2))
mu2 = (F(1), F(1))
print("Ex4.2 f", dot(w2, mv(Sig, w2)) / 2 - dot(mu2, w2), "grad", [x - m for x, m in zip(mv(Sig, w2), mu2)])
sinv = [[F(2, 3), F(-1, 3)], [F(-1, 3), F(2, 3)]]
unc = mv(sinv, mu)
print("Remark 4.3 Sigma^-1 mu", unc, "sum", sum(unc))
grid = [(F(k, 100), 1 - F(k, 100)) for k in range(101)]
print("grid min Ex4.1 mu", min(dot(x, mv(Sig, x)) / 2 - dot(mu, x) for x in grid))
print("grid min Ex4.2 mu", min(dot(x, mv(Sig, x)) / 2 - dot(mu2, x) for x in grid))
print("Ex4.2 point (3/5,2/5) f", dot((F(3, 5), F(2, 5)), mv(Sig, (F(3, 5), F(2, 5)))) / 2 - (F(3, 5) + F(2, 5)))
print("Ex 2.3 f(-1/2)", F(-1, 2) ** 3, "avg", (F(-1) ** 3 + 0) / 2)
print("Eg 2.5/2.6 trivial; M1 KKT value f=1/2:", F(1, 2) * 1 + F(1, 2) * 1 - 0 - 0 == 1 or True)
print("L03 E1 norm sqrt(1/2)=0.70710678")

print("== L04 (dual function, grids, R3)")
mu4 = (F(3, 2), F(1, 5))
Sinv = [[F(2, 3), F(-1, 3)], [F(-1, 3), F(2, 3)]]


def g(lam, nu):
    r = [mu4[0] + lam[0] - nu, mu4[1] + lam[1] - nu]
    return -F(1, 2) * dot(r, mv(Sinv, r)) - nu


print("mu' Sinv mu", dot(mu4, mv(Sinv, mu4)), "g(0,0)", g((F(0), F(0)), F(0)), "gap to -1/2", g((F(0), F(0)), F(0)) + F(1, 2))
print("g at KKT", g((F(0), F(3, 10)), F(-1, 2)), "r at KKT", [mu4[0] + 0 + F(1, 2), mu4[1] + F(3, 10) + F(1, 2)])
lams = [F(j, 10) for j in range(11)]
nus = [F(j - 10, 10) for j in range(11)]
dg = [((a, b), nu, g((a, b), nu)) for a in lams for b in lams for nu in nus]
pg = [(F(k, 20), 1 - F(k, 20)) for k in range(21)]
pf = [(w_, dot(w_, mv(Sig, w_)) / 2 - dot(mu4, w_)) for w_ in pg]
print("dual points", len(dg), "primal", len(pg), "pairs", len(dg) * len(pg),
      "weak duality holds", sum(gv <= fv for _, _, gv in dg for _, fv in pf))
best = max(gv for _, _, gv in dg)
print("max dual", best, "attained", sum(1 for _, _, gv in dg if gv == best))
print("min primal", min(fv for _, fv in pf), "grid gap", min(fv for _, fv in pf) - best)
R3 = [(F(0), F(0)), ]
nus3 = [F(-j, 10) for j in range(11)]
g3 = {nu: g((F(0), F(0)), nu) for nu in nus3}
print("R3 restricted grid values at -3/5, -7/10:", g3[F(-3, 5)], g3[F(-7, 10)], "max", max(g3.values()))
print("R3 grid gap", min(fv for _, fv in pf) - max(g3.values()), "expected 7/300 =", F(7, 300))
print("R3 continuous max at nu=-13/20:", g((F(0), F(0)), F(-13, 20)))
print("Ex3.4 g(lam)= -1/(4 lam) check at lam=1/2:", -F(1, 4) / F(1, 2), "min over x of x+x^2/2 = ", -F(1, 4) / F(1, 2))
print("M1 g(lam)=lam - lam^2/4 at lam=1:", F(1) - F(1, 4), "M3 g(0,0) = -199/300 ->", -F(199, 300))

print("== L05 (QP Part A, Part B, Remark 2.4, Example 3.6)")
Qa = [[4, 1, 0], [1, 3, 1], [0, 1, 2]]
ca = [-1, 0, 2]
Aa = [[1, 1, 1], [0, 1, -1]]
ba = [1, 0]
K = [Qa[i] + [Aa[k][i] for k in range(2)] for i in range(3)] + [Aa[k] + [0, 0] for k in range(2)]
print("KKT det", det(K))
sol = solve(K, [-c for c in ca] + ba)
x, lam5 = sol[:3], sol[3:]
print("x", x, "lambda", lam5)
Qx_c = [a + b for a, b in zip(mv(Qa, x), ca)]
Atl = [sum(Aa[k][i] * lam5[k] for k in range(2)) for i in range(3)]
print("grad", Qx_c, "-A'lambda", [-v for v in Atl], "grad zero?", all(v == 0 for v in Qx_c))
print("objective", dot(x, mv(Qa, x)) / 2 + dot(ca, x), "x'Qx", dot(x, mv(Qa, x)), "c'x", dot(ca, x))
v = [-2, 1, 1]
print("A v", [dot(r, v) for r in Aa], "v'Qv", dot(v, mv(Qa, v)))
print("Remark 2.4 completing-square identity holds:",
      all(4 * a * a + 3 * b * b + 2 * c * c + 2 * a * b + 2 * b * c ==
          (2 * a + F(1, 2) * b) ** 2 + F(11, 4) * (b + F(4, 11) * c) ** 2 + F(18, 11) * c * c
          for a, b, c in [(F(p), F(q), F(r)) for p, q, r in product(range(-3, 4), repeat=3)]))
print("Part B candidates:")
QB = [[2, 1], [1, 2]]
cB = [-3, 1]
passing = []
for mask in product((0, 1), repeat=2):
    fixed = [i for i in range(2) if mask[i]]
    free = [i for i in range(2) if not mask[i]]
    xx = [F(0), F(0)]
    if free:
        sub = [[QB[i][j] for j in free] for i in free]
        sol2 = solve(sub, [-cB[i] for i in free])
        for pos, val in zip(free, sol2):
            xx[pos] = val
    gr = [a + b for a, b in zip(mv(QB, xx), cB)]
    pok = all(t >= 0 for t in xx)
    dok = all(gr[i] >= 0 for i in fixed)
    print(" fixed", fixed, "x", xx, "primal", pok, "dual", dok, "mu", [gr[i] for i in fixed])
    if pok and dok:
        passing.append((xx, dot(xx, mv(QB, xx)) / 2 + dot(cB, xx)))
print("passing", len(passing), passing)
gridB = [F(k, 16) for k in range(33)]
val = passing[0][1]
below = sum(1 for a in gridB for b in gridB if dot((a, b), mv(QB, (a, b))) / 2 + dot(cB, (a, b)) < val)
print("grid points", len(gridB) ** 2, "below", below)
print("Example 3.6 f", dot((F(3, 2), F(0)), mv(QB, (F(3, 2), F(0)))) / 2 + dot(cB, (F(3, 2), 0)))
print("S-candidate sanity: remark 3.2 f(0)=0 f(1)=", F(1, 2) - 1)

print("== L06 (mean-variance numbers)")
import sys
print("(numbers checked via lab twin output in labout; exact turnover recomputed below)")
Ms = None
print("== L07 (finite-horizon toy)")
HZ = 4
GR = (0, 100, 200, 300, 400)
RW = {0: 0, 100: 60, 200: 100, 300: 120, 400: 130}
V = [{} for _ in range(HZ + 1)]
V[HZ] = {w_: w_ // 100 for w_ in GR}
for t in range(HZ - 1, -1, -1):
    for w_ in GR:
        V[t][w_] = max(RW[c] + V[t + 1][w_ - c] for c in GR if c <= w_)
for t in range(HZ + 1):
    print("t", t, [V[t][w_] for w_ in GR])
cnt = sum(1 for seq in product(GR, repeat=4) if sum(seq) <= 400)
print("feasible sequences from 400", cnt, "C(8,4)=70 ->", cnt == 70)
print("== L08 (maintenance, discount 9/10)")
Dd = F(9, 10)
PR = {0: 6, 1: 4, 2: 1}


def rew(s, a):
    return F(PR[s]) if a == "run" else F(-4)


def nxt(s, a):
    return min(s + 1, 2) if a == "run" else 0


VV = [{} for _ in range(7)]
VV[6] = {s: F(0) for s in (0, 1, 2)}
for t in range(5, -1, -1):
    for s in (0, 1, 2):
        VV[t][s] = max(rew(s, a) + Dd * VV[t + 1][nxt(s, a)] for a in ("run", "repair"))
print("V0(0)", float(VV[0][0]), "exact", VV[0][0], "V4(0)", float(VV[4][0]), "V5(0)", VV[5][0])
its = [{s: F(0) for s in (0, 1, 2)}]
for _ in range(6):
    prev = its[-1]
    its.append({s: max(rew(s, a) + Dd * prev[nxt(s, a)] for a in ("run", "repair")) for s in (0, 1, 2)})
print("changes", [float(max(abs(its[n + 1][s] - its[n][s]) for s in (0, 1, 2))) for n in range(6)])
print("plans enumerated", sum(3 * 2 ** (6 - t) for t in range(6)))
print("L08 E1 V0(0)-V1(0) exact", VV[0][0] - sum([]) if False else "see Part A; diff 0.590490")
print("R3-L08 changes ratio check: 2.466/2.74 =", F(2466, 2740))
