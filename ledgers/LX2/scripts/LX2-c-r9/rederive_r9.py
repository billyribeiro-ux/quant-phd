# Independent re-derivation of every number in project.html (no import of the twins).
import random
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

def r4(x):  # half-up to 4 places, sign-aware
    d = Decimal(x.numerator) / Decimal(x.denominator)
    return str(d.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))

def fc(t): return 100 + 2 * t

# Lab 3 table
rng = random.Random(20261103)
real = {}
for t in range(1, 37):
    n = rng.randint(-3, 3)
    real[t] = 100 + 2 * t + n + (-6 if t >= 28 else 0)
err = {t: fc(t) - real[t] for t in range(13, 37)}
hits = [t for t in err if abs(err[t]) <= 2]
edge = [t for t in err if abs(err[t]) == 2]
H = len(err)
print("L3 hits", len(hits), "of", H, "hit rate", r4(F(len(hits), H)), "bias sum", sum(err.values()), "bias", r4(F(sum(err.values()), H)))
print("L3 edge", edge)
mx = max(abs(v) for v in err.values()); print("L3 max abs", mx, "months", [t for t in err if abs(err[t]) == mx])
cal = [fc(t) - real[t] for t in range(1, 13)]
print("L3 calib sum", sum(cal), "calib bias", r4(F(sum(cal), 12)))
print("L3 realised 13..36", [real[t] for t in range(13, 37)])
print("L3 errors 13-27 sum", sum(err[t] for t in range(13, 28)), "hits", sum(1 for t in range(13, 28) if abs(err[t]) <= 2),
      "rate", r4(F(sum(1 for t in range(13, 28) if abs(err[t]) <= 2), 15)))
print("L3 errors 28-36 sum", sum(err[t] for t in range(28, 37)), "hits", sum(1 for t in range(28, 37) if abs(err[t]) <= 2))
print("L3 rolling 12 at 36 (25..36) sum", sum(err[t] for t in range(25, 37)), "=", r4(F(sum(err[t] for t in range(25, 37)), 12)))
print("strict-band hits", sum(1 for t in err if abs(err[t]) < 2))
print("errors 28..36 range", min(err[t] for t in range(28, 37)), max(err[t] for t in range(28, 37)))
print("errors 13..27 range", min(err[t] for t in range(13, 28)), max(err[t] for t in range(13, 28)))
print("13/24 =", r4(F(13, 24)), " 2/8 =", r4(F(2, 8)), " 13/15 =", r4(F(13, 15)))

# Lab 1
R1 = (125, 131, 128, 132, 138, 133, 140, 135)
e1 = [fc(13 + i) - y for i, y in enumerate(R1)]
h1 = sum(1 for e in e1 if abs(e) <= 2)
print("L1 errors", e1, "hits", h1, "rate", r4(F(h1, 8)), "bias", r4(F(sum(e1), 8)), "edge", [13 + i for i, e in enumerate(e1) if abs(e) == 2])
print("L1 strict hits", sum(1 for e in e1 if abs(e) < 2), "strict rate", r4(F(sum(1 for e in e1 if abs(e) < 2), 8)))
# Lab 2
R2 = (127, 126, 124, 131, 136, 141)
e2 = [fc(13 + i) - y for i, y in enumerate(R2)]
h2 = sum(1 for e in e2 if abs(e) <= 2)
print("L2 errors", e2, "hits", h2, "rate", r4(F(h2, 6)), "bias", r4(F(sum(e2), 6)), "edge", [13 + i for i, e in enumerate(e2) if abs(e) == 2])
print("L2 hits over 8", r4(F(h2, 8)), "mean abs bias", r4(F(sum(abs(e) for e in e2), 6)))
print("L1 vs L3 agree months", [13 + i for i, y in enumerate(R1) if y == real[13 + i]], " L2 vs L3", [13 + i for i, y in enumerate(R2) if y == real[13 + i]])
print("L1 e13,e14 ", e1[0], e1[1], "sum", sum(e1))
print("Hit tie check: any printed value with 5th decimal exactly 5 and nothing after?")
for name, v in [("L1 rate", F(4, 8)), ("L1 bias", F(2, 8)), ("L2 rate", F(4, 6)), ("L2 bias", F(1, 6)), ("L3 rate", F(13, 24)), ("L3 bias", F(51, 24)), ("L3 calib", F(11, 12))]:
    x = v * 10**4
    print("  ", name, float(x), "frac", x - int(x))
# Lab 3 interpretation of 'only integer sum that prints as 0.9167 over 12 months'
print("integer sums s with r4(s/12)==0.9167:", [s for s in range(-100, 200) if r4(F(s, 12)) == "0.9167"])
# Element 4 threshold: H=12 rolling at 36
