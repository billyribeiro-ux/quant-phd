# Independent recomputation of numbers printed in CF8 L02 prose (hub/lesson), using exact fractions and floats.
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP
import math

def q2(x):  # round half up to 2 decimals
    return Decimal(repr(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def simple(d, gap):
    return d / (1 - d) * F(365, gap)

def comp(d, gap):
    return (1 / (1 - d)) ** (365 / gap) - 1

for lab, d, gap in [("2/10n30", F(2,100), 20), ("1/10n30", F(1,100), 20), ("2/10n60", F(2,100), 50), ("3/15n45", F(3,100), 30), ("1/15n45", F(1,100), 30), ("2/10n60b", F(2,100), 50), ("0.5% 50d", F(5,1000), 50)]:
    s = simple(d, gap)
    print(lab, "simple %", float(s*100), "compound %", comp(float(d), gap)*100)

A = lambda r, n: sum((1 + r) ** -t for t in range(1, n + 1))
# Example 3.4 / Lab B
rev0, N0, N1, dR, r = F(12_000_000), 30, 45, F(1_500_000), F(1, 10)
dI = ((rev0 + dR) * N1 - rev0 * N0) / 365
print("dI exact", float(dI), "m*", float(r * dI / dR))
def npv(m, dR, dI, n, rr):
    return -dI + m * dR * sum((1 + rr) ** -t for t in range(1, n + 1)) + dI * (1 + rr) ** -n
print("NPV 5pct exact", float(npv(F(5, 100), dR, dI, 5, r)))
# M2
rev0, N0, N1, dR, r = F(6_000_000), 30, 60, F(600_000), F(8, 100)
dI = ((rev0 + dR) * N1 - rev0 * N0) / 365
print("M2 dI", float(dI), "m*", float(r * dI / dR) * 100)
n = 4
print("M3 terms", float(-dI), float(F(10,100) * dR * sum((1 + r) ** -t for t in range(1, n+1))), float(dI * (1 + r) ** -n))
print("M3 NPV exact", float(npv(F(10,100), dR, dI, n, r)))
# R1
annu = sum((1 + r) ** -t for t in range(1, n + 1))
mnr = dI / (dR * annu)
print("R1 mnr", float(mnr) * 100, "ratio", float(1 / (1 - (1 + r) ** -n)))
# E2
rev0, N0, N1, dR, r, m = F(20_000_000), 30, 45, F(2_000_000), F(9, 100), F(6, 100)
dI = ((rev0 + dR) * N1 - rev0 * N0) / 365
print("E2 dI", float(dI), "m*", float(r*dI/dR)*100)
print("E2 NPV", float(npv(m, dR, dI, 3, r)), "A(0.09,3)", float(sum((1+r)**-t for t in range(1,4))))
# E2 alt: check NPV in percent-of-dollars with exact rational
# Problem E1 cost 37.24 etc
print("1/15n45 simple", float(simple(F(1,100), 30)*100), "2/10n60", float(simple(F(2,100), 50)*100))
