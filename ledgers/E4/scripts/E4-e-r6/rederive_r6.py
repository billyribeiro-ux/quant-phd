"""Independent re-derivation of the numbers quoted in the E4 cards (round 6, slice e).

Exact Fractions where the lesson is exact; floats only for the L08 bisection and the L06/L07 sampled
values that are not reproduced here. Prints one line per check: name, recomputed value, quoted value, OK.
"""
import math
from fractions import Fraction as F
from itertools import product

fails = []


def check(name, got, want, tol=None):
    ok = (abs(got - want) <= tol) if tol is not None else (got == want)
    if not ok:
        fails.append(name)
    print(f"{name}: got {got} quoted {want} {'OK' if ok else 'FAIL'}")


# ---- L01: value and expected payoff under prices / probabilities (Lab 1 numbers)
pi1 = [F(1, 8), F(3, 8), F(3, 8), F(1, 8)]
q1 = [F(1, 2), F(1, 3), F(1, 4), F(1, 5)]
x1 = [F(100), F(40), F(0), F(250)]
y1 = [F(0), F(60), F(120), F(30)]
check("L01 value x", sum(a * b for a, b in zip(q1, x1)), F(340, 3))
check("L01 value y", sum(a * b for a, b in zip(q1, y1)), F(56))
comb = [2 * a - F(1, 2) * b for a, b in zip(x1, y1)]
check("L01 value of 2x-y/2", sum(a * b for a, b in zip(q1, comb)), F(596, 3))
check("L01 E x", sum(a * b for a, b in zip(pi1, x1)), F(235, 4))
check("L01 340/3 about 113.33", round(float(F(340, 3)), 2), 113.33)

# ---- L02: Example 2.11 and Lab 2 numbers
pi2 = [F(1, 2), F(1, 4), F(1, 4)]
e1 = [F(3), F(4), F(1)]
e2 = [F(1), F(4), F(3)]
ebar = [a + b for a, b in zip(e1, e2)]
check("L02 aggregate", ebar, [F(4), F(8), F(4)])
th1 = sum(p * a / t for p, a, t in zip(pi2, e1, ebar))
th2 = sum(p * a / t for p, a, t in zip(pi2, e2, ebar))
check("L02 theta1", th1, F(9, 16))
check("L02 theta2", th2, F(7, 16))
qs = [p / t for p, t in zip(pi2, ebar)]
check("L02 prices", qs, [F(1, 8), F(1, 32), F(1, 16)])
check("L02 q.ebar", sum(a * b for a, b in zip(qs, ebar)), F(1))
x1s = [t * th1 for t in ebar]
x2s = [t * th2 for t in ebar]
check("L02 demand1", x1s, [F(9, 4), F(9, 2), F(9, 4)])
check("L02 demand2", x2s, [F(7, 4), F(7, 2), F(7, 4)])
check("L02 ratio agent1", [p / (x * q) for p, x, q in zip(pi2, x1s, qs)], [F(16, 9)] * 3)
check("L02 ratio agent2", [p / (x * q) for p, x, q in zip(pi2, x2s, qs)], [F(16, 7)] * 3)
check("L02 v=(1,-1,0) value", qs[0] - qs[1], F(3, 32))
check("L02 endowment cost", sum(a * b for a, b in zip(qs, e1)), F(9, 16))

# ---- L03: MRS values and R2 derivatives; grid search count
def mrs(pi, x, s, t):
    return (pi[s] / x[s]) / (pi[t] / x[t])


for (s, t) in [(0, 1), (0, 2), (1, 2)]:
    check(f"L03 MRS agent1 {s}{t}", mrs(pi2, x1s, s, t), mrs(pi2, x2s, s, t))
check("L03 MRS12", mrs(pi2, x1s, 0, 1), F(4))
check("L03 MRS13", mrs(pi2, x1s, 0, 2), F(2))
check("L03 MRS23", mrs(pi2, x1s, 1, 2), F(1, 2))
check("L03 price ratio 12", qs[0] / qs[1], F(4))
check("L03 price ratio 13", qs[0] / qs[2], F(2))
check("L03 price ratio 23", qs[1] / qs[2], F(1, 2))
# R2: U1'(eps) = pi1*(-1/3) + pi2*(4/4); U2'(eps) = pi1*(1) + pi2*(-4/4)
check("L03 R2 dU1", pi2[0] * F(-1, 3) + pi2[1] * F(4, 4), F(1, 12))
check("L03 R2 dU2", pi2[0] * F(1) + pi2[1] * F(-4, 4), F(1, 4))
# finite Pareto grid search, recomputed independently (floats, tolerance 1e-12)
GRID = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
tot = ebar


def util(bundle):
    return sum(float(p) * math.log(float(x)) if x > 0 else -math.inf for p, x in zip(pi2, bundle))


