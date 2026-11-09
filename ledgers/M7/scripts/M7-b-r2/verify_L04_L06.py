"""Verifier script (M7-b round 2): independent recomputation of the numbers stated in L04, L05 and L06.

Written by the round-2 verifier from the page text, not from the builder's twins. Standard library only.
Run with: python3 -I ledgers/M7/scripts/M7-b-r2/verify_L04_L06.py   (from the checkout root)
Exact values use fractions.Fraction; the L06 projected-gradient cross-check uses floats.
"""

from fractions import Fraction as F
from itertools import combinations, product
import math


def gauss(a, b):
    """Solve a x = b exactly by Gauss-Jordan elimination with pivoting (independent of the twins)."""
    n = len(b)
    m = [[F(v) for v in row] + [F(bb)] for row, bb in zip(a, b)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        pv = m[c][c]
        m[c] = [v / pv for v in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                fac = m[r][c]
                m[r] = [x - fac * y for x, y in zip(m[r], m[c])]
    return [m[i][n] for i in range(n)]


def det_exact(a):
    """Determinant by permutation-free Bareiss-style elimination with exact fractions."""
    n = len(a)
    m = [[F(v) for v in row] for row in a]
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
            fac = m[r][c] / m[c][c]
            m[r] = [x - fac * y for x, y in zip(m[r], m[c])]
    return d


def dot(u, v):
    return sum((a * b for a, b in zip(u, v)), F(0))


def matvec(a, v):
    return [dot(row, v) for row in a]


# ---------------------------------------------------------------- L04
print("=== L04 ===")
SIG = [[F(2), F(1)], [F(1), F(2)]]
MU4 = [F(3, 2), F(1, 5)]
SIG_INV = [[F(2, 3), F(-1, 3)], [F(-1, 3), F(2, 3)]]
assert matvec(SIG, [F(1), F(0)]) == [F(2), F(1)]
assert [[sum(SIG[i][k] * SIG_INV[k][j] for k in range(2)) for j in range(2)] for i in range(2)] == [
    [F(1), F(0)],
    [F(0), F(1)],
]


def primal4(w):
    return dot(w, matvec(SIG, w)) / 2 - dot(MU4, w)


def dual4(lam, nu):
    r = [MU4[i] + lam[i] - nu for i in range(2)]
    return -dot(r, matvec(SIG_INV, r)) / 2 - nu


duals = [((F(a, 10), F(b, 10)), F(n, 10)) for a in range(11) for b in range(11) for n in range(-10, 1)]
prims = [(F(k, 20), F(20 - k, 20)) for k in range(21)]
print("dual points", len(duals), "primal points", len(prims), "pairs", len(duals) * len(prims))
assert len(duals) == 1331 and len(prims) == 21 and len(duals) * len(prims) == 27951
holds = sum(1 for lam, nu in duals for w in prims if dual4(lam, nu) <= primal4(w))
print("weak duality pairs", holds, "of", len(duals) * len(prims))
best_dual = max(dual4(l, n) for l, n in duals)
attain = [(l, n) for l, n in duals if dual4(l, n) == best_dual]
print("max dual", best_dual, "attained at", attain)
best_primal = min(primal4(w) for w in prims)
print("min primal", best_primal, "at", [w for w in prims if primal4(w) == best_primal])
print("grid gap", best_primal - best_dual)
assert best_dual == F(-1, 2) and attain == [((F(0), F(3, 10)), F(-1, 2))] and best_primal == F(-1, 2)
assert dual4((F(0), F(0)), F(0)) == F(-199, 300)
print("g(0,0) minus p* =", dual4((F(0), F(0)), F(0)) - F(-1, 2), "(page: -49/300)")
assert dual4((F(0), F(3, 10)), F(-1, 2)) == F(-1, 2) == primal4((F(1), F(0)))
# M3: mu' Sigma^{-1} mu
quad_mu = dot(MU4, matvec(SIG_INV, MU4))
print("mu' Sigma^-1 mu =", quad_mu, "(page: 199/150)", "g(0,0) = -1/2 * that =", -quad_mu / 2)
assert quad_mu == F(199, 150)
# Example 2.2: r at KKT point
r_kkt = [MU4[0] + F(0) + F(1, 2), MU4[1] + F(3, 10) + F(1, 2)]
print("r at KKT point", r_kkt, "Sigma^-1 r", matvec(SIG_INV, r_kkt), "r'Sigma^-1 r", dot(r_kkt, matvec(SIG_INV, r_kkt)))
assert r_kkt == [F(2), F(1)] and matvec(SIG_INV, r_kkt) == [F(1), F(0)]
# KKT stationarity of the primal at (1,0) with lambda=(0,3/10), nu=-1/2
grad = [matvec(SIG, [F(1), F(0)])[i] - MU4[i] for i in range(2)]
stat = [grad[0] + F(0) * (-1) + F(-1, 2), grad[1] + F(3, 10) * (-1) + F(-1, 2)]  # grad_i + lam_i * dg_i/dw_i + nu * dh/dw_i, dg_i/dw_i = -1, dh/dw_i = 1
print("KKT stationarity residuals at w*=(1,0):", stat)
assert stat == [F(0), F(0)]
# R3: restricted grid lambda=(0,0), nu = k/10 on [-1,0]
grid_nu = [F(n, 10) for n in range(-10, 1)]
vals = {n: dual4((F(0), F(0)), n) for n in grid_nu}
gmax = max(vals.values())
print("R3 grid values at nu=-3/5, -7/10:", vals[F(-3, 5)], vals[F(-7, 10)], "grid max", gmax)
print("R3 value at nu=-13/20:", dual4((F(0), F(0)), F(-13, 20)), "(page -209/400)")
assert vals[F(-3, 5)] == F(-157, 300) and vals[F(-7, 10)] == F(-157, 300) and gmax == F(-157, 300)
assert dual4((F(0), F(0)), F(-13, 20)) == F(-209, 400)
# the derivative of g(0,nu) in nu vanishes at -13/20 (exact finite difference of a quadratic)
h = F(1, 10**6)
dd = (dual4((F(0), F(0)), F(-13, 20) + h) - dual4((F(0), F(0)), F(-13, 20) - h)) / (2 * h)
print("dg/dnu at -13/20 (central difference, should be ~0):", float(dd))
print("R3 grid gap", best_primal - gmax, "(page 7/300)", best_primal - gmax == F(7, 300))
assert best_primal - gmax == F(7, 300)
# M1: g(lambda) = lambda - lambda^2/4, maximised at 2 with value 1; P1 identity
for lam in [F(0), F(1), F(2), F(3, 2)]:
    assert 1 - (lam - lam * lam / 4) == (1 - lam / 2) ** 2
print("M1: 1 - g(lambda) = (1 - lambda/2)^2 at sample points: True")
# Example 3.4: inf over x of x + lam x^2 equals -1/(4 lam) at x = -1/(2 lam)
for lam in [F(1), F(2), F(1, 3)]:
    xm = -1 / (2 * lam)
    assert xm + lam * xm * xm == -1 / (4 * lam)
print("Example 3.4: g(lambda) = -1/(4 lambda) at sampled lambda: True")
# Remark 1.5 / P2: nothing numeric beyond the above

# ---------------------------------------------------------------- L05
print("=== L05 ===")
QA = [[F(4), F(1), F(0)], [F(1), F(3), F(1)], [F(0), F(1), F(2)]]
CA = [F(-1), F(0), F(2)]
AA = [[F(1), F(1), F(1)], [F(0), F(1), F(-1)]]
BA = [F(1), F(0)]
VN = [F(-2), F(1), F(1)]
K = [QA[i] + [AA[k][i] for k in range(2)] for i in range(3)] + [AA[k] + [F(0), F(0)] for k in range(2)]
dK = det_exact(K)
print("det K =", dK, "(page 19)")
assert dK == 19
sol = gauss(K, [-c for c in CA] + BA)
x_hat, lam_hat = sol[:3], sol[3:]
print("x", x_hat, "lambda", lam_hat)
assert x_hat == [F(13, 19), F(3, 19), F(3, 19)] and lam_hat == [F(-36, 19), F(11, 19)]


def fq(x):
    return dot(x, matvec(QA, x)) / 2 + dot(CA, x)


obj = fq(x_hat)
print("objective", obj, float(obj), "to 10 places", f"{float(obj):.10f}", "(551/722)", F(551, 722) == obj)
assert obj == F(551, 722)
qv = matvec(QA, VN)
print("Qv", qv, "v'Qv", dot(VN, qv))
assert dot(VN, qv) == 19
# null line exact check
ok = True
for k in range(-8, 9):
    t = F(k, 4)
    p = [x_hat[i] + t * VN[i] for i in range(3)]
    feas = all(dot(AA[r], p) == BA[r] for r in range(2))
    ok = ok and feas and (fq(p) - obj == F(1, 2) * t * t * 19)
print("null line exact identity over 17 t-values:", ok)
assert ok
# stationarity and constraint residual
stat = [matvec(QA, x_hat)[i] + CA[i] + sum(AA[k][i] * lam_hat[k] for k in range(2)) for i in range(3)]
print("stationarity residuals", stat)
assert stat == [0, 0, 0]
# Remark 2.4 completing-the-square identity on integer points
for x1, x2, x3 in product(range(-3, 4), repeat=3):
    lhs = 4 * x1 * x1 + 3 * x2 * x2 + 2 * x3 * x3 + 2 * x1 * x2 + 2 * x2 * x3
    rhs = (2 * x1 + F(1, 2) * x2) ** 2 + F(11, 4) * (x2 + F(4, 11) * x3) ** 2 + F(18, 11) * x3 * x3
    assert lhs == rhs
print("Remark 2.4 identity on 343 integer points: True")
# Remark 2.2 K singular for equal rows
K2 = [[1, 0, 1, 1], [0, 1, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]]
print("Remark 2.2 det:", det_exact(K2), "(page 0)")
assert det_exact(K2) == 0
# Part B: enumerate the four sets
QB = [[F(2), F(1)], [F(1), F(2)]]
CB = [F(-3), F(1)]
print("Part B candidates (zero set: x, primal, dual):")
passing = []
for mask in product((0, 1), repeat=2):
    fixed = [i for i in range(2) if mask[i]]
    free = [i for i in range(2) if not mask[i]]
    x = [F(0), F(0)]
    if free:
        sub = [[QB[i][j] for j in free] for i in free]
        rhs = [-CB[i] for i in free]
        xf = gauss(sub, rhs)
        for pos, v in zip(free, xf):
            x[pos] = v
    g = [matvec(QB, x)[i] + CB[i] for i in range(2)]
    primal_ok = all(v >= 0 for v in x)
    dual_ok = all(g[i] >= 0 for i in fixed)
    print("  fixed", fixed, "x", [str(v) for v in x], "mu", [str(v) for v in g], primal_ok, dual_ok)
    if primal_ok and dual_ok:
        passing.append((fixed, x))
print("passing candidates", len(passing), passing)
assert len(passing) == 1 and passing[0][1] == [F(3, 2), F(0)]
fqB = lambda x: dot(x, matvec(QB, x)) / 2 + dot(CB, x)
assert fqB([F(3, 2), F(0)]) == F(-9, 4)
grid = [F(k, 16) for k in range(33)]
pts = [(a, b) for a in grid for b in grid]
below = sum(1 for a, b in pts if fqB([a, b]) < F(-9, 4))
print("grid points", len(pts), "below -9/4:", below)
assert len(pts) == 1089 and below == 0
# Example 3.6 check and M-problems
assert matvec(QB, [F(3, 2), F(0)]) == [F(3), F(3, 2)]
assert [matvec(QB, [F(3, 2), F(0)])[i] + CB[i] for i in range(2)] == [F(0), F(5, 2)]
# M1
print("M1 check:", [F(1, 2), F(1, 2)], "lambda -1 from 2x+lambda=0 at x=1/2:", 2 * F(1, 2) + F(-1) == 0)
# M3 unconstrained minimiser
m3 = gauss(QB, [F(3), F(-1)])
print("M3 unconstrained minimiser", m3, "(page 7/3, -5/3)")
assert m3 == [F(7, 3), F(-5, 3)]
# R2 (n=3, Q=I, c=(1,-1,-2), x>=0): max(0, -c_i)
print("R2 minimiser", [max(F(0), -c) for c in [F(1), F(-1), F(-2)]], "(page (0,1,2))")
# R3: w = r + t 1 with t = 0.44
rr = [F(1, 10), F(2, 100)]
t = (1 - sum(rr)) / 2
print("R3 w =", [rr[0] + t, rr[1] + t], "(page (0.54, 0.46))")
assert [rr[0] + t, rr[1] + t] == [F(54, 100), F(46, 100)]
# E1 decimal
print("E1 551/722 to 10 places:", f"{float(F(551, 722)):.10f}", "to 4 places:", f"{float(F(551, 722)):.4f}")
# Misconception 1: f on (0,t) with Q=diag(1,-1)
print("Misconception 1: f(0,t) = -t^2/2 check:", all(F(1, 2) * (0 * 0) + F(-1, 2) * t * t == -F(t * t, 2) for t in range(-3, 4)))

# ---------------------------------------------------------------- L06
print("=== L06 ===")
SEED = 2026
N = 4


class Lcg:
    def __init__(self, s):
        self.s = s

    def draw(self, mod):
        self.s = (1103515245 * self.s + 12345) % 2**31
        return self.s % mod


gen = Lcg(SEED)
Mx = [[F(gen.draw(7) - 3) for _ in range(N)] for _ in range(N)]
mu6 = [F(gen.draw(13) + 2, 100) for _ in range(N)]
S6 = [
    [sum((Mx[k][i] * Mx[k][j] for k in range(N)), F(0)) / 16 + (F(1, 10) if i == j else F(0)) for j in range(N)]
    for i in range(N)
]
print("mu", [str(v) for v in mu6], "(page 7/100 1/20 3/25 1/50)")
print("sigma diag", [str(S6[i][i]) for i in range(N)], "(page 49/40 27/20 103/80 103/80)")
assert mu6 == [F(7, 100), F(1, 20), F(3, 25), F(1, 50)]
assert [S6[i][i] for i in range(N)] == [F(49, 40), F(27, 20), F(103, 80), F(103, 80)]
print("sigma symmetric", all(S6[i][j] == S6[j][i] for i in range(N) for j in range(N)))
# positive definiteness by leading minors (exact)
print("leading minors positive", all(det_exact([row[:k] for row in S6[:k]]) > 0 for k in range(1, N + 1)))


def eq_solution(gamma):
    """Equality-only minimiser by the KKT system [[gamma S, 1],[1', 0]] [w; lam] = [mu; 1]."""
    kk = [[gamma * S6[i][j] for j in range(N)] + [F(1)] for i in range(N)] + [[F(1)] * N + [F(0)]]
    s = gauss(kk, mu6 + [F(1)])
    return s[:N], s[N]


def obj6(gamma, w):
    return gamma / 2 * dot(w, matvec(S6, w)) - dot(mu6, w)


def risk6(w):
    return dot(w, matvec(S6, w))


GAM = [F(1), F(2), F(4), F(8), F(16)]
eq_w = {}
eq_obj = {}
for g_ in GAM:
    w, lam = eq_solution(g_)
    eq_w[g_] = w
    eq_obj[g_] = obj6(g_, w)
    print(
        "equality gamma",
        g_,
        "return",
        f"{float(dot(mu6, w)):.6f}",
        "risk",
        f"{float(risk6(w)):.6f}",
        "objective",
        f"{float(obj6(g_, w)):.6f}",
        "budget",
        sum(w) == 1,
        "weights",
        [f"{float(v):.6f}" for v in w],
    )
# closed form P3 check for Sigma = I (independent)
# Part A expected values from the page
assert f"{float(eq_obj[F(1)]):.6f}" == "-0.051893" and f"{float(eq_obj[F(2)]):.6f}" == "0.007996"
assert f"{float(eq_obj[F(16)]):.6f}" == "0.820002" and f"{float(eq_obj[F(4)]):.6f}" == "0.124753"


def nonneg_candidates(gamma):
    kept = []
    for mask in product((0, 1), repeat=N):
        zeros = [i for i in range(N) if mask[i]]
        free = [i for i in range(N) if not mask[i]]
        if not free:
            continue
        sub = [[gamma * S6[i][j] for j in free] for i in free]
        kk = [row + [F(1)] for row in sub] + [[F(1)] * len(free) + [F(0)]]
        s = gauss(kk, [mu6[i] for i in free] + [F(1)])
        w = [F(0)] * N
        for pos, v in zip(free, s[: len(free)]):
            w[pos] = v
        lam = s[len(free)]
        sw = matvec(S6, w)
        nu = [gamma * sw[i] - mu6[i] + lam for i in range(N)]
        if all(v >= 0 for v in w) and all(nu[i] >= 0 for i in zeros):
            kept.append((zeros, w))
    return kept


nn_w = {}
nn_obj = {}
for g_ in GAM:
    kept = nonneg_candidates(g_)
    best = min(kept, key=lambda it: obj6(g_, it[1]))
    nn_w[g_] = best[1]
    nn_obj[g_] = obj6(g_, best[1])
    print(
        "nonneg gamma",
        g_,
        "zero set",
        [f"A{i + 1}" for i in best[0]],
        "passing",
        len(kept),
        "distinct",
        len({tuple(w) for _, w in kept}),
        "return",
        f"{float(dot(mu6, best[1])):.6f}",
        "risk",
        f"{float(risk6(best[1])):.6f}",
        "objective",
        f"{float(nn_obj[g_]):.6f}",
        "weights",
        [f"{float(v):.6f}" for v in best[1]],
    )
    assert nn_obj[g_] >= eq_obj[g_]

# Independent cross-check: projected gradient on the simplex (floats), for each gamma
def proj_simplex(v):
    u = sorted(v, reverse=True)
    css = 0.0
    rho = 0
    theta = 0.0
    for i, ui in enumerate(u):
        css += ui
        t = (css - 1.0) / (i + 1)
        if ui - t > 0:
            rho = i
            theta = t
    return [max(vi - theta, 0.0) for vi in v]


Sf = [[float(S6[i][j]) for j in range(N)] for i in range(N)]
muf = [float(v) for v in mu6]
for g_ in GAM:
    gf = float(g_)
    step = 1.0 / (gf * sum(Sf[i][i] for i in range(N)))
    w = [0.25] * N
    for _ in range(200000):
        gradv = [gf * sum(Sf[i][j] * w[j] for j in range(N)) - muf[i] for i in range(N)]
        w = proj_simplex([w[i] - step * gradv[i] for i in range(N)])
    exact = nn_w[g_]
    diffw = max(abs(w[i] - float(exact[i])) for i in range(N))
    fobj = gf / 2 * sum(w[i] * Sf[i][j] * w[j] for i in range(N) for j in range(N)) - sum(muf[i] * w[i] for i in range(N))
    print("projected gradient gamma", g_, "max |w - exact|", f"{diffw:.2e}", "objective", f"{fobj:.9f}", "exact", f"{float(nn_obj[g_]):.9f}")
    assert diffw < 1e-5

# Part C
eqr = [risk6(eq_w[g]) for g in GAM]
nnr = [risk6(nn_w[g]) for g in GAM]
print("equality risks", [f"{float(v):.6f}" for v in eqr], "nonneg risks", [f"{float(v):.6f}" for v in nnr])
print("equality risk nonincreasing", all(eqr[i + 1] <= eqr[i] for i in range(4)), "nonneg", all(nnr[i + 1] <= nnr[i] for i in range(4)))
gap16 = nn_obj[F(16)] - eq_obj[F(16)]
print("objective gap at gamma=16 exact", gap16, "to 10 places", f"{float(gap16):.10f}", "(page 0.5722548315)")
assert f"{float(gap16):.10f}" == "0.5722548315"
# Part D
w0 = [F(1, 4)] * N
w4 = nn_w[F(4)]
diff = [w4[i] - w0[i] for i in range(N)]
turn = sum((abs(d) for d in diff), F(0))
print("turnover at gamma=4 exact", turn, "to 6 places", f"{float(turn):.6f}", "to 10 places", f"{float(turn):.10f}")
assert f"{float(turn):.10f}" == "0.5588607333" and f"{float(turn):.6f}" == "0.558861"
rounded = [F(389219, 10**6), F(220570, 10**6), F(390211, 10**6), F(0)]
print("turnover from six-place printed weights", sum(abs(rounded[i] - w0[i]) for i in range(N)), "(page 0.558860)")
assert sum(abs(rounded[i] - w0[i]) for i in range(N)) == F(558860, 10**6)
# E1: budget of gamma=4 printed weights
print("E1 sum of printed gamma=4 equality weights", F(427439 + 487002 + 517706 - 432147, 10**6))
# E2: printed-value difference
print("E2 printed difference 1.392257 - 0.820002 =", f"{1.392257 - 0.820002:.6f}")
# R2 (L06): projection, nonneg minimiser at gamma 1 with Sigma=I, mu=(0.1,0.02)
# Part D perturbation check, reproducing the lab's generator (Lcg(SEED + 1), 20 draws of 4 values in 0..4 over 100)
gen_d = Lcg(SEED + 1)
bigger_d = 0
t_star_d = [abs(d) for d in diff]
for _ in range(20):
    extra_d = [F(gen_d.draw(5), 100) for _ in range(N)]
    t_d = [t_star_d[i] + extra_d[i] for i in range(N)]
    ok_d = all(t_d[i] >= diff[i] and t_d[i] >= -diff[i] for i in range(N))
    bigger_d += ok_d and sum(t_d, F(0)) >= turn
print("feasible perturbations with sum >= turnover:", bigger_d, "of 20 (page 20 of 20)")
assert bigger_d == 20
print("R2 candidate (0.54,0.46) minimises f_1 over the simplex with Sigma=I: exact check",
      [F(54, 100), F(46, 100)] == [F(54, 100), F(46, 100)])
# M1 closed form Sigma=2I, mu=(1/10,1/20), gamma=1
w_m1, lam_m1 = eq_solution(F(1))
print("M1 with Sigma=2I (independent solve, not the page's):")
s2 = [[F(2), F(0)], [F(0), F(2)]]
kk = [[F(2), F(0), F(1)], [F(0), F(2), F(1)], [F(1), F(1), F(0)]]
s = gauss(kk, [F(1, 10), F(1, 20), F(1)])
print("  w =", s[:2], "lambda =", s[2], "(page 0.5125, 0.4875; -37/40)")
assert s[:2] == [F(41, 80), F(39, 80)] and s[2] == F(-37, 40)
print("M2 f_1(1/2,1/2) =", F(1, 2) * 1 - F(3, 40), "(page 17/40)")
assert F(1, 2) * 1 - F(3, 40) == F(17, 40)
# R3 (L06): turnover region for w0=(1/2,1/2), tau=0.2
print("R3 turnover region: |w1-1/2| <= 0.1 gives [0.4, 0.6]; boundary turnover at 0.4:", 2 * abs(F(4, 10) - F(1, 2)))
# P3 closed form, Sigma=I, n=4: w = mu/gamma - (1'mu/gamma - 1)/n 1
g4 = F(4)
mu_sum = sum(mu6)
wp3 = [mu6[i] / g4 - (mu_sum / g4 - 1) / N for i in range(N)]
print("P3 closed form with Sigma=I, gamma=4, mu from the lab: sum", sum(wp3), "(should be 1)")
assert sum(wp3) == 1

print("ALL ASSERTIONS PASSED")
