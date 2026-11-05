"""LX2-c r12: independent re-derivation of every number in project.html (prose and printed blocks).

Written from the page's stated definitions, not copied from the lab code. Uses only the standard library.
Prints each number with the prose claim it checks. Run: .venv/bin/python -I ledgers/LX2/scripts/LX2-c-r12/rederive_r12.py
"""
import random
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP


def r4(x):
    """Round a Fraction half up (away from zero for ties) to 4 places, as text."""
    q = Decimal(x.numerator) / Decimal(x.denominator)
    return str(q.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))


def f(n, d=1):
    return Fraction(n, d)


def measures(months, realised, fc=lambda t: 100 + 2 * t):
    e = {t: fc(t) - realised[t] for t in months}
    H = len(months)
    hits = sum(1 for t in months if abs(e[t]) <= 2)
    edge = [t for t in months if abs(e[t]) == 2]
    bias = Fraction(sum(e.values()), H)
    return e, H, hits, Fraction(hits, H), bias, edge


# Lab 3 case: seeded realised values, months 1 to 36
rng = random.Random(20261103)
y = {}
for t in range(1, 37):
    noise = rng.randint(-3, 3)
    y[t] = 100 + 2 * t + noise - (6 if t >= 28 else 0)
val = list(range(13, 37))
e, H, hits, hr, bias, edge = measures(val, y)
print("L3 validation: H", H, "hits", hits, "hit rate", r4(hr), "(13/24 =", float(hr), ") bias", r4(bias), "sum", sum(e.values()))
print("L3 edge months", edge)
worst = max(val, key=lambda t: (abs(e[t]), -t))
print("L3 largest |e|", abs(e[worst]), "month", worst, "| months with |e|=8:", [t for t in val if abs(e[t]) == 8])
cal = list(range(1, 13))
ecal = {t: 100 + 2 * t - y[t] for t in cal}
print("L3 calibration errors", [ecal[t] for t in cal], "sum", sum(ecal.values()), "bias", r4(Fraction(sum(ecal.values()), 12)), "(11/12 =", float(Fraction(11, 12)), ")")
print("integers s with round(s/12,4)==0.9167:", [s for s in range(-200, 200) if r4(Fraction(s, 12)) == "0.9167"])
a = list(range(13, 28)); b = list(range(28, 37))
print("split 13-27: sum", sum(e[t] for t in a), "n", len(a), "hits", sum(1 for t in a if abs(e[t]) <= 2), "bias", r4(Fraction(sum(e[t] for t in a), len(a))), "hit rate", r4(Fraction(sum(1 for t in a if abs(e[t]) <= 2), len(a))), "=13/15", float(Fraction(13, 15)))
print("split 28-36: sum", sum(e[t] for t in b), "n", len(b), "hits", sum(1 for t in b if abs(e[t]) <= 2), "bias", r4(Fraction(sum(e[t] for t in b), len(b))))
print("errors 28-36 all positive:", all(e[t] > 0 for t in b), "min", min(e[t] for t in b), "max", max(e[t] for t in b))
print("errors 13-27 within [-3,3]:", all(-3 <= e[t] <= 3 for t in a))
print("errors 25-36 sum:", sum(e[t] for t in range(25, 37)), "/12 =", r4(Fraction(sum(e[t] for t in range(25, 37)), 12)))
strict = [t for t in val if abs(e[t]) < 2]
print("strict band hits:", len(strict), "rate", r4(Fraction(len(strict), 24)))
print("hits with |e|<=2 by month:", [t for t in val if abs(e[t]) <= 2])
print("errors 13-36 list:", [(t, e[t]) for t in val])
print("months 13-36 realised:", [y[t] for t in val])

# Lab 1 (rung 1): realised values stated in the page's lab 1 code, months 13 to 20
R1 = {13: 125, 14: 131, 15: 128, 16: 132, 17: 138, 18: 133, 19: 140, 20: 135}
e1, H1, h1, hr1, b1, ed1 = measures(list(R1), R1)
print("L1: errors", [e1[t] for t in R1], "hits", h1, "hit rate", r4(hr1), "bias", r4(b1), "edge", ed1)
print("L1 strict-band hits", sum(1 for t in R1 if abs(e1[t]) < 2), "(claim: strict test drops rate to 0.2500 = 2 of 8)")
print("L1 lab3 agreement months:", [t for t in R1 if y[t] == R1[t]])
# Lab 2 (rung 2): realised values, months 13 to 18
R2 = {13: 127, 14: 126, 15: 124, 16: 131, 17: 136, 18: 141}
e2, H2, h2, hr2, b2, ed2 = measures(list(R2), R2)
print("L2: errors", [e2[t] for t in R2], "hits", h2, "hit rate", r4(hr2), "bias", r4(b2), "edge", ed2)
print("L2 mean absolute error (claim 2.8333):", r4(Fraction(sum(abs(e2[t]) for t in R2), 6)))
print("L2 lab3 agreement months:", [t for t in R2 if y[t] == R2[t]])
print("L2 hit count over 8 (claim 0.5000):", r4(Fraction(h2, 8)))
print("hit rate ties (any 5th digit 5 exactly):", [r4(x) for x in [hr, bias, hr1, b1, hr2, b2, Fraction(11, 12)]])
print("hours: 2+2+2+3+3+2 =", 2 + 2 + 2 + 3 + 3 + 2, "; 14/50 =", Fraction(14, 50) * 100, "%")
print("L3 bias 51/24 =", float(Fraction(51, 24)), r4(Fraction(51, 24)))
