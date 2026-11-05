"""Independent re-derivation of the numbers in E4 L07, L08 and L09 (verifier round 8).

Written from the lesson statements (Proposition 6.7 of L06 as quoted in L07, and Definition 4.3, Proposition 3.1,
Proposition 4.1 and Lemma 4.5 of L08), not from the lab twins. Exact Fraction arithmetic where possible.
"""
import itertools
import math
from fractions import Fraction as F

print("== L07: exact population values ==")


def l07(sig_v2, sig_e2, a, lam, sd):
    tau_v = 1 / sig_v2
    tau_e = 1 / sig_e2
    kappa = a * sig_e2 / lam  # kappa = a sigma_eps^2 / lambda (Proposition 6.7 of L06)
    sig_eta2 = sig_e2 + kappa**2 * sd**2
    tau_eta = 1 / sig_eta2
    tau_bar = lam * tau_e + (1 - lam) * tau_eta
    theta_s = tau_bar / (tau_v + tau_bar)
    theta_u = kappa * theta_s
    var_p = theta_s**2 * (sig_v2 + sig_e2) + theta_u**2 * sd**2
    cov_vp = theta_s * sig_v2
    rho2_moments = cov_vp**2 / (sig_v2 * var_p)
    rho2_closed = sig_v2 / (sig_v2 + sig_eta2)
    return dict(sig_eta2=sig_eta2, theta_s=theta_s, theta_u=theta_u, var_p=var_p, rho2=rho2_moments,
                closed=rho2_closed, tau_eta=tau_eta)


base = l07(F(1), F(1), F(1), F(1, 2), F(1, 2))
print("base", base)
for sd in [F(1, 4), F(1, 2), F(1), F(2), F(4)]:
    r = l07(F(1), F(1), F(1), F(1, 2), sd)
    print("sd", sd, "sig_eta2", r["sig_eta2"], "var_p", r["var_p"], "rho2", r["rho2"], "closed==moments", r["rho2"] == r["closed"])
for lam in [F(1, 4), F(1, 2), F(3, 4)]:
    r = l07(F(1), F(1), F(1), lam, F(1, 2))
    print("lam", lam, "sig_eta2", r["sig_eta2"], "rho2", r["rho2"])
for a in [F(1, 2), F(1), F(2)]:
    r = l07(F(1), F(1), a, F(1, 2), F(1, 2))
    print("a", a, "sig_eta2", r["sig_eta2"], "rho2", r["rho2"])
r = l07(F(1), F(1), F(1), F(1, 2), F(1, 100))
print("sd 1/100 rho2", r["rho2"], "below 1/2", r["rho2"] < F(1, 2))
# Remark 7.9: var_p monotone in sd on the printed grid?
vps = [l07(F(1), F(1), F(1), F(1, 2), sd)["var_p"] for sd in [F(1, 4), F(1, 2), F(1), F(2), F(4)]]
print("var_p rising on grid:", all(vps[i] < vps[i + 1] for i in range(4)), [str(v) for v in vps])
# Prop 7.7 signs checked on a random exact grid
ok = True
for sv, se, a, lam, su in itertools.product([F(1, 2), F(1), F(3)], [F(1, 3), F(1), F(2)], [F(1, 2), F(1), F(3)],
                                            [F(1, 5), F(1, 2), F(4, 5)], [F(1, 3), F(1), F(3)]):
    base_r = l07(sv, se, a, lam, su)["closed"]
    if not (l07(sv, se, a, lam, su * 2)["closed"] < base_r):
        ok = False
    if not (l07(sv, se, a * 2, lam, su)["closed"] < base_r):
        ok = False
    if not (l07(sv, se * 2, a, lam, su)["closed"] < base_r):
        ok = False
    if not (l07(sv, se, a, min(lam * F(3, 2), F(9, 10)), su)["closed"] > base_r) and min(lam * F(3, 2), F(9, 10)) > lam:
        ok = False
print("Prop 7.7 signs on exact grid:", ok)
# Lemma 7.4 / Remark 7.8 derived numbers
print("R2 sigma_u at base:", (F(2) / F(4)) ** 0.5, "(=1/sqrt 2)")
print("E2: sigma_u^2 for rho2=1/4:", (F(3) - 1) / 4)
print("E1: 1/3 - 0.330625 =", 1 / 3 - 0.330625, "in tolerance units", (1 / 3 - 0.330625) / 0.02)

print("== L08: G(lambda) from the Definition 4.3 formulas, floats ==")
A_CARA, VV, VE, VU = 2.0, 1.0, 1.0, 1.0


def gain(lam, vu=VU):
    tv, te = 1 / VV, 1 / VE
    kap = A_CARA * VE / lam
    se2 = VE + kap**2 * vu
    tn = 1 / se2
    Abar = lam * te + (1 - lam) * tn
    beta = Abar / (tv + Abar)
    bs = VV / (VV + VE)
    by = tn / (tv + tn)
    VI = 1 / (tv + te)
    VUp = 1 / (tv + tn)
    var_DI = (bs - beta) ** 2 * (VV + VE) + kap**2 * beta**2 * vu
    var_DU = (by - beta) ** 2 * (VV + se2)
    return math.log((1 + var_DI / VI) / (1 + var_DU / VUp)) / (2 * A_CARA)


def gain0(vu=VU):
    # Lemma 4.5 closed form, and the same quantity from the lambda=0 gaps (independent route)
    q = VV / VE
    return math.log(1 + q) / (2 * A_CARA)