def improves(c, r):
    return all(ci >= ri - 1e-12 for ci, ri in zip(c, r)) and any(ci > ri + 1e-12 for ci, ri in zip(c, r))


ref_eq = (util(x1s), util(x2s))
ref_en = (util(e1), util(e2))
cands = []
for f in product(GRID, repeat=3):
    a1 = [fi * t for fi, t in zip(f, tot)]
    a2 = [(1 - fi) * t for fi, t in zip(f, tot)]
    cands.append((a1, a2))
n_eq = sum(1 for a1, a2 in cands if improves((util(a1), util(a2)), ref_eq))
n_en = sum(1 for a1, a2 in cands if improves((util(a1), util(a2)), ref_en))
check("L03 grid size", len(cands), 125)
check("L03 improvements at equilibrium", n_eq, 0)
check("L03 improvements at endowment", n_en, 2)

# ---- L04: ranks and attainability (Gaussian elimination in Fractions)
def rank(rows):
    m = [list(map(F, r)) for r in rows]
    r = 0
    ncol = len(m[0])
    for c in range(ncol):
        piv = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c] / m[r][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return r


inc = [(1, 1, 1), (0, 1, 2)]
comp = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 2, 3)]
check("L04 rank incomplete", rank(inc), 2)
check("L04 rank complete", rank(comp), 3)
for pay, want in [((1, 2, 3), 2), ((0, 0, 1), 3), ((5, 0, 0), 3)]:
    check(f"L04 augmented rank {pay}", rank(inc + [pay]), want)
check("L04 rank of (1,1,1),(1,1,1),(0,1,2)", rank([(1, 1, 1), (1, 1, 1), (0, 1, 2)]), 2)
check("L04 rank of (1,2,0),(2,4,0)", rank([(1, 2, 0), (2, 4, 0)]), 1)

# ---- L05: fixed point and error ratios
def run_map(alpha, beta, vs, delta, steps=8, start=(F(0), F(0))):
    c0, c1 = start
    path = [(c0, c1)]
    for _ in range(steps):
        c0, c1 = (alpha - vs * c0) / beta, -(vs * c1 + delta) / beta
        path.append((c0, c1))
    return path


def fp(alpha, beta, vs, delta):
    return (alpha / (beta + vs), -delta / (beta + vs))


tgt = fp(F(10), F(2), F(1, 2), F(3, 4))
check("L05 base fixed point c0", tgt[0], F(4))
check("L05 base fixed point c1", tgt[1], F(-3, 10))
path = run_map(F(10), F(2), F(1, 2), F(3, 4))
check("L05 base c0 path 0,5,15/4,65/16", [str(p[0]) for p in path[:4]], ["0", "5", "15/4", "65/16"])
check("L05 base ratio c0", (path[1][0] - tgt[0]) / (path[0][0] - tgt[0]), F(-1, 4))
tgt_eq = fp(F(10), F(2), F(2), F(3, 4))
check("L05 equal fixed point c0", tgt_eq[0], F(5, 2))
check("L05 equal fixed point c1", tgt_eq[1], F(-3, 16))
path_eq = run_map(F(10), F(2), F(2), F(3, 4), steps=6)
check("L05 equal path", [str(p[0]) for p in path_eq], ["0", "5", "0", "5", "0", "5", "0"])
tgt_l = fp(F(10), F(2), F(3), F(3, 4))
check("L05 large fixed point c0", tgt_l[0], F(2))
check("L05 large fixed point c1", tgt_l[1], F(-3, 20))
path_l = run_map(F(10), F(2), F(3), F(3, 4), steps=3)
check("L05 large path", [str(p[0]) for p in path_l], ["0", "5", "-5/2", "35/4"])
check("L05 large ratio", (path_l[2][0] - tgt_l[0]) / (path_l[1][0] - tgt_l[0]), F(-3, 2))
check("L05 damped step c0", F(4, 5) * (F(10) / 2), F(4))
check("L05 damped weight", F(2) / (F(2) + F(1, 2)), F(4, 5))
check("L05 M3 conditional variance", (F(4) + F(1)) / F(4), F(5, 4))

# ---- L06: base instance, moments, clearing and the alternative slope
sv, se, a, lam, su = F(1), F(1), F(1), F(1, 2), F(1, 4)
tv, te = 1 / sv, 1 / se
kap = a / (lam * te)
seta = se + kap * kap * su
teta = 1 / seta
tbar = lam * te + (1 - lam) * teta
ths = tbar / (tv + tbar)
thu = kap * ths
check("L06 kappa", kap, F(2))
check("L06 sigma_eta2", seta, F(2))
check("L06 tau_bar", tbar, F(3, 4))
check("L06 theta_s", ths, F(3, 7))
check("L06 theta_u", thu, F(6, 7))
varp = ths ** 2 * (sv + se) + thu ** 2 * su
covvp = ths * sv
b = covvp / varp
check("L06 Var(p)", varp, F(27, 49))
check("L06 slope b", b, F(7, 9))
check("L06 posterior var", sv - b * covvp, F(2, 3))


