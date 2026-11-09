"""Independent re-derivation of the numbers printed on the changed or added L07 to L09 cards (E4-c round 1).

Written from the lesson formulas, not from the lab twins. Exact arithmetic where possible.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction as F


def rho2(sv2: F, se2: F, a: F, lam: F, su2: F) -> F:
    tau_v, tau_e = 1 / sv2, 1 / se2
    kappa = a * se2 / lam
    tau_eta = 1 / (se2 + kappa * kappa * su2)
    tau_bar = lam * tau_e + (1 - lam) * tau_eta
    th_s = tau_bar / (tau_v + tau_bar)
    th_u = kappa * th_s
    cov = th_s * sv2
    var_p = th_s * th_s * (sv2 + se2) + th_u * th_u * su2
    return cov * cov / (sv2 * var_p)


def var_p(sv2: F, se2: F, a: F, lam: F, su2: F) -> F:
    tau_v, tau_e = 1 / sv2, 1 / se2
    kappa = a * se2 / lam
    tau_eta = 1 / (se2 + kappa * kappa * su2)
    tau_bar = lam * tau_e + (1 - lam) * tau_eta
    th_s = tau_bar / (tau_v + tau_bar)
    return th_s * th_s * (sv2 + se2) + (kappa * th_s) ** 2 * su2


print("== c142 / c147 / c148 / c140: base instance sv2=se2=1, a=1, lam=1/2, sd grid")
for sd in [F(1, 4), F(1, 2), F(1), F(2), F(4)]:
    r = rho2(F(1), F(1), F(1), F(1, 2), sd * sd)
    print("sd", sd, "rho2", r, "var_p", var_p(F(1), F(1), F(1), F(1, 2), sd * sd))
print("c148 tau_eta at base instance (su2=1/4):", 1 / (1 + (F(1) / F(1, 2)) ** 2 * F(1, 4)))
print("c140 Var(p) identity at base, su2=1/4:", var_p(F(1), F(1), F(1), F(1, 2), F(1, 4)))

print("== c150: lam sweep at sd=1/2")
print([str(rho2(F(1), F(1), F(1), l, F(1, 4))) for l in [F(1, 4), F(1, 2), F(3, 4)]])

print("== c139 / Remark 7.8: rho2 < benchmark for su2>0, tends to it")
bench = F(1, 2)
for su2 in [F(1, 10000), F(1, 100), F(1)]:
    print("su2", su2, "rho2", float(rho2(F(1), F(1), F(1), F(1, 2), su2)), "bench", float(bench), "below", rho2(F(1), F(1), F(1), F(1, 2), su2) < bench)

print("== Example 1.1 (a=2, sv2=se2=su2=1): G(0), G(1), gaps at costs 0.12 and 0.18")
G0 = math.log(2) / 4
G1 = math.log(5 / 3) / 4


def gain(lam: float, a: float = 2.0, sv2: float = 1.0, se2: float = 1.0, su2: float = 1.0) -> float:
    tau_v, tau_e = 1 / sv2, 1 / se2
    kappa = a * se2 / lam
    sig_eta2 = se2 + kappa * kappa * su2
    tau_eta = 1 / sig_eta2
    A = lam * tau_e + (1 - lam) * tau_eta
    beta = A / (tau_v + A)
    b_s = sv2 / (sv2 + se2)
    b_y = tau_eta / (tau_v + tau_eta)
    VI = 1 / (tau_v + tau_e)
    VU = 1 / (tau_v + tau_eta)
    var_DI = (b_s - beta) ** 2 * (sv2 + se2) + kappa * kappa * beta * beta * su2
    var_DU = (b_y - beta) ** 2 * (sv2 + sig_eta2)
    return math.log((1 + var_DI / VI) / (1 + var_DU / VU)) / (2 * a)


print("G(0) closed", G0, " G(1) closed", G1, " G(1) from gain(1.0)", gain(1.0), " G(0.5)", gain(0.5))
print("c183 gap at cost 0.12 (G(1)-c):", f"{G1 - 0.12:.2e}", " c262 gap at cost 0.18 (G(0)-c):", f"{G0 - 0.18:.2e}")
print("c270: G(0)=%.6f > 0.15 (case i fails)=%s ; G(1)=%.6f < 0.15 (case ii fails)=%s" % (G0, G0 > 0.15, G1, G1 < 0.15))
print("c270 interior gains equal to cost 0.15 on sigma_u^2=0 grid:")
su0 = 0.0
cnt = 0
for k in range(1, 1000):
    lam = k / 1000
    g = gain(lam, su2=su0)
    if abs(g - 0.15) < 1e-12:
        cnt += 1
print("count", cnt, " max |gain| at su2=0 over grid:", max(abs(gain(k / 1000, su2=0.0)) for k in range(1, 1000)))

print("== c260: lim Var(D_U) as lam->0+ equals a^2 su2 sv2^2 (two parameter sets)")
for a, sv2, se2, su2 in [(2.0, 1.0, 1.0, 1.0), (1.5, 2.0, 0.5, 3.0)]:
    lam = 1e-5
    tau_v, tau_e = 1 / sv2, 1 / se2
    kappa = a * se2 / lam
    sig_eta2 = se2 + kappa * kappa * su2
    tau_eta = 1 / sig_eta2
    A = lam * tau_e + (1 - lam) * tau_eta
    beta = A / (tau_v + A)
    b_y = tau_eta / (tau_v + tau_eta)
    var_DU = (b_y - beta) ** 2 * (sv2 + sig_eta2)
    print("a", a, "sv2", sv2, "se2", se2, "su2", su2, "Var(D_U) at lam=1e-5:", var_DU, " predicted a^2 su2 sv2^2 =", a * a * su2 * sv2 * sv2)

print("== c187 / c139: sigma_u=0 correlation equals sv2/(sv2+se2) and is < 1")
for lam in [F(1, 4), F(1)]:
    print("lam", lam, "rho2 at su2=0 (formula with su2=0):", rho2(F(1), F(1), F(2), lam, F(0)))

print("== c200 / c269 / c203: Example 2.4 and the bet enumeration (exact)")
states = [1, 2, 3, 4, 5, 6]
P1 = [{1, 2}, {3}, {4, 5, 6}]
P2 = [{1, 2, 3}, {4, 5}, {6}]


def cell(P, w):
    return next(c for c in P if w in c)


def meet(w):
    reach = {w}
    changed = True
    while changed:
        changed = False
        for P in (P1, P2):
            for c in P:
                if reach & c and not c <= reach:
                    reach |= c
                    changed = True
    return reach


M1 = meet(1)
print("M(1) =", sorted(M1))
x = {1: -1, 2: 2, 3: -2, 4: -2, 5: -2, 6: -2}
g1 = lambda w: F(sum(x[s] for s in cell(P1, w)), len(cell(P1, w)))
g2 = lambda w: F(sum(-x[s] for s in cell(P2, w)), len(cell(P2, w)))
print("g1(1)", g1(1), "g2(1)", g2(1), "g1(3)", g1(3), "g2(3)", g2(3))

count_nonneg = 0
count_zero = 0
count_strict1 = 0
for vals in itertools.product(range(-2, 3), repeat=6):
    xx = dict(zip(states, vals))
    gg1 = {w: F(sum(xx[s] for s in cell(P1, w)), len(cell(P1, w))) for w in states}
    gg2 = {w: F(sum(-xx[s] for s in cell(P2, w)), len(cell(P2, w))) for w in states}
    if all(gg1[w] >= 0 and gg2[w] >= 0 for w in M1):
        count_nonneg += 1
        if all(gg1[w] == 0 and gg2[w] == 0 for w in M1):
            count_zero += 1
    if gg1[1] > 0 and gg2[1] > 0:
        count_strict1 += 1
print("enumerated", 5 ** 6, "bets; nonneg on meet", count_nonneg, "; of which zero posteriors on meet", count_zero, "; strict at state 1", count_strict1)
print("c203 closed form 5*5**3 =", 5 * 5 ** 3)
