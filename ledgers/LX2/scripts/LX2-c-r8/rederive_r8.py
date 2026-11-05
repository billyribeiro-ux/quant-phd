"""Independent re-derivation of every number on the project page (no import of the lab twins)."""
import random
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP

def fc(t): return 100 + 2 * t

def hit(e): return abs(e) <= 2

def r4(x):  # half-up to 4 dp, exact
    return (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

# Lab 1
R1 = {13: 125, 14: 131, 15: 128, 16: 132, 17: 138, 18: 133, 19: 140, 20: 135}
e1 = {t: fc(t) - R1[t] for t in R1}
h1 = sum(hit(e) for e in e1.values())
print("L1 errors", [e1[t] for t in sorted(e1)], "hits", h1, "rate", r4(Fraction(h1, 8)), "bias", r4(Fraction(sum(e1.values()), 8)),
      "edge", [t for t in sorted(e1) if abs(e1[t]) == 2], "strict-band hits", sum(abs(e) < 2 for e in e1.values()))
# Lab 2
R2 = {13: 127, 14: 126, 15: 124, 16: 131, 17: 136, 18: 141}
e2 = {t: fc(t) - R2[t] for t in R2}
h2 = sum(hit(e) for e in e2.values())
print("L2 errors", [e2[t] for t in sorted(e2)], "hits", h2, "rate", r4(Fraction(h2, 6)), "bias", r4(Fraction(sum(e2.values()), 6)),
      "edge", [t for t in sorted(e2) if abs(e2[t]) == 2], "abs-mean", r4(Fraction(sum(abs(e) for e in e2.values()), 6)),
      "hit/8", r4(Fraction(h2, 8)), "ceil-as-half-up differs?", r4(Fraction(h2, 6)) == Decimal("0.6667"))
# Lab 3
rng = random.Random(20261103)
R3 = {}
for t in range(1, 37):
    n = rng.randint(-3, 3)
    R3[t] = 100 + 2 * t + n + (-6 if t >= 28 else 0)
E = {t: fc(t) - R3[t] for t in range(13, 37)}
H = len(E)
hits = sum(hit(e) for e in E.values())
bias = Fraction(sum(E.values()), H)
cal = Fraction(sum(fc(t) - R3[t] for t in range(1, 13)), 12)
print("L3 hits", hits, "H", H, "rate", r4(Fraction(hits, H)), "bias", r4(bias), "sum", sum(E.values()))
print("L3 calibration sum", sum(fc(t) - R3[t] for t in range(1, 13)), "cal bias", r4(cal))
print("L3 edge", [t for t in E if abs(E[t]) == 2], "E-max", max(abs(v) for v in E.values()), [t for t in E if abs(E[t]) == 8])
print("L3 13-27 sum", sum(E[t] for t in range(13, 28)), "hits", sum(hit(E[t]) for t in range(13, 28)), "rate", r4(Fraction(sum(hit(E[t]) for t in range(13, 28)), 15)))
print("L3 28-36 sum", sum(E[t] for t in range(28, 37)), "hits", sum(hit(E[t]) for t in range(28, 37)))
print("L3 28-36 min/max abs", min(E[t] for t in range(28, 37)), max(E[t] for t in range(28, 37)), "all positive", all(E[t] > 0 for t in range(28, 37)))
print("L3 rolling 12 at 36 (25..36)", sum(E[t] for t in range(25, 37)), r4(Fraction(sum(E[t] for t in range(25, 37)), 12)))
print("L3 strict-band hits", sum(abs(e) < 2 for e in E.values()), "strict rate", r4(Fraction(sum(abs(e) < 2 for e in E.values()), 24)))
print("L3 edge-as-miss rate", r4(Fraction(hits - 7, 24)), "hits-7", hits - 7)
print("L3 ratio 13/24", r4(Fraction(13, 24)), "13/15", r4(Fraction(13, 15)), "-3/15", r4(Fraction(-3, 15)), "54/9", r4(Fraction(54, 9)))
# ties: any exact 5th-decimal tie in any printed quantity
ties = []
for name, q in [("L1 rate", Fraction(h1, 8)), ("L1 bias", Fraction(sum(e1.values()), 8)), ("L2 rate", Fraction(h2, 6)), ("L2 bias", Fraction(sum(e2.values()), 6)),
                ("L3 rate", Fraction(hits, H)), ("L3 bias", bias), ("L3 cal", cal)]:
    s = q * 10000
    if s.denominator != 1 and (s - int(s)) == Fraction(1, 2):
        ties.append(name)
print("exact ties at 4dp:", ties or "none")
print("L3 calibration integer sums printing 0.9167:", [k for k in range(-200, 201) if r4(Fraction(k, 12)) == Decimal("0.9167")])