def resid(s, u, th_s, th_u):
    p = th_s * s - th_u * u
    vp = th_s ** 2 * (sv + se) + th_u ** 2 * su
    cv = th_s * sv
    slope = cv / vp
    rv = sv - slope * cv
    vI = sv * se / (sv + se)
    dI = (sv * s / (sv + se) - p) / (a * vI)
    dU = (slope * p - p) / (a * rv)
    return lam * dI + (1 - lam) * dU - u


grid_s = [F(-1), F(0), F(1), F(2)]
grid_u = [F(-1), F(0), F(1, 2), F(2)]
zeros = sum(1 for s in grid_s for u in grid_u if resid(s, u, ths, thu) == 0)
check("L06 zero residuals of 16", zeros, 16)
check("L06 alt residual at (1,0)", resid(F(1), F(0), F(1, 2), thu), F(-9, 85))
check("L06 x_I at (1,0)", (F(1, 2) * F(1) - ths) / (F(1) * F(1, 2)), F(1, 7))
check("L06 x_U at (1,0)", (F(7, 9) * ths - ths) / (F(1) * F(2, 3)), F(-1, 7))

# ---- L07: informativeness sweep (exact)
def coef(sv_, se_, a_, lam_, sd_):
    tv_ = 1 / sv_
    te_ = 1 / se_
    k = a_ / (lam_ * te_)
    s2 = se_ + k * k * sd_ * sd_
    tb = lam_ * te_ + (1 - lam_) * (1 / s2)
    th = tb / (tv_ + tb)
    return s2, th, k * th


def rho2(sv_, se_, a_, lam_, sd_):
    s2, th, tu = coef(sv_, se_, a_, lam_, sd_)
    cv = th * sv_
    vp = th * th * (sv_ + se_) + tu * tu * sd_ * sd_
    return cv * cv / (sv_ * vp), sv_ / (sv_ + s2), vp


for sd_, want_r, want_v in [(F(1, 4), F(4, 9), F(729, 1444)), (F(1, 2), F(1, 3), F(27, 49)),
                            (F(1), F(1, 6), F(27, 32)), (F(2), F(1, 18), F(729, 338)),
                            (F(4), F(1, 66), F(35937, 4802))]:
    r_m, r_c, vp = rho2(F(1), F(1), F(1), F(1, 2), sd_)
    check(f"L07 rho2 moments sd={sd_}", r_m, want_r)
    check(f"L07 rho2 closed sd={sd_}", r_c, want_r)
    check(f"L07 Var(p) sd={sd_}", vp, want_v)
for lam_, want in [(F(1, 4), F(1, 6)), (F(1, 2), F(1, 3)), (F(3, 4), F(9, 22))]:
    check(f"L07 rho2 lam={lam_}", rho2(F(1), F(1), F(1), lam_, F(1, 2))[1], want)
for a_, want in [(F(1, 2), F(4, 9)), (F(1), F(1, 3)), (F(2), F(1, 6))]:
    check(f"L07 rho2 a={a_}", rho2(F(1), F(1), a_, F(1, 2), F(1, 2))[1], want)
check("L07 tiny sd below benchmark", rho2(F(1), F(1), F(1), F(1, 2), F(1, 100))[1] < F(1, 2), True)
check("L07 M1 rho2 at sd=1", rho2(F(1), F(1), F(1), F(1, 2), F(1))[1], F(1, 6))
check("L07 M2 rho2 lam=3/4", rho2(F(1), F(1), F(1), F(3, 4), F(1, 2))[1], F(9, 22))
check("L07 R2 sigma_u", math.sqrt(0.5), 0.7071067811865476, 1e-12)

# ---- L08: G(0), G(1), bisection roots, Corr^2 at the printed costs (floats, from the lesson formulas)
A, VV, VE, VU = 2.0, 1.0, 1.0, 1.0


def gain(lmb, vu=VU):
    tv = 1 / VV
    te = 1 / VE
    k = A * VE / lmb
    teta = 1 / (VE + k * k * vu)
    aw = lmb * te + (1 - lmb) * teta
    beta = aw / (tv + aw)
    bs = te / (tv + te)
    by = teta / (tv + teta)
    postI = 1 / (tv + te)
    postU = 1 / (tv + teta)
    vdI = (bs - beta) ** 2 * (VV + VE) + (k * beta) ** 2 * vu
    vdU = (by - beta) ** 2 * (VV + 1 / teta)
    return math.log((1 + vdI / postI) / (1 + vdU / postU)) / (2 * A), by


def gain0():
    return math.log(1 + VV / VE) / (2 * A)


