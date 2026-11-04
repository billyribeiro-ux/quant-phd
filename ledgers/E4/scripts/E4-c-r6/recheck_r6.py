"""E4-c round 6: independent recheck of the printed and quoted numbers in L07, L08 and L09.

Usage: python -I -W error recheck_r6.py   (standard library only; no import of the lab twins).
Each block re-derives a number from the model in its own code path and prints it next to the value the page quotes.
"""
import itertools
import math
from fractions import Fraction as F

print("== L07 (exact)")
# Base instance: sig_v^2 = sig_e^2 = 1, a = 1, lam = 1/2, sd = 1/2. Derive kappa, sig_eta^2, rho^2 by hand.
sv2, se2, a, lam = F(1), F(1), F(1), F(1, 2)


def rho2(sd):
    kappa = a * se2 / lam
    seta2 = se2 + kappa * kappa * sd * sd
    return sv2 / (sv2 + seta2), seta2


for sd in (F(1, 4), F(1, 2), F(1), F(2), F(4)):
    r, s2 = rho2(sd)
    print("sd", sd, "rho2", r, "sig_eta2", s2)
print("E2 check: sig_u^2 for rho2=1/4:", (3 - 1) / 4, "sigma_u =", math.sqrt(0.5))
print("R2 check: sigma_u at half benchmark:", math.sqrt(2 / 4))
print("E1 check: diff/tol =", (1 / 3 - 0.330625) / 0.02)
print("Lemma 7.3 witness: E[v^4]-1 =", 3 - 1)
# Price variance sweep via the closed form of L06 Prop 6.7 (theta_s, theta_u), recomputed by hand from tau.
for sd in (F(1, 4), F(4)):
    kappa = a * se2 / lam
    seta2 = se2 + kappa * kappa * sd * sd
    tau_bar = lam / se2 + (1 - lam) / seta2
    th_s = tau_bar / (1 / sv2 + tau_bar)
    th_u = kappa * th_s
    varp = th_s * th_s * (sv2 + se2) + th_u * th_u * sd * sd
    print("sd", sd, "theta_s", th_s, "theta_u", th_u, "var_p", varp)

print("== L08")


def gain(lam_, var_u, cara=2.0, vv=1.0, ve=1.0):
    """G(lam) from Definition 4.3 with Var(D_I), Var(D_U) written from Proposition 4.1 (independent code)."""
    tv, te = 1 / vv, 1 / ve
    kap = cara * ve / lam_
    teta = 1 / (ve + kap * kap * var_u)
    A = lam_ * te + (1 - lam_) * teta
    beta = A / (tv + A)
    bs = te / (tv + te)
    by = teta / (tv + teta)
    VI = 1 / (tv + te)
    VU = 1 / (tv + teta)
    DI = (bs - beta) ** 2 * (vv + ve) + (kap * beta) ** 2 * var_u
    DU = (by - beta) ** 2 * (vv + 1 / teta)
    return math.log((1 + DI / VI) / (1 + DU / VU)) / (2 * cara)


def gain0(var_u, cara=2.0, vv=1.0, ve=1.0):
    return math.log(1 + vv / ve) / (2 * cara)


print("G(0) =", gain0(1.0), " printed 0.173287")
print("G(0.5) =", gain(0.5, 1.0), " printed 0.158997")
print("G(1) =", gain(1.0, 1.0), " printed 0.127706 = ln(5/3)/4 =", math.log(5 / 3) / 4)
print("Lab Part A: b_y/beta at lam=1/2 =", (1 / 18) / (9 / 26), "(13/81)")
print("G(1e-6)-G(0) =", gain(1e-6, 1.0) - gain0(1.0))


def root(cost, tol=1e-13):
    """Secant-free bracket: bisection on the sign of G(lam)-cost with an endpoint test, written independently."""
    if cost >= gain0(1.0):
        return 0.0
    if cost <= gain(1.0, 1.0):
        return 1.0
    lo, hi = 1e-12, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if gain(mid, 1.0) > cost:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return (lo + hi) / 2


printed = {0.13: 0.965625410, 0.14: 0.815032329, 0.15: 0.657828572, 0.16: 0.480567912, 0.17: 0.231615819}
for c, pv in printed.items():
    r = root(c)
    print("cost", c, "lam*", round(r, 9), "printed", pv, "abs diff", abs(r - pv))
print("cost 0.12 lam* =", root(0.12), " cost 0.18 lam* =", root(0.18))
print("boundary gaps: G(1)-0.12 =", gain(1.0, 1.0) - 0.12, " G(0)-0.18 =", gain0(1.0) - 0.18)
print("Corr^2 at lam=1/2 (sig_u^2=1):", (1 / 17) / (1 + 1 / 17), "= 1/18")
print("L08 Part D: gain with sig_u^2 = 0 at lam = 0.3:", gain(0.3, 0.0))
print("Emp3 G(1) by hand: ln(5/3)/4 =", math.log(5 / 3) / 4)

print("== L09 (exact, independent enumeration)")
STATES = (1, 2, 3, 4, 5, 6)
PART1 = [{1, 2}, {3}, {4, 5, 6}]
PART2 = [{1, 2, 3}, {4, 5}, {6}]


def cell(part, w):
    for c in part:
        if w in c:
            return c
    raise ValueError


def meet(w):
    seen = {w}
    todo = [w]
    while todo:
        x = todo.pop()
        for part in (PART1, PART2):
            for y in cell(part, x):
                if y not in seen:
                    seen.add(y)
                    todo.append(y)
    return seen


def post(part, w, bet):
    c = cell(part, w)
    return sum(F(bet[k]) for k in c) / len(c)


VALUES = (-2, -1, 0, 1, 2)
for state, label in ((1, "state 1"), (4, "state 4")):
    M = meet(state)
    strict = 0
    strict_nonneg = 0
    nonneg_meet = 0
    nonneg_nonzero = 0
    for vals in itertools.product(VALUES, repeat=6):
        bet = {w: v for w, v in zip(STATES, vals)}
        neg = {w: -v for w, v in bet.items()}
        g1 = {w: post(PART1, w, bet) for w in STATES}
        g2 = {w: post(PART2, w, neg) for w in STATES}
        if g1[state] > 0 and g2[state] > 0:
            strict += 1
            if all(g1[w] >= 0 and g2[w] >= 0 for w in M):
                strict_nonneg += 1
        if all(g1[w] >= 0 and g2[w] >= 0 for w in M):
            nonneg_meet += 1
            if any(g1[w] != 0 or g2[w] != 0 for w in M):
                nonneg_nonzero += 1
    print(label, "meet", sorted(M), "strict", strict, "strict and nonneg on meet", strict_nonneg,
          "nonneg on meet", nonneg_meet, "with nonzero posterior", nonneg_nonzero)
