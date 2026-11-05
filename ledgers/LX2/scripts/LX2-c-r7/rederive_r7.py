"""Independent re-derivation of every number the LX2 project page states, from first principles (Fraction, random.Random)."""
import random
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP

def r4(x):  # half-up to 4 places, from the exact value
    return str(Decimal(x.numerator) / Decimal(x.denominator)).__class__ and \
        (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

def f(t): return 100 + 2 * t

# Lab 1 (months 13-20)
R1 = {13: 125, 14: 131, 15: 128, 16: 132, 17: 138, 18: 133, 19: 140, 20: 135}
e1 = {t: f(t) - R1[t] for t in R1}
hits1 = [t for t in R1 if abs(e1[t]) <= 2]
edge1 = [t for t in R1 if abs(e1[t]) == 2]
print("L1 errors", [e1[t] for t in R1], "sum", sum(e1.values()))
print("L1 hits", len(hits1), "rate", r4(Fraction(len(hits1), 8)), "bias", r4(Fraction(sum(e1.values()), 8)), "edge", edge1)
strict1 = [t for t in R1 if abs(e1[t]) < 2]
print("L1 strict-band hits", len(strict1), "rate", Fraction(len(strict1), 8), "=", float(Fraction(len(strict1), 8)))
print("L1 both signs", any(e > 0 for e in e1.values()), any(e < 0 for e in e1.values()))
print("L1 rung-1 1/8 =", r4(Fraction(1, 8)))

# Lab 2 (months 13-18)
R2 = {13: 127, 14: 126, 15: 124, 16: 131, 17: 136, 18: 141}
e2 = {t: f(t) - R2[t] for t in R2}
h2 = sum(1 for t in R2 if abs(e2[t]) <= 2)
edge2 = [t for t in R2 if abs(e2[t]) == 2]
print("L2 errors", list(e2.values()), "hits", h2, "rate", r4(Fraction(h2, 6)), "bias", r4(Fraction(sum(e2.values()), 6)), "edge", edge2)
print("L2 hit count over 8 ->", r4(Fraction(h2, 8)), "; mean abs error ->", r4(Fraction(sum(abs(v) for v in e2.values()), 6)), Fraction(sum(abs(v) for v in e2.values()), 6))
print("L2 tie check (exact, 5th place 5 and nothing after):", [str(Fraction(h2, 6)), str(Fraction(sum(e2.values()), 6))])

# Lab 3, seed 20261103
rng = random.Random(20261103)
R3 = {}
for t in range(1, 37):
    noise = rng.randint(-3, 3)
    shift = -6 if t >= 28 else 0
    R3[t] = 100 + 2 * t + noise + shift
E3 = {t: f(t) - R3[t] for t in range(1, 37)}
val = range(13, 37)
hits3 = [t for t in val if abs(E3[t]) <= 2]
edge3 = [t for t in val if abs(E3[t]) == 2]
bias3 = Fraction(sum(E3[t] for t in val), 24)
print("L3 hits", len(hits3), "rate", Fraction(len(hits3), 24), r4(Fraction(len(hits3), 24)), "bias", bias3, r4(bias3))
print("L3 edge", edge3)
mx = max(abs(E3[t]) for t in val)
print("L3 max abs err", mx, "months", [t for t in val if abs(E3[t]) == mx])
cal = Fraction(sum(E3[t] for t in range(1, 13)), 12)
print("L3 calibration sum", sum(E3[t] for t in range(1, 13)), "bias", cal, r4(cal))
print("L3 Part A errors:", [E3[t] for t in val])
s1 = [E3[t] for t in range(13, 28)]; s2 = [E3[t] for t in range(28, 37)]
print("split 13-27 sum", sum(s1), "n", len(s1), "hits", sum(1 for t in range(13, 28) if abs(E3[t]) <= 2),
      "rate", Fraction(sum(1 for t in range(13, 28) if abs(E3[t]) <= 2), 15), "bias", Fraction(sum(s1), 15))
print("split 28-36 sum", sum(s2), "n", len(s2), "min/max", min(s2), max(s2), "hits", sum(1 for t in range(28, 37) if abs(E3[t]) <= 2),
      "bias", Fraction(sum(s2), 9))
print("split total", sum(s1) + sum(s2), "vs C", sum(E3[t] for t in val))
print("rolling 12 at month 36 (errors 25-36):", sum(E3[t] for t in range(25, 37)), Fraction(sum(E3[t] for t in range(25, 37)), 12), r4(Fraction(sum(E3[t] for t in range(25, 37)), 12)))
strict3 = [t for t in val if abs(E3[t]) < 2]
print("L3 strict hits", len(strict3), Fraction(len(strict3), 24), "=", r4(Fraction(len(strict3), 24)))
print("L3 forecast-minus-realised min/max from month 28:", min(E3[t] for t in range(28, 37)), max(E3[t] for t in range(28, 37)))
print("L3 realised months 13-20", [R3[t] for t in range(13, 21)])
print("L1 vs L3 agreement months 13-20:", [t for t in range(13, 21) if R1[t] == R3[t]])
print("L2 vs L3 agreement months 13-18:", [t for t in range(13, 19) if R2[t] == R3[t]])
print("L2 realised", [R2[t] for t in range(13, 19)], "L3 realised", [R3[t] for t in range(13, 19)])
print("month 13-27 counts: months with |e|<=2 in 13-27:", sum(1 for t in range(13, 28) if abs(E3[t]) <= 2))
print("E3 months 13-27 errors within [-3,3]:", all(-3 <= E3[t] <= 3 for t in range(13, 28)))
print("R3 realised 1-36 positive:", all(R3[t] > 0 for t in R3))
print("L3 calibration errors", [E3[t] for t in range(1, 13)])
