"""Independent recomputation of every number in L04 (outcomes analysis) and L03 claims that cite Lab 1 values.

Written from the page text and the generator draw order, not by importing the lab. Prints each figure checked.
"""

import math
import random
from fractions import Fraction

# L04 generator: realised y = 100 + U (U in -6..6), forecast = 101 + V (V in -4..4), draws U_1, V_1, U_2, V_2, ...
rng = random.Random(20261103)
path = []
for t in range(1, 25):
    u = rng.randint(-6, 6)
    v = rng.randint(-4, 4)
    path.append((t, 101 + v, 100 + u))
errors = [f - y for (_, f, y) in path]
hits = [1 if abs(e) <= 2 else 0 for e in errors]
print("errors", errors)
print("hits", sum(hits), "of", len(hits), "hit rate", Fraction(sum(hits), 24))
bias = Fraction(sum(errors), 24)
print("bias", bias, float(bias), "sum", sum(errors))
print("first12 hit rate", Fraction(sum(hits[:12]), 12), "bias", Fraction(sum(errors[:12]), 12))
print("last12 hit rate", Fraction(sum(hits[12:]), 12), "bias", Fraction(sum(errors[12:]), 12))
print("MAE full", Fraction(sum(abs(e) for e in errors), 24))


def rnd(x: Fraction) -> str:
    sign = "-" if x < 0 else ""
    units = math.floor(abs(x) * 10**4 + Fraction(1, 2))
    return f"{sign}{units // 10**4}.{units % 10**4:04d}"


print("display hit rate 3/8", rnd(Fraction(3, 8)), "bias 41/12", rnd(bias), "11/3", rnd(Fraction(11, 3)), "19/6", rnd(Fraction(19, 6)))
print("display -7/3", rnd(Fraction(-7, 3)), "44/117", rnd(Fraction(44, 117)), "20/39", rnd(Fraction(20, 39)))

# Proposition 4.4 by exhaustive enumeration: forecast draw V in -4..4 (9), realised draw U in -6..6 (13)
pairs = [(1 + v - u) for v in range(-4, 5) for u in range(-6, 7)]
n = len(pairs)
print("pairs", n)
print("P(hit)", Fraction(sum(1 for e in pairs if abs(e) <= 2), n))
print("E[e]", Fraction(sum(pairs), n))
for b in range(0, 5):
    c = sum(1 for e in pairs if abs(e) <= b)
    print("band", b, "count", c, "prob", Fraction(c, n), float(Fraction(c, n)))

# Variances and standard error (E3)
def var_uniform(k: int) -> Fraction:
    vals = list(range(-(k - 1) // 2, (k - 1) // 2 + 1)) if k % 2 else None
    m = Fraction(sum(vals), len(vals))
    return Fraction(sum((x - m) ** 2 for x in vals), len(vals))


def var_forecast_9() -> Fraction:
    vals = list(range(-4, 5))
    m = Fraction(sum(vals), len(vals))
    return Fraction(sum((x - m) ** 2 for x in vals), len(vals))


def var_realised_13() -> Fraction:
    vals = list(range(-6, 7))
    m = Fraction(sum(vals), len(vals))
    return Fraction(sum((x - m) ** 2 for x in vals), len(vals))


vf, vr = var_forecast_9(), var_realised_13()
print("Var V (9 values)", vf, "Var U (13 values)", vr, "Var e", vf + vr)
se2 = (vf + vr) / 24
print("se^2", se2, "se", math.sqrt(se2), "gap", Fraction(41, 12) - 1, "z", (float(Fraction(41, 12) - 1)) / math.sqrt(se2))
