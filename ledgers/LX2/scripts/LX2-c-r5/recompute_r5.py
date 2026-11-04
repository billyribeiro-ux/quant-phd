"""Independent recomputation of every number on project.html (exact Fractions, separate code path from the labs)."""
import random
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

def r4(x):
    return Decimal(x.numerator) / Decimal(x.denominator)  # exact decimal of the fraction
def rnd(x, places=4):
    q = Decimal(1).scaleb(-places)
    return str(Decimal(x.numerator) / Decimal(x.denominator) if False else (Decimal(x.numerator) / Decimal(x.denominator)).quantize(q, rounding=ROUND_HALF_UP))

def fc(t):
    return 100 + 2 * t

# Lab 1: months 13-20
R1 = [125, 131, 128, 132, 138, 133, 140, 135]
e1 = [fc(13 + i) - y for i, y in enumerate(R1)]
h1 = [abs(e) <= 2 for e in e1]
print("L1 errors", e1, "hits", sum(h1), "hit rate", rnd(F(sum(h1), 8)), "bias", rnd(F(sum(e1), 8)), "sum", sum(e1))
print("L1 edge", [13 + i for i, e in enumerate(e1) if abs(e) == 2], "strict hits", sum(abs(e) < 2 for e in e1), "strict rate", rnd(F(sum(abs(e) < 2 for e in e1), 8)), "one hit", rnd(F(1, 8)))
# Lab 2: months 13-18
R2 = [127, 126, 124, 131, 136, 141]
e2 = [fc(13 + i) - y for i, y in enumerate(R2)]
h2 = [abs(e) <= 2 for e in e2]
print("L2 errors", e2, "hits", sum(h2), "rate", rnd(F(sum(h2), 6)), "bias", rnd(F(sum(e2), 6)), "mean abs", rnd(F(sum(abs(e) for e in e2), 6)), "strict", rnd(F(sum(abs(e) < 2 for e in e2), 6)), "edge", [13 + i for i, e in enumerate(e2) if abs(e) == 2])
print("L2 hit count over 8", rnd(F(sum(h2), 8)), "truncated 0.6666 check", rnd(F(sum(h2), 6)))
# Lab 3: seeded
rng = random.Random(20261103)
real = {}
for t in range(1, 37):
    noise = rng.randint(-3, 3)
    shift = -6 if t >= 28 else 0
    real[t] = 100 + 2 * t + noise + shift
e3 = {t: fc(t) - real[t] for t in range(13, 37)}
hits = [t for t in e3 if abs(e3[t]) <= 2]
print("L3 hits", len(hits), "of 24 rate", rnd(F(len(hits), 24)), "bias", rnd(F(sum(e3.values()), 24)), "sum", sum(e3.values()))
print("L3 edge", [t for t in e3 if abs(e3[t]) == 2])
worst = max(e3, key=lambda t: (abs(e3[t]), -t))
print("L3 worst", abs(e3[worst]), "month", worst, "ties at max", [t for t in e3 if abs(e3[t]) == abs(e3[worst])])
cal = [fc(t) - real[t] for t in range(1, 13)]
print("L3 calibration sum", sum(cal), "bias", rnd(F(sum(cal), 12)), "integer sums printing 0.9167 over 12:", [s for s in range(-200, 200) if rnd(F(s, 12)) == "0.9167"])
print("L3 months 13-27 sum", sum(e3[t] for t in range(13, 28)), "hits", sum(abs(e3[t]) <= 2 for t in range(13, 28)), "bias", rnd(F(sum(e3[t] for t in range(13, 28)), 15)), "rate", rnd(F(sum(abs(e3[t]) <= 2 for t in range(13, 28)), 15)))
print("L3 months 28-36 sum", sum(e3[t] for t in range(28, 37)), "bias", rnd(F(sum(e3[t] for t in range(28, 37)), 9)), "hits", sum(abs(e3[t]) <= 2 for t in range(28, 37)))
print("L3 errors 28-36 min/max", min(e3[t] for t in range(28, 37)), max(e3[t] for t in range(28, 37)))
print("L3 rolling bias month 36 (25-36) sum", sum(e3[t] for t in range(25, 37)), "rate", rnd(F(sum(e3[t] for t in range(25, 37)), 12)))
print("L3 strict hits", sum(abs(e3[t]) < 2 for t in e3), "strict rate", rnd(F(sum(abs(e3[t]) < 2 for t in e3), 24)))
print("L3 13/24 =", rnd(F(13, 24)), " 13/15 =", rnd(F(13, 15)), " -3/15 =", rnd(F(-3, 15)), " 54/9 =", rnd(F(54, 9)), " 56/12 =", rnd(F(56, 12)), " 51/24 =", rnd(F(51, 24)))
print("L3 Part A lines (t, fc, real, err, hit):")
for t in range(13, 37):
    print(t, fc(t), real[t], fc(t) - real[t], "yes" if abs(fc(t) - real[t]) <= 2 else "no")