check("L08 G(0)", gain0(), math.log(2) / 4, 1e-12)
check("L08 G(1)", gain(1.0)[0], math.log(5 / 3) / 4, 1e-12)
check("L08 G(0.5)", round(gain(0.5)[0], 6), 0.158997)


def solve(cost):
    if cost >= gain0():
        return 0.0
    if cost <= gain(1.0)[0]:
        return 1.0
    lo, hi = 0.0, 1.0
    while hi - lo > 1e-12:
        mid = 0.5 * (lo + hi)
        if gain(mid)[0] - cost > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


for cost, want in [(0.12, 1.0), (0.13, 0.965625410), (0.15, 0.657828572), (0.17, 0.231615819), (0.18, 0.0)]:
    lam_star = solve(cost)
    check(f"L08 lambda* at cost {cost}", round(lam_star, 9), want, 1e-9)
lam15 = solve(0.15)
check("L08 Corr2 at cost 0.15", round(gain(lam15)[1], 6), 0.088941, 1e-6)
check("L08 Corr2 at cost 0.17", round(gain(solve(0.17))[1], 6), 0.013061, 1e-6)
check("L08 gap at cost 0.15 ~ 0", abs(gain(lam15)[0] - 0.15) < 1e-12, True)
check("L08 gap at cost 0.12 (N(1))", round(gain(1.0)[0] - 0.12, 5), 0.00771, 1e-5)
check("L08 gap at cost 0.18 (N(0))", round(gain0() - 0.18, 5), -0.00671, 1e-5)
tau_eta_half = 1 / (VE + (A * VE / 0.5) ** 2 * VU)
check("L08 quiz tau_eta lam=1/2", round(tau_eta_half, 12), round(1 / 17, 12), 1e-12)

# ---- L09: counts and example
VALS = (-2, -1, 0, 1, 2)
ST = (1, 2, 3, 4, 5, 6)
P1c = (frozenset({1, 2}), frozenset({3}), frozenset({4, 5, 6}))
P2c = (frozenset({1, 2, 3}), frozenset({4, 5}), frozenset({6}))


def cell(part, w):
    return next(c for c in part if w in c)


def post(part, w, rec):
    c = cell(part, w)
    return sum(F(rec[k]) for k in c) / len(c)


def meet_of(w):
    seen = {w}
    stack = [w]
    while stack:
        cur = stack.pop()
        for part in (P1c, P2c):
            for o in cell(part, cur):
                if o not in seen:
                    seen.add(o)
                    stack.append(o)
    return frozenset(seen)


check("L09 meet of 1", sorted(meet_of(1)), [1, 2, 3])
check("L09 meet of 4", sorted(meet_of(4)), [4, 5, 6])
ex = dict(zip(ST, (-1, 2, -2, -2, -2, -2)))
neg = {k: -v for k, v in ex.items()}
check("L09 g1(1)", post(P1c, 1, ex), F(1, 2))
check("L09 g2(1)", post(P2c, 1, neg), F(1, 3))
check("L09 g1(3)", post(P1c, 3, ex), F(-2))
strict_total = {1: 0, 4: 0}
nonneg_meet = {1: 0, 4: 0}
both_zero = 0
for vals in product(VALS, repeat=6):
    x = dict(zip(ST, vals))
    nx = {k: -v for k, v in x.items()}
    for st in (1, 4):
        m = meet_of(st)
        g1s = {w: post(P1c, w, x) for w in ST}
        g2s = {w: post(P2c, w, nx) for w in ST}
        if g1s[st] > 0 and g2s[st] > 0:
            strict_total[st] += 1
            if all(g1s[w] >= 0 and g2s[w] >= 0 for w in m):
                nonneg_meet[st] += 1
        if st == 1 and all(g1s[w] >= 0 and g2s[w] >= 0 for w in m):
            nonneg_meet.setdefault("cnt1", 0)
            nonneg_meet["cnt1"] += 1
            if all(g1s[w] == 0 and g2s[w] == 0 for w in m):
                both_zero += 1
check("L09 strict at state 1", strict_total[1], 500)
check("L09 strict at state 4", strict_total[4], 500)
check("L09 strict and nonneg on meet (state 1)", nonneg_meet[1], 0)
check("L09 strict and nonneg on meet (state 4)", nonneg_meet[4], 0)
check("L09 nonneg on meet (state 1)", nonneg_meet.get("cnt1", 0), 625)
check("L09 zero posteriors on meet 1 (625)", both_zero, 625)
check("L09 5^6", len(list(product(VALS, repeat=6))), 15625)
check("L09 two priors receipts 0.4", 0.7 - 0.3, 0.4, 1e-12)
check("L09 two priors receipts 0.2", -(0.4 - 0.6), 0.2, 1e-12)

print("FAILS:", fails)
