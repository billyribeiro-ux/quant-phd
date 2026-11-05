import random
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

def r4(x: Fraction) -> str:
    # independent: exact half-away-from-zero via Decimal of the exact fraction
    d = (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    return str(d)

# Lab 3 realised, rebuilt independently
rng = random.Random(20261103)
real = {}
for t in range(1, 37):
    noise = rng.randint(-3, 3)
    shift = -6 if t >= 28 else 0
    real[t] = 100 + 2 * t + noise + shift
err = {t: (100 + 2 * t) - real[t] for t in range(13, 37)}
hits = [t for t in err if abs(err[t]) <= 2]
edge = [t for t in err if abs(err[t]) == 2]
print("L3 hits", len(hits), "rate", r4(Fraction(len(hits), 24)), "bias", Fraction(sum(err.values()), 24), r4(Fraction(sum(err.values()), 24)))
print("L3 edge", edge)
mx = max(abs(v) for v in err.values()); print("L3 max|e|", mx, [t for t in err if abs(err[t]) == mx])
print("L3 errors 13..36", [err[t] for t in range(13, 37)])
print("sum 13..27", sum(err[t] for t in range(13, 28)), "hits 13..27", len([t for t in range(13, 28) if abs(err[t]) <= 2]))
print("sum 28..36", sum(err[t] for t in range(28, 37)), "min,max 28..36", min(err[t] for t in range(28, 37)), max(err[t] for t in range(28, 37)))
print("range 13..27", min(err[t] for t in range(13, 28)), max(err[t] for t in range(13, 28)))
print("rolling 25..36 sum", sum(err[t] for t in range(25, 37)), Fraction(sum(err[t] for t in range(25, 37)), 12), r4(Fraction(sum(err[t] for t in range(25, 37)), 12)))
cal = {t: (100 + 2 * t) - real[t] for t in range(1, 13)}
s = sum(cal.values()); print("calibration sum", s, "bias", r4(Fraction(s, 12)))
print("integer s in [-60,60] with r4(s/12)==0.9167:", [k for k in range(-60, 61) if r4(Fraction(k, 12)) == "0.9167"])
print("strict-band hits", len([t for t in err if abs(err[t]) < 2]), r4(Fraction(len([t for t in err if abs(err[t]) < 2]), 24)))
print("first 13..27 bias", r4(Fraction(sum(err[t] for t in range(13,28)), 15)), "rate", r4(Fraction(13,15)), r4(Fraction(-3,15)))
print("month 28-36 bias", r4(Fraction(54, 9)), r4(Fraction(0, 9)))
# Lab 1
L1r = (125, 131, 128, 132, 138, 133, 140, 135)
e1 = [100 + 2 * t - y for t, y in zip(range(13, 21), L1r)]
h1 = [abs(e) <= 2 for e in e1]
print("L1 errors", e1, "hits", sum(h1), r4(Fraction(sum(h1), 8)), "bias", r4(Fraction(sum(e1), 8)), "edge", [t for t, e in zip(range(13, 21), e1) if abs(e) == 2])
print("L1 strict-band hits", sum(abs(e) < 2 for e in e1), r4(Fraction(sum(abs(e) < 2 for e in e1), 8)))
print("L1 13/24 check", r4(Fraction(13, 24)), "1/8", r4(Fraction(1, 8)))
# Lab 2
L2r = (127, 126, 124, 131, 136, 141)
e2 = [100 + 2 * t - y for t, y in zip(range(13, 19), L2r)]
h2 = sum(abs(e) <= 2 for e in e2)
print("L2 errors", e2, "hits", h2, r4(Fraction(h2, 6)), "bias", Fraction(sum(e2), 6), r4(Fraction(sum(e2), 6)), "edge", [t for t, e in zip(range(13, 19), e2) if abs(e) == 2])
print("L2 hit count over 8", r4(Fraction(h2, 8)), "mean abs", Fraction(sum(abs(e) for e in e2), 6), r4(Fraction(sum(abs(e) for e in e2), 6)))
print("L2 hit rate over 8 (page says 0.5000 for count over 8):", r4(Fraction(4, 8)))
print("tie check for printed values: fractions", [str(Fraction(h2,6)), str(Fraction(sum(e2),6))])
print("L3 printed values scaled by 1e4 remainders:", [ (Fraction(13,24)*10**4) % 1, (Fraction(51,24)*10**4) % 1 ])
