from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 60
F, C, N = Decimal(100000), Decimal(5000), 10
def cf(t): return C + (F if t == N else 0)
def P(y): return sum(cf(t) / (1 + y) ** t for t in range(1, N + 1))
def P1(y): return -sum(t * cf(t) / (1 + y) ** (t + 1) for t in range(1, N + 1))
def P2(y): return sum(t * (t + 1) * cf(t) / (1 + y) ** (t + 2) for t in range(1, N + 1))
def P3(y): return -sum(t * (t + 1) * (t + 2) * cf(t) / (1 + y) ** (t + 3) for t in range(1, N + 1))
y0 = Decimal("0.04")
print("P(y0) exact-ish", P(y0))
print("P1", P1(y0), "P2", P2(y0), "P3", P3(y0))
print("-P1/P", -P1(y0) / P(y0), "P2/P", P2(y0) / P(y0))
def T1(dy): return P(y0) + P1(y0) * dy
def T2(dy): return T1(dy) + Decimal("0.5") * P2(y0) * dy * dy
for dy in [Decimal("0.01"), Decimal("0.005"), Decimal("0.0025")]:
    e1 = P(y0 + dy) - T1(dy); e2 = P(y0 + dy) - T2(dy)
    print("dy", dy, "e1", float(e1), "e2", float(e2), "R<0 for dy>0:", e2 < 0)
for dy in [Decimal("0.01"), Decimal("-0.01")]:
    print("shift", dy, "P cents", round(P(y0 + dy), 0), "T2", float(T2(dy)), "diff", float(P(y0 + dy) - T2(dy)))
# ratios
e = {}
for dy in [Decimal("0.01"), Decimal("0.005"), Decimal("0.0025")]:
    e[dy] = (P(y0 + dy) - T1(dy), P(y0 + dy) - T2(dy))
ks = list(e)
print("ratio1", float(e[ks[0]][0] / e[ks[1]][0]), float(e[ks[1]][0] / e[ks[2]][0]))
print("ratio2", float(e[ks[0]][1] / e[ks[1]][1]), float(e[ks[1]][1] / e[ks[2]][1]))
# sign of third derivative and Prop 3.3 check on grid
import itertools
ok = all(P(y0 + Decimal(d)) - T1(Decimal(d)) >= 0 for d in ["-0.03","-0.01","-0.001","0.001","0.05","0.5","3"] if y0 + Decimal(d) > -1)
print("prop3.3 on grid", ok)
