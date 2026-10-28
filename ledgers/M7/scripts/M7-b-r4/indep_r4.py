"""Independent recomputation for M7 slice b, round 4 (L04 to L06). Standard library only (fractions, math)."""

from fractions import Fraction as F
import math

out = []


def p(*a):
    out.append(" ".join(str(x) for x in a))


def solve(M, r):
    n = len(r)
    R = [list(M[i]) + [r[i]] for i in range(n)]
    for c in range(n):
        piv = next(i for i in range(c, n) if R[i][c] != 0)
        R[c], R[piv] = R[piv], R[c]
        pv = R[c][c]
        R[c] = [x / pv for x in R[c]]
        for i in range(n):
            if i != c and R[i][c] != 0:
                f = R[i][c]
                R[i] = [x - f * y for x, y in zip(R[i], R[c])]
    return [R[i][n] for i in range(n)]


def inv(M):
    n = len(M)
    cols = [solve(M, [F(int(i == j)) for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def mv(M, v):
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


# ---------- L04 ----------
S = [[F(2), F(1)], [F(1), F(2)]]
mu4 = [F(3, 2), F(1, 5)]
Si = inv(S)
p("L04 Sigma^{-1}", Si)
p("L04 g(0,0) =", -F(1, 2) * dot(mu4, mv(Si, mu4)))


def g4(lam, nu):
    r = [mu4[0] + lam[0] - nu, mu4[1] + lam[1] - nu]
    return -F(1, 2) * dot(r, mv(Si, r)) - nu


def f4(w):
    return F(1, 2) * dot(w, mv(S, w)) - dot(mu4, w)


duals = [((F(a, 10), F(b, 10)), F(n, 10)) for a in range(11) for b in range(11) for n in range(-10, 1)]
prims = [(F(k, 20), 1 - F(k, 20)) for k in range(21)]
print_count = sum(1 for (l, n) in duals for w in prims if g4(l, n) <= f4(w))
p("L04 weak duality pairs", print_count, "of", len(duals) * len(prims))
best = max(duals, key=lambda t: g4(*t))
p("L04 max dual", g4(*best), "at", best, "count attaining", sum(1 for t in duals if g4(*t) == g4(*best)))
pm = min(prims, key=f4)
p("L04 min primal", f4(pm), "at", pm, "grid gap", f4(pm) - g4(*best))
p("L04 g(0,-3/5)", g4((F(0), F(0)), F(-3, 5)), "g(0,-7/10)", g4((F(0), F(0)), F(-7, 10)), "g(0,-13/20)", g4((F(0), F(0)), F(-13, 20)))
p("L04 grid gap R3 (lambda=0):", f4(pm) - max(g4((F(0), F(0)), F(-k, 10)) for k in range(11)))
p("L04 KKT dual value", g4((F(0), F(3, 10)), F(-1, 2)), "primal at (1,0)", f4((F(1), F(0))))
p("L04 M3 check mu'Sigma^-1 mu", dot(mu4, mv(Si, mu4)))

# ---------- L05 ----------
Q = [[F(4), F(1), F(0)], [F(1), F(3), F(1)], [F(0), F(1), F(2)]]
c = [F(-1), F(0), F(2)]
A = [[F(1), F(1), F(1)], [F(0), F(1), F(-1)]]
b = [F(1), F(0)]
K = [Q[i] + [A[k][i] for k in range(2)] for i in range(3)] + [A[k] + [F(0), F(0)] for k in range(2)]
sol = solve(K, [-x for x in c] + b)
x, lam = sol[:3], sol[3:]
p("L05 x", x, "lambda", lam)
f5 = lambda y: F(1, 2) * dot(y, mv(Q, y)) + dot(c, y)
p("L05 objective", f5(x), float(f5(x)))
v = [F(-2), F(1), F(1)]
p("L05 v'Qv", dot(v, mv(Q, v)), "Qv", mv(Q, v))
p("L05 Av", [dot(A[k], v) for k in range(2)])
p("L05 remark 2.4 identity at x=0:", all(F(1, 2) * dot(v, mv(Q, v)) * t * t == f5([x[i] + t * v[i] for i in range(3)]) - f5(x) for t in [F(k, 4) for k in range(-8, 9)]))
# leading minors (Sylvester) for Q
def det(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    return sum((-1) ** j * M[0][j] * det([row[:j] + row[j + 1:] for row in M[1:]]) for j in range(n))
p("L05 leading minors Q", [det([row[:k] for row in Q[:k]]) for k in range(1, 4)])
p("L05 det K", det(K))
# Part B
QB = [[F(2), F(1)], [F(1), F(2)]]
cB = [F(-3), F(1)]
fB = lambda y: F(1, 2) * dot(y, mv(QB, y)) + dot(cB, y)
p("L05 part B f(3/2,0)", fB([F(3, 2), F(0)]))
grid = [F(k, 16) for k in range(33)]
vals = [fB([a, bb]) for a in grid for bb in grid]
p("L05 grid below -9/4:", sum(1 for t in vals if t < F(-9, 4)), "points", len(vals), "min==-9/4", min(vals) == F(-9, 4))
# Example 3.6 KKT check
xb = [F(3, 2), F(0)]
gr = [dot(QB[i], xb) + cB[i] for i in range(2)]
p("L05 Ex3.6 grad", gr, "mu=(0,5/2)")
# Remark 2.4 completed square identity
ok = all(
    (2 * a + F(1, 2) * bb) ** 2 + F(11, 4) * (bb + F(4, 11) * cc) ** 2 + F(18, 11) * cc * cc
    == 4 * a * a + 3 * bb * bb + 2 * cc * cc + 2 * a * bb + 2 * bb * cc
    for a in [F(k, 3) for k in range(-3, 4)] for bb in [F(k, 5) for k in range(-3, 4)] for cc in [F(k, 7) for k in range(-3, 4)]
)
p("L05 completed square identity on sample", ok)
p("L05 R3 two-asset", [F(54, 100), F(46, 100)], "w-r", [F(54, 100) - F(1, 10), F(46, 100) - F(2, 100)])

# ---------- L06 ----------
M = None


class Lcg:
    def __init__(self, s):
        self.s = s

    def draw(self, m):
        self.s = (1103515245 * self.s + 12345) % 2**31
        return self.s % m


g = Lcg(2026)
Mm = [[F(g.draw(7) - 3) for _ in range(4)] for _ in range(4)]
mu6 = [F(g.draw(13) + 2, 100) for _ in range(4)]
Sig = [[sum(Mm[k][i] * Mm[k][j] for k in range(4)) / 16 + (F(1, 10) if i == j else 0) for j in range(4)] for i in range(4)]
p("L06 M", [[int(z) for z in r] for r in Mm])
p("L06 mu", mu6, [float(z) for z in mu6])
p("L06 Sigma diag", [Sig[i][i] for i in range(4)])
ones = [F(1)] * 4


def eq_w(gam):
    k = [[gam * Sig[i][j] for j in range(4)] + [F(1)] for i in range(4)] + [[F(1)] * 4 + [F(0)]]
    s = solve(k, mu6 + [F(1)])
    return s[:4], s[4]


def obj(gam, w):
    return gam / 2 * dot(w, mv(Sig, w)) - dot(mu6, w)


def nn_w(gam):
    best = None
    kept = []
    import itertools
    for mask in itertools.product((0, 1), repeat=4):
        zeros = [i for i in range(4) if mask[i]]
        free = [i for i in range(4) if not mask[i]]
        if not free:
            continue
        sub = [[gam * Sig[i][j] for j in free] + [F(1)] for i in free] + [[F(1)] * len(free) + [F(0)]]
        s = solve(sub, [mu6[i] for i in free] + [F(1)])
        w = [F(0)] * 4
        for pos, val in zip(free, s[:len(free)]):
            w[pos] = val
        lamb = s[len(free)]
        nu = [gam * mv(Sig, w)[i] - mu6[i] + lamb for i in range(4)]
        if all(z >= 0 for z in w) and all(nu[i] >= 0 for i in zeros):
            kept.append((zeros, w))
    return kept


for gam in [F(1), F(2), F(4), F(8), F(16)]:
    w, lamb = eq_w(gam)
    ret = dot(mu6, w)
    var = dot(w, mv(Sig, w))
    o = obj(gam, w)
    p("L06 eq gamma", gam, "ret", float(ret), "var", float(var), "obj", float(o), "budget", sum(w) == 1)
    p("   weights", [float(z) for z in w], "lambda", float(lamb))
    kept = nn_w(gam)
    p("   nn kept", [(z, [float(q) for q in ww]) for z, ww in kept], "count", len(kept))
    for z, ww in kept:
        p("   nn ret", float(dot(mu6, ww)), "var", float(dot(ww, mv(Sig, ww))), "obj", float(obj(gam, ww)), "obj-eq", float(obj(gam, ww) - o))
        if gam == 16:
            p("   E2 exact diff obj_nn - obj_eq at 16:", repr(float(obj(gam, ww) - o)))
    if gam == 4:
        w0 = [F(1, 4)] * 4
        ww = kept[0][1]
        t_turn = sum(abs(ww[i] - w0[i]) for i in range(4))
        p("L06 E3 unrounded turnover gamma 4 (exact):", float(t_turn), repr(float(t_turn)))
        p("   deviations", [float(ww[i] - w0[i]) for i in range(4)])

# closed form check gamma 1
w1, _ = eq_w(F(1))
a = solve(Sig, mu6)
bvec = solve(Sig, ones)
lam_cf = (sum(a) - 1) / sum(bvec)
p("L06 closed form sum(1'b)", sum(bvec), "lambda cf", float(lam_cf))
p("L06 R2 check: (0.54,0.46) nearest", [F(54, 100) - F(1, 10), F(46, 100) - F(2, 100)])
p("L06 P3-style check mu/gamma etc skip")
# M1 check
p("L06 M1 w", [F(1, 20) + F(37, 80), F(1, 40) + F(37, 80)], "sum", F(1, 20) + F(37, 80) + F(1, 40) + F(37, 80))
p("L06 M2 f1", F(1, 2) * 1 - F(3, 40))
print("\n".join(out))
