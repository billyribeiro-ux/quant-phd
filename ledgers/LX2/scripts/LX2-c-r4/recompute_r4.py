"""LX2-c round 4: independent recomputation of every number in project.html (own code, exact Fractions).

Run: .venv/bin/python -I ledgers/LX2/scripts/LX2-c-r4/recompute_r4.py
Uses only the seeded generator (random.Random) and the illustrative values written in the page's labs.
"""

import random
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP


def r4(x: Fraction) -> str:
    """Half-up (ties away from zero) to four decimals, via Decimal on the exact fraction."""
    d = (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    return str(d)


def f(x: Fraction) -> float:
    return float(x)


def has_exact_tie(x: Fraction) -> bool:
    """True if x*10^4 has fractional part exactly 1/2 (a tie at four decimals)."""
    y = x * 10000
    return (y - int(y)) == Fraction(1, 2) or (y - int(y)) == Fraction(-1, 2)


def forecast(t: int) -> int:
    return 100 + 2 * t


# Lab 1 (months 13..20)
L1_REAL = (125, 131, 128, 132, 138, 133, 140, 135)
L1_E = [forecast(13 + i) - y for i, y in enumerate(L1_REAL)]
L1_H = len(L1_E)
L1_hits = sum(abs(e) <= 2 for e in L1_E)
L1_edge = [13 + i for i, e in enumerate(L1_E) if abs(e) == 2]
L1_strict = sum(abs(e) < 2 for e in L1_E)
print("LAB1 errors", L1_E, "sum", sum(L1_E))
print("LAB1 hits", L1_hits, "of", L1_H, "rate", r4(Fraction(L1_hits, L1_H)), "bias", r4(Fraction(sum(L1_E), L1_H)))
print("LAB1 edge", L1_edge, "strict hits", L1_strict, "strict rate", r4(Fraction(L1_strict, L1_H)))
print("LAB1 one hit moves rate by", Fraction(1, L1_H), "=", r4(Fraction(1, L1_H)))
print("LAB1 ties", [has_exact_tie(Fraction(L1_hits, L1_H)), has_exact_tie(Fraction(sum(L1_E), L1_H))])

# Lab 2 (months 13..18)
L2_REAL = (127, 126, 124, 131, 136, 141)
L2_E = [forecast(13 + i) - y for i, y in enumerate(L2_REAL)]
L2_H = len(L2_E)
L2_hits = sum(abs(e) <= 2 for e in L2_E)
L2_edge = [13 + i for i, e in enumerate(L2_E) if abs(e) == 2]
print("LAB2 errors", L2_E, "hits", L2_hits, "of", L2_H, "rate", r4(Fraction(L2_hits, L2_H)))
print("LAB2 bias", r4(Fraction(sum(L2_E), L2_H)), "edge", L2_edge)
print("LAB2 mean abs error", r4(Fraction(sum(abs(e) for e in L2_E), L2_H)), "hits over 8", r4(Fraction(L2_hits, 8)))
print("LAB2 strict hits", sum(abs(e) < 2 for e in L2_E), r4(Fraction(sum(abs(e) < 2 for e in L2_E), L2_H)))
print("LAB2 ties", [has_exact_tie(Fraction(L2_hits, L2_H)), has_exact_tie(Fraction(sum(L2_E), L2_H))])

# Lab 3: seeded generator, reimplemented from the stated rule
rng = random.Random(20261103)
real = {}
for t in range(1, 37):
    noise = rng.randint(-3, 3)
    real[t] = 100 + 2 * t + noise - (6 if t >= 28 else 0)
E = {t: forecast(t) - real[t] for t in range(1, 37)}
V = range(13, 37)
val = {t: E[t] for t in V}
H = len(val)
hits = sum(abs(val[t]) <= 2 for t in V)
bias_sum = sum(val.values())
print("LAB3 H", H, "hits", hits, "rate", r4(Fraction(hits, H)), "bias", r4(Fraction(bias_sum, H)), "sum", bias_sum)
print("LAB3 edge", [t for t in V if abs(val[t]) == 2])
worst = max(V, key=lambda t: (abs(val[t]), -t))
print("LAB3 worst", abs(val[worst]), "month", worst, "all months with that |e|", [t for t in V if abs(val[t]) == abs(val[worst])])
cal = [E[t] for t in range(1, 13)]
print("LAB3 calibration sum", sum(cal), "bias", r4(Fraction(sum(cal), 12)))
print("LAB3 integer sums s in -200..200 that print as 0.9167 over 12:", [s for s in range(-200, 201) if r4(Fraction(s, 12)) == "0.9167"])
print("LAB3 strict hits", sum(abs(val[t]) < 2 for t in V))
print("LAB3 hit rate 13/24 exact decimal ->", r4(Fraction(13, 24)), "tie?", has_exact_tie(Fraction(13, 24)))
print("LAB3 bias 51/24 ->", r4(Fraction(51, 24)), "tie?", has_exact_tie(Fraction(51, 24)))
print("LAB3 bias 2.125 check", Fraction(51, 24) == Fraction(2125, 1000))
print("LAB3 sums 13-27", sum(E[t] for t in range(13, 28)), "hits", sum(abs(E[t]) <= 2 for t in range(13, 28)))
print("LAB3 sums 28-36", sum(E[t] for t in range(28, 37)), "hits", sum(abs(E[t]) <= 2 for t in range(28, 37)))
print("LAB3 errors 28-36", [E[t] for t in range(28, 37)], "min", min(E[t] for t in range(28, 37)), "max", max(E[t] for t in range(28, 37)))
print("LAB3 -3/15", r4(Fraction(-3, 15)), "13/15", r4(Fraction(13, 15)), "54/9", r4(Fraction(54, 9)), "0/9", r4(Fraction(0, 9)))
print("LAB3 rolling 12 at 36 (months 25..36)", sum(E[t] for t in range(25, 37)), r4(Fraction(sum(E[t] for t in range(25, 37)), 12)))
print("LAB3 strict count 13 minus edge count", hits - len([t for t in V if abs(val[t]) == 2]))
print("LAB3 errors 13-27", [E[t] for t in range(13, 28)])
print("LAB3 errors 13-36 full", [E[t] for t in V])
print("LAB3 sum check", sum(E[t] for t in range(13, 28)) + sum(E[t] for t in range(28, 37)) == bias_sum)
print("LAB3 realised 13-20", [real[t] for t in range(13, 21)])
print("LAB3 realised 13-18", [real[t] for t in range(13, 19)])
print("LAB1 vs case series agree at months", [13 + i for i in range(8) if L1_REAL[i] == real[13 + i]])
print("LAB2 vs case series agree at months", [13 + i for i in range(6) if L2_REAL[i] == real[13 + i]])
print("LAB3 errors 1-12 months (calibration)", cal)
print("Lab 3 line 0.0000 for 0/9 hit rate ->", r4(Fraction(0, 9)))
