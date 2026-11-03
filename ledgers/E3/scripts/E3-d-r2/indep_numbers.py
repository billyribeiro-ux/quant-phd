"""Independent re-derivation of Lab 1, Lab 2 and Lab 3 printed numbers (Decimal for CEs, scipy for Lab 3)."""
from decimal import Decimal as D, getcontext, ROUND_FLOOR
from fractions import Fraction as F
import math
getcontext().prec = 60

GAMMA, LAM, KAPPA, WEALTH = D("0.40"), D("2.00"), D("1.50"), D(100000)
def dpow(x, e):
    return x ** e
def cents_half_up(x):
    return int((x + D("0.5")).to_integral_value(rounding=ROUND_FLOOR))
def crra_ce(prizes, probs, g):
    exp_u = sum(D(p.numerator) / D(p.denominator) * dpow(WEALTH + D(x), 1 - g) for x, p in zip(prizes, probs))
    return dpow(exp_u, 1 / (1 - g)) - WEALTH
def pv(x, g, lam):
    x = D(x)
    if x >= 0:
        return dpow(x, 1 - g)
    return -lam * dpow(-x, 1 - g)
def prospect_ce(prizes, probs, g, lam):
    V = sum(D(p.numerator) / D(p.denominator) * pv(x, g, lam) for x, p in zip(prizes, probs))
    if V >= 0:
        return dpow(V, 1 / (1 - g))
    return -dpow(-V / lam, 1 / (1 - g))
def pa_of(ca, cb, k):
    z = k * (ca - cb) / D(10000)
    return 1 / (1 + (-z).exp())
pairs = [
    ([2000, -1000], [F(1, 2), F(1, 2)], [500], [F(1)], "A"),
    ([3000], [F(1)], [4000, -2000], [F(1, 4), F(3, 4)], "B"),
    ([1500, 2500], [F(1, 3), F(2, 3)], [-500, 3000], [F(1, 2), F(1, 2)], "A"),
]
tot = D(0)
for pa, qa, pb, qb, ch in pairs:
    ca_c, cb_c = crra_ce(pa, qa, GAMMA), crra_ce(pb, qb, GAMMA)
    ca, cb = prospect_ce(pa, qa, GAMMA, LAM), prospect_ce(pb, qb, GAMMA, LAM)
    p = pa_of(ca, cb, KAPPA)
    pc = p if ch == "A" else 1 - p
    tot += pc.ln()
    print("CRRA exact", float(ca_c), float(cb_c), "cents", cents_half_up(ca_c), cents_half_up(cb_c),
          "| prospect exact", float(ca), float(cb), "cents", cents_half_up(ca), cents_half_up(cb),
          "| P(A)", round(float(p), 6), "logP(chosen)", round(float(pc.ln()), 6))
print("total loglik", round(float(tot), 6))
# Lab 2
z = D(2) * (D(1500) - D(2200)) / D(10000)
print("Lab2 z", z, "logA", float(-(1 + (-z).exp()).ln()), "logB", float(-(1 + z.exp()).ln()))
