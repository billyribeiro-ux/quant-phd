"""E4-c round 2: independent re-derivation of every printed or quoted number in L07, L08 and L09.

Written from the page text, not from the lab code. Standard library only. Usage: python -I recheck_c_r2.py
"""
from fractions import Fraction as F
import math
import itertools

def p(*args):
    print(*args)

# ---------- L07: exact moments of p = theta_s s - theta_u u, with kappa = a sig_e2 / lam ----------
def l07_coef(sv2, se2, a, lam, su2):
    tau_v = 1 / sv2
    kappa = a * se2 / lam
    sig_eta2 = se2 + kappa * kappa * su2          # sigma_u2 is the variance (sd squared)
    tau_eta = 1 / sig_eta2
    tau_bar = lam / se2 + (1 - lam) * tau_eta
    theta_s = tau_bar / (tau_v + tau_bar)
    theta_u = kappa * theta_s
    return kappa, sig_eta2, theta_s, theta_u

def l07_rho2_moments(sv2, se2, su2, a, lam):
    kappa, s_eta2, ts, tu = l07_coef(sv2, se2, a, lam, su2)
    cov = ts * sv2
    varp = ts * ts * (sv2 + se2) + tu * tu * su2
    return cov * cov / (sv2 * varp), varp, sv2 / (sv2 + s_eta2), s_eta2

one, half, quarter = F(1), F(1, 2), F(1, 4)
p("L07 Part A (sd=1/2, lam=1/2, a=1): moments and closed form")
r_mom, varp, r_cl, se = l07_rho2_moments(one, one, F(1, 4), one, half)
p(f"  rho2 moments {r_mom} closed {r_cl} sig_eta2 {se}  (page: 1/3, sig_eta2 2)")
p("L07 Part B (sweep over sd; sd^2 = su2)")
for sd in [F(1, 4), F(1, 2), F(1), F(2), F(4)]:
    r, vp, rc, s_eta2 = l07_rho2_moments(one, one, sd * sd, one, half)
    p(f"  sd {sd}: sig_eta2 {s_eta2} var_p {vp} rho2 {r} closed {rc}")
p("L07 Part C (lam sweep at sd=1/2):")
for lam in [F(1, 4), F(1, 2), F(3, 4)]:
    r, vp, rc, s_eta2 = l07_rho2_moments(one, one, F(1, 4), one, lam)
    p(f"  lam {lam}: sig_eta2 {s_eta2} rho2 {r}")
p("L07 Part D (a sweep at sd=1/2, lam=1/2):")
for a in [F(1, 2), F(1), F(2)]:
    r, vp, rc, s_eta2 = l07_rho2_moments(one, one, F(1, 4), a, half)
    p(f"  a {a}: sig_eta2 {s_eta2} rho2 {r}")
p("L07 Part E: benchmark and sd=1/100:")
r, vp, rc, s_eta2 = l07_rho2_moments(one, one, F(1, 10000), one, half)
p(f"  benchmark {F(1,2)} rho2(sd=1/100) {r}  (page: 2500/5001)  below: {r < F(1,2)}")
p("L07 Part F arithmetic: |1/3 - 0.330625| / 0.02 =", round(abs(1/3 - 0.330625) / 0.02, 4), "(page: 0.135)")

