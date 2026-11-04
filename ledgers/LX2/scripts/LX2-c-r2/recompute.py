# Independent recomputation (own Fraction code; does not import the lab twin).
import random
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP

def half_up(x, places=4):
    q = Decimal(x.numerator) / Decimal(x.denominator)
    return str(q.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))

def f(t): return 100 + 2 * t

# Rung 1: months 13..20
R1 = [125, 131, 128, 132, 138, 133, 140, 135]
e1 = [f(13 + i) - y for i, y in enumerate(R1)]
h1 = sum(1 for e in e1 if abs(e) <= 2)
print("R1 errors", e1, "hits", h1, "of", len(e1), "rate", half_up(Fraction(h1, 8)), "bias", half_up(Fraction(sum(e1), 8)),
      "edge", [13 + i for i, e in enumerate(e1) if abs(e) == 2], "strict hits", sum(1 for e in e1 if abs(e) < 2),
      "strict rate", half_up(Fraction(sum(1 for e in e1 if abs(e) < 2), 8)))

# Rung 2: months 13..18
R2 = [127, 126, 124, 131, 136, 141]
e2 = [f(13 + i) - y for i, y in enumerate(R2)]
h2 = sum(1 for e in e2 if abs(e) <= 2)
print("R2 errors", e2, "hits", h2, "rate", half_up(Fraction(h2, 6)), "bias", half_up(Fraction(sum(e2), 6)),
      "edge", [13 + i for i, e in enumerate(e2) if abs(e) == 2],
      "hit count over 8", half_up(Fraction(h2, 8)), "mean abs", half_up(Fraction(sum(abs(e) for e in e2), 6)),
      "truncated 4dp rate", Fraction(int(Fraction(h2, 6) * 10000), 10000))

# Lab 3: seed 20261103, t=1..36, noise randint(-3,3) per month in order, -6 from 28
rng = random.Random(20261103)
real = {}
for t in range(1, 37):
    noise = rng.randint(-3, 3)
    real[t] = 100 + 2 * t + noise + (-6 if t >= 28 else 0)
E = {t: f(t) - real[t] for t in range(1, 37)}
V = range(13, 37)
hits = sum(1 for t in V if abs(E[t]) <= 2)
print("L3 realised", [real[t] for t in range(1, 37)])
print("L3 errors 13..36", [E[t] for t in V])
print("L3 hits", hits, "of", len(V), "rate", half_up(Fraction(hits, 24)), "bias", half_up(Fraction(sum(E[t] for t in V), 24)),
      "sum", sum(E[t] for t in V))
print("L3 edge", [t for t in V if abs(E[t]) == 2])
worst = max(V, key=lambda t: (abs(E[t]), -t))
print("L3 largest abs error", abs(E[worst]), "month", worst, "months with that error", [t for t in range(1, 37) if abs(E[t]) == abs(E[worst])])
cal = [E[t] for t in range(1, 13)]
print("L3 calibration sum", sum(cal), "bias", half_up(Fraction(sum(cal), 12)))
a = [E[t] for t in range(13, 28)]; b = [E[t] for t in range(28, 37)]
print("split 13-27: n", len(a), "sum", sum(a), "bias", half_up(Fraction(sum(a), 15)), "hits", sum(1 for e in a if abs(e) <= 2),
      "rate", half_up(Fraction(sum(1 for e in a if abs(e) <= 2), 15)), "exact 13/15", Fraction(sum(1 for e in a if abs(e) <= 2), 15))
print("split 28-36: n", len(b), "sum", sum(b), "bias", half_up(Fraction(sum(b), 9)), "hits", sum(1 for e in b if abs(e) <= 2),
      "rate", half_up(Fraction(sum(1 for e in b if abs(e) <= 2), 9)))
print("post-change error range", min(abs(e) for e in b), max(abs(e) for e in b), "post-change all misses:", all(abs(e) > 2 for e in b))
r12 = [E[t] for t in range(25, 37)]
print("rolling 12-month bias at 36: sum", sum(r12), "/12 =", half_up(Fraction(sum(r12), 12)), Fraction(sum(r12), 12))
print("strict band hits (L3)", sum(1 for t in V if abs(E[t]) < 2), "rate", half_up(Fraction(sum(1 for t in V if abs(E[t]) < 2), 24)))
print("13/24 =", half_up(Fraction(13, 24)), " 51/24 =", half_up(Fraction(51, 24)), " 54/9 =", Fraction(54, 9), " 56/12 =", Fraction(56, 12))
print("Lab 3 first-line 13/15 =", half_up(Fraction(13, 15)), "-3/15 =", half_up(Fraction(-3, 15)), " 2.8333 check =", half_up(Fraction(17, 6)))
