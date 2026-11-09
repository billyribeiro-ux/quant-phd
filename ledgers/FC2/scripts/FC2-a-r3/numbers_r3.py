"""Round 3 FC2-a: independent recomputation of the numbers printed in the slice (Fraction/Decimal, own code)."""

from __future__ import annotations

import math
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import product

getcontext().prec = 50


def D(x):
    return Decimal(x)


print("== L01 lab counts (own brute force, Fraction, box -10..10, SMALL -2..2)")
bond_u, stock_u = Fraction(1), Fraction(3)
bond_d, stock_d = Fraction(1), Fraction(1)
X = [[bond_u, stock_u], [bond_d, stock_d]]  # rows states u,d; cols bond, stock


def pay(h):
    return [h[0] * X[s][0] + h[1] * X[s][1] for s in range(2)]


def cost(h, p):
    return h[0] * p[0] + h[1] * p[1]


def arb(h, p):
    c = cost(h, p)
    pl = pay(h)
    if c <= 0 and all(x >= 0 for x in pl) and (c < 0 or any(x > 0 for x in pl)):
        return True
    return False


box = range(-10, 11)
for label, p in [("A consistent", [Fraction(9, 10), Fraction(1)]), ("B mispriced", [Fraction(9, 10), Fraction(1, 2)])]:
    n_arb = sum(1 for h in product(box, box) if arb(h, p))
    small = list(product(range(-2, 3), range(-2, 3)))
    dom = bad = 0
    for a in small:
        for b in small:
            pa, pb = pay(a), pay(b)
            if all(x >= y for x, y in zip(pa, pb)):
                dom += 1
                if cost(a, p) < cost(b, p):
                    bad += 1
    print(label, "arb in box", n_arb, "dominance pairs", dom, "misordered", bad)
# state prices
p = [Fraction(9, 10), Fraction(1, 2)]
det = X[0][0] * X[1][1] - X[1][0] * X[0][1]
psi_u = (p[0] * X[1][1] - X[1][0] * p[1]) / det
psi_d = (X[0][0] * p[1] - X[0][1] * p[0]) / det
print("mispriced state prices", psi_u, psi_d, "det", det)
print("zero-cost holdings with box", [h for h in product(box, box) if cost(h, p) == 0 and all(x > 0 for x in pay(h))][:3])
print("arb (-5,9) payoff", pay((-5, 9)), "cost", cost((-5, 9), p))

print("\n== L01 Example 3.4 / Prop 3.5 / R1 / misconception numbers")
q = Fraction(1)
pp = [Fraction(9, 10), q]
psi_u = (q - Fraction(9, 10)) / 2
psi_d = (Fraction(27, 10) - q) / 2
print("q=1 psi_u", psi_u, "psi_d", psi_d, "sum", psi_u + psi_d)
print("misconception1 cost", 1 - 2 * Fraction(9, 10), "payoff u", -2 * 1 + 1 * 3, "d", -2 + 1)
print("M2 psi (bond 4/5, stock 1)", (Fraction(1) - Fraction(4, 5)) / 2, Fraction(4, 5) - (Fraction(1) - Fraction(4, 5)) / 2)
print("M1 cost 2 bonds -1 stock", 2 * Fraction(9, 10) - 1, "payoff", 2 - 3, 2 - 1)
print("E2 zero cost (-5,9) at stock 1/2 cost", -5 * Fraction(9, 10) + 9 * Fraction(1, 2))

print("\n== L02 numbers")
F = D(50) * D(math.exp(0.025))
print("50e^0.025 =", F, "round cents", F.quantize(D("0.01")))
print("M1 e^0.025 to 10", "%.10f" % math.exp(0.025), "50*that", "%.6f" % (50 * math.exp(0.025)))
F2 = D(80) * D(math.exp(0.01))
print("80e^0.01 =", F2, "profit", D(81) - F2)
print("M3 100e^-0.015 =", D(100) * D(math.exp(-0.015)), "value", D(104) - D(100) * D(math.exp(-0.015)))
Fw = D(5000) * D(math.exp(0.025))
print("L02 fair cents", Fw, "quote gain", D(5200) - Fw)
print("E3 value 5300 - F e^{-0.0125} =", D(5300) - Fw * D(math.exp(-0.0125)), "discounted", Fw * D(math.exp(-0.0125)))
print("R3 e^0.1", D(math.exp(0.1)), "1.05^2", D("1.1025"), "diff", D(math.exp(0.1)) - D("1.1025"))
print("quiz e^0.1 to 4 places", round(math.exp(0.1), 4))
for s in [3000, 4500, 6000, 7500]:
    print("replication", s, D(s) - Fw)

print("\n== L03 numbers")
rates = [Fraction(3, 100), Fraction(7, 200), Fraction(4, 100), Fraction(9, 200), Fraction(5, 100)]
dfs = [Fraction(1)]
for i, z in enumerate(rates, 1):
    dfs.append(1 / (1 + z) ** i)
annuity = sum(dfs[1:], Fraction(0))
R = (1 - dfs[5]) / annuity
print("DFs", [round(float(d), 6) for d in dfs[1:]])
print("annuity", float(annuity), "par", float(R), "par exact decimal", D(R.numerator) / D(R.denominator))
pay_cents = R * 100_000_000
print("payment cents unrounded", D(pay_cents.numerator) / D(pay_cents.denominator))
print("value to payer cents", float(-Fraction(1, 100) * annuity * 100_000_000))
print("par - each zero rate", [float(R - z) for z in rates])
print("M2 DF3 1.06^-3", 1 / 1.06 ** 3, "round 6", round(1 / 1.06 ** 3, 6))
dfM3 = [1 / 1.06, 1 / 1.06**2, 1 / 1.06**3]
print("M3 DFs", dfM3, "sum", sum(dfM3), "display sum", round(dfM3[0], 6) + round(dfM3[1], 6) + round(dfM3[2], 6))
print("M3 value per 100", 100 * (0.06 - 0.05) * sum(dfM3))
f1 = Fraction(1) / 1
print("R3 DF1, DF2, par")
d1 = 1 / Fraction(103, 100)
d2 = d1 / Fraction(105, 100)
print(float(d1), float(d2), float((1 - d2) / (d1 + d2)), "flat3 DF2", 1 / 1.03**2)
print("E1 margins", [b - a for a, b in zip([5000, 5039, 5070, 5104, 5069, 5103, 5090, 5054, 5077, 5106, 5084], [5039, 5070, 5104, 5069, 5103, 5090, 5054, 5077, 5106, 5084])])
print("P2 check -0.01*annuity*N", -Fraction(1, 100) * annuity * 100_000_000)
