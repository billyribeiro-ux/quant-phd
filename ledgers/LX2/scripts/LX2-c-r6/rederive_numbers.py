"""Independent re-derivation of every number in project.html (rungs 1-3, exemplars, limitations, monitoring).

Written from the case documentation, not from the lab code: forecast(t) = 100 + 2t; seeded noise via
random.Random(20261103).randint(-3, 3) for t = 1..36 in order; realised = forecast-free 100 + 2t + noise, minus 6 from
month 28. Uses exact Fraction arithmetic and a half-up rounding applied once.

Usage: python3 -I rederive_numbers.py
"""
import random
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP


def fmt(x: Fraction, places: int = 4) -> str:
    d = Decimal(x.numerator) / Decimal(x.denominator)
    q = Decimal(1).scaleb(-places)
    return str(d.quantize(q, rounding=ROUND_HALF_UP))


def fmt_halfeven(x: Fraction, places: int = 4) -> str:
    from decimal import ROUND_HALF_EVEN
    d = Decimal(x.numerator) / Decimal(x.denominator)
    return str(d.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_EVEN))


def F(t: int) -> int:
    return 100 + 2 * t


# ---- Lab 3 (seeded) ----
rng = random.Random(20261103)
Y = {}
for t in range(1, 37):
    noise = rng.randint(-3, 3)
    Y[t] = 100 + 2 * t + noise - (6 if t >= 28 else 0)
E = {t: F(t) - Y[t] for t in range(1, 37)}
val = range(13, 37)
hits = [t for t in val if abs(E[t]) <= 2]
print("L3 validation hits", len(hits), "of", len(val), "rate", fmt(Fraction(len(hits), 24)), "strict-test hits",
      len([t for t in val if abs(E[t]) < 2]))
S = sum(E[t] for t in val)
print("L3 validation error sum", S, "bias", fmt(Fraction(S, 24)))
edge = [t for t in val if abs(E[t]) == 2]
print("L3 edge months", edge)
mx = max(abs(E[t]) for t in val)
print("L3 max abs err", mx, "months", [t for t in val if abs(E[t]) == mx])
cal = sum(E[t] for t in range(1, 13))
print("L3 calibration error sum", cal, "bias", fmt(Fraction(cal, 12)), "half-even", fmt_halfeven(Fraction(cal, 12)))
print("integer sums S with fmt(S/12)==0.9167:", [s for s in range(-200, 200) if fmt(Fraction(s, 12)) == "0.9167"])
print("L3 months 13-27 sum", sum(E[t] for t in range(13, 28)), "hits", len([t for t in range(13, 28) if abs(E[t]) <= 2]))
print("L3 months 28-36 sum", sum(E[t] for t in range(28, 37)), "hits", len([t for t in range(28, 37) if abs(E[t]) <= 2]))
print("L3 months 28-36 errors", [E[t] for t in range(28, 37)], "min", min(E[t] for t in range(28, 37)),
      "max", max(E[t] for t in range(28, 37)), "all positive", all(E[t] > 0 for t in range(28, 37)))
print("L3 rolling-12 at month 36 sum(25..36)", sum(E[t] for t in range(25, 37)),
      fmt(Fraction(sum(E[t] for t in range(25, 37)), 12)))
print("L3 errors months 13-27 in [-3,3]:", all(-3 <= E[t] <= 3 for t in range(13, 28)))
print("L3 total sum", S, "= 51 ?", S == 51, "; 13-27 + 28-36 =", sum(E[t] for t in range(13, 28)) + sum(E[t] for t in range(28, 37)))
print("L3 Y[13..36]", [Y[t] for t in range(13, 37)])
print("L3 abs-error mean-equivalent check: bias 2.1250 ==", fmt(Fraction(S, 24)) == "2.1250")
print("strict-band hit rate 6/24 =", fmt(Fraction(6, 24)))
print("L3 Y[18]", Y[18], "Y[13..20]", [Y[t] for t in range(13, 21)])

# ---- Lab 1 and Lab 2 (illustrative values, as written in the pages) ----
R1 = (125, 131, 128, 132, 138, 133, 140, 135)
e1 = [F(13 + i) - r for i, r in enumerate(R1)]
h1 = [abs(x) <= 2 for x in e1]
print("L1 errors", e1, "hits", sum(h1), "rate", fmt(Fraction(sum(h1), 8)), "bias", fmt(Fraction(sum(e1), 8)),
      "edge", [13 + i for i, x in enumerate(e1) if abs(x) == 2], "sum", sum(e1))
print("L1 strict hits", len([x for x in e1 if abs(x) < 2]), "L1 Y18 equal to L3 Y18:", R1[5] == Y[18],
      "L1 agrees with L3 at months", [13 + i for i, r in enumerate(R1) if Y[13 + i] == r])
R2 = (127, 126, 124, 131, 136, 141)
e2 = [F(13 + i) - r for i, r in enumerate(R2)]
h2 = [abs(x) <= 2 for x in e2]
print("L2 errors", e2, "hits", sum(h2), "rate", fmt(Fraction(sum(h2), 6)), "bias", fmt(Fraction(sum(e2), 6)),
      "edge", [13 + i for i, x in enumerate(e2) if abs(x) == 2], "mean abs", fmt(Fraction(sum(abs(x) for x in e2), 6)),
      "L2 agrees with L3 at", [13 + i for i, r in enumerate(R2) if Y[13 + i] == r],
      "hit/8 =", fmt(Fraction(sum(h2), 8)))
print("L1 hit count / 8 interplay: L1 bias 2/8 =", fmt(Fraction(2, 8)), "1/8 =", fmt(Fraction(1, 8)))
print("tie check: 13/24 =", fmt(Fraction(13, 24)), fmt_halfeven(Fraction(13, 24)))
print("L1 bias check 2/8, hit 4/8 and lab1 interpret 1/8=0.1250:", fmt(Fraction(1, 8)))