# Misconception and problem numbers
p("L07 M1 (sig_v2=sig_e2=1, a=1, lam=1/2, sd=1): rho2", l07_rho2_moments(one, one, one, one, half)[0], "(page 1/6)")
p("L07 M2 (sd=1/2, lam=3/4): rho2", l07_rho2_moments(one, one, quarter, one, F(3, 4))[0], "(page 9/22)")
p("L07 M3 (sig_v2=2, sd=1): rho2", l07_rho2_moments(F(2), one, one, one, half)[0], "(page 2/7)")
# E2: rho2 = 1/4 => sig_eta2 = 3 => 1 + 4 su2 = 3 => su2 = 1/2
p("L07 E2 check: sig_eta2 for rho2=1/4 is", F(4) - 1, "; su2 =", F(3 - 1, 4), "(page: 1/2)")
# R2: chi sigma_u^2 = sig_v2 + sig_e2 with chi = a^2 sig_e2^2 / lam^2 (sig_e2 = 1): chi = 4
chi = (one * one) / (half * half)
p("L07 R2: chi =", chi, " su2 =", (2) / chi, "(page: 1/2, sigma_u = 1/sqrt2)")
# Witness: v ~ N(0,1), p = v^2
# E v^4 = 3, E v^2 = 1, E v^3 = 0, E v = 0
Ev4, Ev2, Ev3, Ev1 = F(3), F(1), F(0), F(0)
varp_w = Ev4 - Ev2 * Ev2
cov_w = Ev3 - Ev1 * Ev2
p("L07 witness: Var(p) =", varp_w, " Cov(v,p) =", cov_w, " rho2 =", cov_w * cov_w / (1 * varp_w), "(page: Var=2, rho2=0)")
# R1 limit: rho2 = sv2/(sv2 + s_eta2) with kappa -> infinity
for a in [F(10), F(1000)]:
    r, vp, rc, se_ = l07_rho2_moments(one, one, quarter, a, half)
    p(f"L07 R1 a={a}: rho2 {float(r):.3e}")
# Sign grids (Prop 7.7) on exact rationals
ok = True
vals = [F(i, 10) for i in range(1, 6)]
for sv2, se2, su2, a, lam in itertools.product(vals, vals, [F(i, 7) for i in range(1, 5)], [F(i, 3) for i in range(1, 4)], [F(i, 10) for i in range(1, 10)]):
    base = l07_rho2_moments(sv2, se2, su2, a, lam)[0]
    if l07_rho2_moments(sv2, se2, su2 + F(1, 100), a, lam)[0] >= base: ok = False
    if l07_rho2_moments(sv2, se2, su2, a + F(1, 100), lam)[0] >= base: ok = False
    if l07_rho2_moments(sv2, se2 + F(1, 100), su2, a, lam)[0] >= base: ok = False
    if l07_rho2_moments(sv2, se2, su2, a, min(lam + F(1, 100), F(99, 100)))[0] <= base and lam < F(99, 100): ok = False
p("L07 Prop 7.7 sign grid on exact rationals (4-dp steps, all signs):", ok)

# ---------- L08 ----------
A_, SV, SE, SU, PM = 2.0, 1.0, 1.0, 1.0, 0.0
def l08_eq(lam, su2=SU):
    tv, te = 1 / SV, 1 / SE
    kappa = A_ * SE / lam
    teta = 1 / (SE + kappa * kappa * su2)
    Aw = lam * te + (1 - lam) * teta
    beta = Aw / (tv + Aw)
    bs = te / (tv + te)
    by = teta / (tv + teta)
    Vi = 1 / (tv + te)
    Vu = 1 / (tv + teta)
    vdi = (bs - beta) ** 2 * (SV + SE) + (kappa * beta) ** 2 * su2
    vdu = (by - beta) ** 2 * (SV + 1 / teta)
    G = math.log((1 + vdi / Vi) / (1 + vdu / Vu)) / (2 * A_)
    return dict(G=G, corr2=by, beta=beta, kappa=kappa, vdi=vdi, vdu=vdu, Vi=Vi, Vu=Vu, teta=teta)

def G0(su2=SU):
    return math.log(1 + SV / SE) / (2 * A_)