g0, g1, gh = gain0(), gain(1.0), gain(0.5)
print("G(0) =", g0, "G(0.5) =", gh, "G(1) =", g1, " ln2/4 =", math.log(2) / 4, " ln(5/3)/4 =", math.log(5 / 3) / 4)
print("G(1e-6)-G(0) =", gain(1e-6) - g0)
grid = [k / 1000 for k in range(1, 1000)]
gs = [gain(x) for x in grid]
cs = []
for x in grid:
    kap = A_CARA / x
    se2 = 1 + kap**2
    tn = 1 / se2
    Ab = x + (1 - x) * tn
    beta = Ab / (1 + Ab)
    cs.append(tn / (1 + tn))
print("G strictly decreasing on grid:", all(gs[i + 1] < gs[i] for i in range(len(gs) - 1)))
print("Corr^2 strictly increasing on grid:", all(cs[i + 1] > cs[i] for i in range(len(cs) - 1)))


def root(cost):
    lo, hi = 0.0, 1.0
    while hi - lo > 1e-12:
        mid = (lo + hi) / 2
        if gain(mid) - cost > 0:
            lo = mid
        else:
            hi = mid
    lam = (lo + hi) / 2
    return lam, gain(lam) - cost


for cost in [0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18]:
    if cost >= g0:
        print("cost", cost, "boundary lam=0 gap", g0 - cost)
    elif cost <= g1:
        print("cost", cost, "boundary lam=1 gap", g1 - cost)
    else:
        lam, gap = root(cost)
        print("cost", cost, "root lam", round(lam, 9), "gap", gap)
# Proposition 5.2(a): limit of G at 0 with noise
for lam in [1e-2, 1e-4, 1e-6]:
    print("lam", lam, "G-G0", gain(lam) - g0)
# Part D analogue: noiseless
print("noiseless G(0.5) =", gain(0.5, vu=0.0), "noiseless G(1) =", gain(1.0, vu=0.0), "noiseless G(0) =", gain0(0.0))
# Example 1.1 part A slope formula check: b_y/beta at lam = 1/2
lam = 0.5
kap = 2 / lam
se2 = 1 + kap**2
tn = 1 / se2
Ab = lam + (1 - lam) * tn
beta = Ab / (1 + Ab)
print("b_y/beta at lam=1/2:", (tn / (1 + tn)) / beta)
# Corollary 3.2 at lam=1/2 (unit parameters, a=2): Corr^2 = 1/18
print("Corr^2 at lam=1/2:", tn / (1 + tn), "1/18 =", 1 / 18)

print("== L09: exhaustive enumeration with independent code ==")
states = [1, 2, 3, 4, 5, 6]
P1 = [{1, 2}, {3}, {4, 5, 6}]
P2 = [{1, 2, 3}, {4, 5}, {6}]


def cell(P, w):
    return next(c for c in P if w in c)


def gval(P, x, w):
    c = cell(P, w)
    return sum(x[k] for k in c) / len(c)  # uniform prior: the prior weights cancel within a cell


def meet(w):
    seen, stack = {w}, [w]
    while stack:
        u = stack.pop()
        for P in (P1, P2):
            for v in cell(P, u):
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
    return seen


vals = [-2, -1, 0, 1, 2]
for w in (1, 4):
    M = meet(w)
    strict = 0
    strict_and_nonneg = 0
    nonneg = 0
    nonneg_nonzero = 0
    for tup in itertools.product(vals, repeat=6):
        x = dict(zip(states, tup))
        nx = {k: -v for k, v in x.items()}
        g1 = {u: gval(P1, x, u) for u in states}
        g2 = {u: gval(P2, nx, u) for u in states}
        if g1[w] > 0 and g2[w] > 0:
            strict += 1
            if all(g1[u] >= 0 and g2[u] >= 0 for u in M):
                strict_and_nonneg += 1
        if all(g1[u] >= 0 and g2[u] >= 0 for u in M):
            nonneg += 1
            if any(g1[u] != 0 or g2[u] != 0 for u in M):
                nonneg_nonzero += 1
    print(f"state {w}: meet {sorted(M)} strict-both {strict}, strict&nonneg-on-meet {strict_and_nonneg}, "
          f"nonneg-on-meet {nonneg}, nonzero among them {nonneg_nonzero}")
# first bet in product order with both strict at state 1
for tup in itertools.product(vals, repeat=6):
    x = dict(zip(states, tup))
    nx = {k: -v for k, v in x.items()}
    if gval(P1, x, 1) > 0 and gval(P2, nx, 1) > 0:
        print("first strict bet at state 1:", tup)
        break
for tup in itertools.product(vals, repeat=6):
    x = dict(zip(states, tup))
    nx = {k: -v for k, v in x.items()}
    if gval(P1, x, 4) > 0 and gval(P2, nx, 4) > 0:
        print("first strict bet at state 4:", tup)
        break
# Example 2.4 values
x = {1: -1, 2: 2, 3: -2, 4: -2, 5: -2, 6: -2}
nx = {k: -v for k, v in x.items()}
print("Ex2.4 g1(1), g2(1), g1(3):", gval(P1, x, 1), gval(P2, nx, 1), gval(P1, x, 3))
# Mech 2 meet on the 4-state example
P1b = [{1, 2}, {3, 4}]
P2b = [{1}, {2, 3}, {4}]
def meet_b(w):
    seen, stack = {w}, [w]
    while stack:
        u = stack.pop()
        for P in (P1b, P2b):
            for v in cell(P, u):
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
    return sorted(seen)
print("Mech 2 meet M(1) =", meet_b(1))
