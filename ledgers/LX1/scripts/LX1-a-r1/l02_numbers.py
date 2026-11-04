"""LX1-a r1 independent recomputation of L02 prose numbers: exact Fractions, rebuilt from the printed changes."""
from fractions import Fraction as Fr
from decimal import Decimal, getcontext
import math
getcontext().prec = 60
changes = [-1, 1, 1, 3, -4, -1, 2, -4, -3, 3, 2, -4]  # printed in lab Part A, t = 1..12
P = [Fr(100)]
for c in changes:
    P.append(P[-1] * (1 + Fr(c, 100)))
def rhu(x): return math.floor(x + Fr(1, 2))
D = 1_000_000
V = [Fr(D) * 100 / p for p in P]
print("P12 exact", P[12], float(P[12]), "decimal", Decimal(P[12].numerator) / Decimal(P[12].denominator))
print("100/P12 exact", float(Fr(100) / P[12]), "decimal", Decimal(100) / (Decimal(P[12].numerator) / Decimal(P[12].denominator)))
print("printed-index ratio 100/94.7051 =", Decimal(100) / Decimal("94.7051"))
print("V rounded", [rhu(v) for v in V])
steps = [rhu(V[t]) - rhu(V[t - 1]) for t in range(1, 13)]
print("steps", steps, "max", max(steps), "at t", steps.index(max(steps)) + 1)
falls = [t for t in range(1, 13) if P[t] < P[t - 1]]
rises = [t for t in range(1, 13) if V[t] > V[t - 1]]
print("falls", falls, len(falls), "rises", rises, len(rises), "equal", falls == rises)
print("V1 check 2000*100/95", float(Fr(200000, 95)), "V1 M1", Fr(2000 * 100, 80), "M2 90/85", Fr(90, 85))
print("E2 1000000*100/99", float(Fr(100000000, 99)))
print("ratio V12/V0 six dp", float(V[12] / V[0]), rhu(V[12]), "at 1e6 scale", V[12] / V[0])
print("identity (a) all", all(V[t] / V[t - 1] == P[t - 1] / P[t] for t in range(1, 13)))
print("nonzero changes", all(c != 0 for c in changes))
print("R3 check P0/P12 vs 1.055909", float(P[0] / P[12]))
print("18/17", Decimal(18) / Decimal(17))
print("CU", D / 100, "CU")
