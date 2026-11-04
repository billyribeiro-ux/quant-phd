"""LX1-c round 2: independent Fraction recomputation of every number on the rung 1 and rung 2 pages."""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F


def r2(x, places):
    q = Decimal(1).scaleb(-places)
    return Decimal(x.numerator) / Decimal(x.denominator) if False else (Decimal(x.numerator) / Decimal(x.denominator)).quantize(q, rounding=ROUND_HALF_UP)


D1 = F(100000)  # dollars, A1
falling = [F(p, 100) for p in (100, 97, 94, 91, 88, 85)]
rising = [F(p, 100) for p in (100, 103, 106, 109, 112, 115)]
print("Rung1 real debt (dollars) falling:", [str(r2(D1 / p, 2)) for p in falling])
print("Rung1 real debt (dollars) rising :", [str(r2(D1 / p, 2)) for p in rising])
print("Rung1 burden falling 100*(P0/P5-1) =", float(100 * (falling[0] / falling[-1] - 1)), "->", r2(100 * (falling[0] / falling[-1] - 1), 2))
print("Rung1 burden rising  =", float(100 * (rising[0] / rising[-1] - 1)), "->", r2(100 * (rising[0] / rising[-1] - 1), 2))
cents_fall = F(10000000) / falling[-1]
cents_rise = F(10000000) / rising[-1]
print("Rung1 period-5 real value cents falling (exact):", float(cents_fall), " rising:", float(cents_rise))
print("Rung1 difference cents exact:", float(cents_fall - cents_rise), " dollars:", r2((cents_fall - cents_rise) / 100, 2))
print("Rung1 1/0.85 - 1 percent:", float(100 * (F(1) / F(85, 100) - 1)))
# Rounding-first check (informational): round each period-5 real value to cent, then difference
rf = F(round(cents_fall)) - F(round(cents_rise))
print("Rung1 rounded-first difference cents:", rf, "dollars", r2(rf / 100, 2))
print("Rung1 rounded-first burden from rounded real values:",
      r2(100 * (F(round(D1 * 100 / 1) ) / 1 - 0), 2) if False else "n/a")
# Rung 2
D2 = F(4000000)
path2 = [F(p, 100) for p in (100, 99, 98, 96, 95, 93)]
print("Rung2 real debt dollars:", [str(r2(D2 / 100 / 1 / 1 * 1 / p if False else (D2 / p) / 100, 2)) for p in path2])
print("Rung2 burden 100*(P0/P5-1) =", float(100 * (path2[0] / path2[-1] - 1)), "->", r2(100 * (path2[0] / path2[-1] - 1), 2))
print("Rung2 inverted burden 100*(P5/P0-1) =", float(100 * (path2[-1] / path2[0] - 1)), "->", r2(100 * (path2[-1] / path2[0] - 1), 2))
print("Rung2 no-division real value stays 40000.00 in every period")
print("Rung2 burden without percent (ratio-1) =", float(path2[0] / path2[-1] - 1), "->", r2(path2[0] / path2[-1] - 1, 2))
# Lab 1 and 2 intermediate: the 'period 5' real value in cents for rung 2
print("Rung2 period-5 cents exact:", float(D2 / path2[-1]))
# Rung 1 exemplar A claim: 0.32 difference and window stats are in the Lab 3 script
