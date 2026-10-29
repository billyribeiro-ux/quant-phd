"""Independent recomputation of the numbers printed in L07 and L08 (decimal, 40 digits; exact fractions).

Usage: python -I ledgers/E3/scripts/E3-c-r3/recheck_L07_L08_numbers.py
"""

from __future__ import annotations

import math
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 50
D = Decimal


def sqrt(x: Decimal) -> Decimal:
    return x.sqrt()


def omega(p: Decimal) -> Decimal:
    """omega_{1/2}(p) = sqrt(p) / (1 + 2 sqrt(p(1-p)))."""
    return sqrt(p) / (1 + 2 * sqrt(p * (1 - p)))


def omega_general(p: Decimal) -> Decimal:
    """p**eta / (p**eta + (1-p)**eta)**(1/eta) at eta = 1/2, computed as in the lab."""
    s, t = sqrt(p), sqrt(1 - p)
    return s / (s + t) ** 2


print("== L07 weights ==")
for name, p in [("0.01", D("0.01")), ("0.05", D("0.05")), ("0.3", D("0.3")), ("0.5", D("0.5")),
                ("0.6", D("0.6")), ("0.95", D("0.95")), ("0.99", D("0.99")), ("1/4", D(1) / 4)]:
    print(f"omega({name}) = {omega(p):.12f}")
print("omega(1/2) exact 1/(2 sqrt 2) =", f"{D(1)/(2*sqrt(D(2))):.12f}")
w3, w6 = omega(D("0.3")), omega(D("0.6"))
print("2*omega(0.3) =", f"{2*w3:.12f}", " (text says 0.57158177)")
print("omega(0.3)/omega(0.6) =", f"{w3/w6:.12f}", " (text says 0.73045450)")
print("threshold alpha=1 =", f"{1/(1+D(2)**-1):.12f}", " alpha=1/2 =", f"{1/(1+D(2)**(D(-1)/2)):.12f}  (text 0.58578644)")
print("omega(0.3)*150 =", f"{w3*150:.12f}", " (text 42.86863274)")
print("omega(0.6)*100 =", f"{w6*100:.12f}", " (text 39.12507700)")
print("difference =", f"{w3*150 - w6*100:.12f}", " rounded", f"{(w3*150 - w6*100):.4f}", " printed diff of 4dp values 42.8686-39.1251 =", f"{42.8686-39.1251:.4f}")
print("alpha=1/2: omega(0.3)*(sqrt50+10) =", f"{w3*(sqrt(D(50))+10):.8f}", " omega(0.6)*10 =", f"{w6*10:.8f}")
print("ratio of 0.28579088/0.39125077 =", f"{D('0.28579088')/D('0.39125077'):.10f}")

# Misconception 3, lottery L: 100 CU w.p. 0.01, 50 CU w.p. 0.99
w01, w99 = omega(D("0.01")), omega(D("0.99"))
wv = w01 * 100 + w99 * 50
print("omega(0.01) =", f"{w01:.10f}", "omega(0.99) =", f"{w99:.10f}")
print("weighted value =", f"{wv:.6f}", " EV = 50.5 ; net =", f"{wv-D('50.5'):.6f}")
print("overweight 0.01:", f"{(w01-D('0.01'))*100:.6f}", " underweight 0.99:", f"{(D('0.99')-w99)*50:.6f}")

# Observation 1.5 grid: sign changes, last point above, monotone
grid = [Fraction(i, 1000) for i in range(1001)]
gvals = [omega(D(g.numerator) / D(g.denominator)) for g in grid]
gp = [D(g.numerator) / D(g.denominator) for g in grid]
mono = all(gvals[i] <= gvals[i + 1] for i in range(1000))
above = [gvals[i] > gp[i] for i in range(1, 1000)]
changes = sum(1 for i in range(len(above) - 1) if above[i] != above[i + 1])
last_above = max(i for i in range(1, 1000) if gvals[i] > gp[i])
print("monotone on grid:", mono, "| sign changes interior:", changes, "| last grid index above:", last_above, grid[last_above])
print("omega-p at 0.278 =", f"{gvals[278]-gp[278]:.3e}", " at 0.279 =", f"{gvals[279]-gp[279]:.3e}")
# bisection on the exact function for the crossing
lo, hi = D("0.27"), D("0.29")
for _ in range(200):
    mid = (lo + hi) / 2
    if omega(mid) > mid:
        lo = mid
    else:
        hi = mid
print("crossing of omega(p)=p (bisection, 50 digits) =", f"{lo:.12f}")

print("== L07 M1 / P1 ==", f"{omega(D(1)/4):.12f}", " 2-sqrt3 =", f"{2-sqrt(D(3)):.12f}")
print("== L07 misc ==", f"{omega(D(1)/2)*100:.9f}")

print("== L08 ==")
ce_eu = Fraction(4180000, 41)
print("EU CE exact", ce_eu, float(ce_eu))
# prospect
v_gain, v_loss = math.sqrt(100), -2 * math.sqrt(50)
V = D("0.5") * D(10) + D("0.5") * (-2 * sqrt(D(50)))
print("prospect V =", f"{V:.12f}")
inv = -((-V / 2) ** 2)
print("prospect CE change (CU) =", f"{inv:.12f}", " wealth cents =", f"{100000 + 100*inv:.10f}")
print("change in cents =", f"{-100*inv:.10f}")
# maxmin and alpha-MEU
g = lambda p: Fraction(p) / 110000 + (1 - Fraction(p)) / 95000  # noqa: E731
print("maxmin CE (p=1/3) =", float(1 / g(Fraction(1, 3))), " exact", 1 / g(Fraction(1, 3)))
print("EU CE at p=1/4 =", float(1 / g(Fraction(1, 4))), " exact", 1 / g(Fraction(1, 4)))
print("CE at p=3/4 =", f"{float(1 / g(Fraction(3, 4))):.6f}")
print("two-urn known red (1/3, 110000/100000):", 1 / (Fraction(1, 3) / 110000 + Fraction(2, 3) / 100000))
print("two-urn known black (2/3):", float(1 / (Fraction(2, 3) / 110000 + Fraction(1, 3) / 100000)))
print("risk premium exact:", Fraction(102500) - ce_eu, float(Fraction(102500) - ce_eu))
print("prior 1/4 vs 3/4 maxmin:", float(min(1 / g(Fraction(1, 4)), 1 / g(Fraction(3, 4)))))
print("M1 expected wealth 98750; CE", float(1 / g(Fraction(1, 4))))