p("L08 G(0) =", round(G0(), 6), " closed ln2/4 =", round(math.log(2) / 4, 6))
p("L08 G(1) =", l08_eq(1.0)["G"], " closed ln(5/3)/4 =", math.log(5 / 3) / 4)
p("L08 Emp3 at lam=1: kappa", l08_eq(1.0)["kappa"], "teta", l08_eq(1.0)["teta"], "b_y", l08_eq(1.0)["corr2"], "beta", l08_eq(1.0)["beta"])
p("L08 Lab part A b_y/beta at lam=1/2 =", l08_eq(0.5)["corr2"] / l08_eq(0.5)["beta"], "(page 0.1605)")
p("L08 Corr at lam=1/2 (quiz 1/18):", l08_eq(0.5)["corr2"], 1 / 18)
# Independent bisection with a different bracket rule (fixed 200 halvings) for the printed costs
def fraction_for_cost(cost):
    if cost >= G0():
        return 0.0
    if cost <= l08_eq(1.0)["G"]:
        return 1.0
    lo, hi = 1e-300, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if l08_eq(mid)["G"] - cost > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
for c, printed in [(0.13, 0.965625410), (0.14, 0.815032329), (0.15, 0.657828572), (0.16, 0.480567912), (0.17, 0.231615819)]:
    lam = fraction_for_cost(c)
    p(f"L08 root cost {c}: independent {lam:.9f} printed {printed:.9f} diff {abs(lam - printed):.2e} gap {l08_eq(lam)['G'] - c:.2e}")
p("L08 corr at printed roots (cost 0.17):", l08_eq(0.231615819)["corr2"], "(page 0.013061)")
p("L08 corr at lam=1 (cost 0.12):", l08_eq(1.0)["corr2"], "(page 0.166667)")
p("L08 Part B gap(1e-6)-G0:", l08_eq(1e-6)["G"] - G0())
grid = [k / 1000 for k in range(1, 1000)]
gs = [l08_eq(x)["G"] for x in grid]
cs = [l08_eq(x)["corr2"] for x in grid]
p("L08 G strictly decreasing on 999 grid:", all(b < a for a, b in zip(gs, gs[1:])), " corr strictly increasing:", all(b > a for a, b in zip(cs, cs[1:])))
# Prop 5.2(a): G(lambda) -> G(0) as lambda -> 0 (noise su2=1)
for lam in [1e-2, 1e-3, 1e-4, 1e-5]:
    p(f"L08 Prop5.2a lam={lam}: G={l08_eq(lam)['G']:.9f} vs G0 {G0():.9f}")
# Noiseless case at cost 0.15 (page: no equilibrium)
g_noiseless0 = G0(0.0) if False else math.log(1 + SV / SE) / (2 * A_)
def l08_noise0(lam):
    return l08_eq(lam, su2=0.0)["G"]
p("L08 noiseless: max |G| on grid", max(abs(l08_noise0(x)) for x in grid))
# Lemma 2.2 check: E exp(-Z^2/2) for Z ~ N(0,4) by numerical integration
import random
rng = random.Random(1)
n = 2000000
s = sum(math.exp(-(2.0 * rng.gauss(0, 1)) ** 2 / 2) for _ in range(n)) / n
p("L08 Lemma 2.2 MC (Z~N(0,4)):", round(s, 4), " closed 1/sqrt5 =", round(1 / math.sqrt(5), 6))
p("L08 Lemma 4.5 G(0) = ln(1+q)/(2a) with q=1:", math.log(2) / 4)

# ---------- L09 ----------
STATES = (1, 2, 3, 4, 5, 6)
P1 = [{1, 2}, {3}, {4, 5, 6}]
P2 = [{1, 2, 3}, {4, 5}, {6}]
def cell(part, w):
    for c_ in part:
        if w in c_:
            return c_
def meet(w):
    seen = {w}
    stack = [w]
    while stack:
        u = stack.pop()
        for part in (P1, P2):
            for v in cell(part, u):
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
    return seen
def post(part, w, x):
    c_ = cell(part, w)
    return F(sum(x[k] for k in c_), len(c_))
counts = {"strict1": 0, "nonneg_meet1": 0, "strict_and_nonneg_meet1": 0, "nonzero_on_nonneg1": 0,
          "strict4": 0, "nonneg_meet4": 0, "strict_and_nonneg_meet4": 0, "nonzero_on_nonneg4": 0}
first_strict1 = None
first_strict4 = None
for vals in itertools.product((-2, -1, 0, 1, 2), repeat=6):
    x = dict(zip(STATES, vals))
    negx = {k: -v for k, v in x.items()}
    g1 = {w: post(P1, w, x) for w in STATES}
    g2 = {w: post(P2, w, negx) for w in STATES}
    for st, tag in ((1, "1"), (4, "4")):
        M = meet(st)
        strict = g1[st] > 0 and g2[st] > 0
        nonneg = all(g1[w] >= 0 and g2[w] >= 0 for w in M)
        if strict:
            counts["strict" + tag] += 1
            if tag == "1" and first_strict1 is None:
                first_strict1 = vals
            if tag == "4" and first_strict4 is None:
                first_strict4 = vals
        if nonneg:
            counts["nonneg_meet" + tag] += 1
            if any(g1[w] != 0 or g2[w] != 0 for w in M):
                counts["nonzero_on_nonneg" + tag] += 1
        if strict and nonneg:
            counts["strict_and_nonneg_meet" + tag] += 1
p("L09 counts (independent enumeration of 15625 bets):", counts)
p("L09 first strict at state 1 (page: (-1,2,-2,-2,-2,-2)):", first_strict1)
p("L09 first strict at state 4 (page: (-2,-2,-2,-2,1,2)):", first_strict4)
p("L09 meet(1) =", sorted(meet(1)), " meet(4) =", sorted(meet(4)))
x = {1: -1, 2: 2, 3: -2, 4: -2, 5: -2, 6: -2}
p("L09 Example 2.4: g1(1), g2(1), g1(3):", post(P1, 1, x), post(P2, 1, {k: -v for k, v in x.items()}), post(P1, 3, x))
# Misconception 2 (states a,b,c)
Pa1 = [{"a", "b"}, {"c"}]
Pa2 = [{"a"}, {"b", "c"}]
def cella(part, w):
    for c_ in part:
        if w in c_:
            return c_
def meeta(w):
    seen = {w}; stack = [w]
    while stack:
        u = stack.pop()
        for part in (Pa1, Pa2):
            for v in cella(part, u):
                if v not in seen:
                    seen.add(v); stack.append(v)
    return seen
E = {"a", "b"}
p("L09 misc2: M(a) =", sorted(meeta("a")), " M(a) subset of E:", meeta("a") <= E)
# Res 2: two priors, bet exists; check the page's theta construction for a few (p, r)
for pp, rr in [(F(7, 10), F(4, 10)), (F(1, 10), F(9, 10)), (F(1, 3), F(1, 2))]:
    if pp > rr:
        pass
    lo_p, hi_p = (rr, pp) if rr < pp else (pp, rr)
    th = (lo_p + hi_p) / 2
    t = th / (1 - th)
    r1 = pp - (1 - pp) * t
    r2 = -(rr - (1 - rr) * t)
    p(f"L09 Res2 p={pp} r={rr}: t={float(t):.4f} trader1 receipt {float(r1):.4f} trader2 receipt {float(r2):.4f} (both >0 needs p>r case)")
# Mech 1 and Emp 3 claims
xx = {1: 2, 2: 0, 3: -1, 4: 4}
p("L09 Mech1 g1 on {1,2}, {3,4}:", F(2 + 0, 2), F(-1 + 4, 2))
# Emp 3: zero-posterior count on {1,2,3}: x(3)=0, x(2)=-x(1)
cnt = sum(1 for v in itertools.product((-2, -1, 0, 1, 2), repeat=6) if v[2] == 0 and v[1] == -v[0])
p("L09 Emp3 count of bets with x(3)=0, x(2)=-x(1):", cnt, "(page 625)")
