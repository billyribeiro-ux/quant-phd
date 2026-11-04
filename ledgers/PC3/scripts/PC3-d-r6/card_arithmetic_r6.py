"""Re-derive the numeric claims of PC3 cards (exact fractions and float checks), independent of the lessons' prose.

Usage: python -I ledgers/PC3/scripts/PC3-d-r6/card_arithmetic_r6.py
"""
import itertools
import math
from fractions import Fraction as F

print("== L03 biased game +150/-100 each 1/2, six turns (cards c051, c052, c135, c136)")


def stop_value(rule):
    total = F(0)
    for path in itertools.product([150, -100], repeat=6):
        s = 0
        pay = None
        for t, x in enumerate(path):
            s += x
            if rule(s, path[: t + 1]):
                pay = s
                break
        if pay is None:
            pay = s
        total += F(pay, 64)
    return total


print("play all", stop_value(lambda s, h: False), "| first loss", stop_value(lambda s, h: h[-1] == -100),
      "| total reaches 100", stop_value(lambda s, h: s >= 100), "| 200 gain or loss", stop_value(lambda s, h: abs(s) >= 200))
print("== L03 fair game, two-turn rule that stops at larger cumulative total (c055)")
paths = []
for x1, x2 in itertools.product([100, -100], repeat=2):
    w1, w2 = x1, x1 + x2
    paths.append(w1 if w1 > w2 else w2)  # stop at the turn with the larger cumulative total
print("totals", paths, "mean", F(sum(paths), 4))
print("== L03 reroll game (c045, c046, c056, c058)")
cont = F(sum(100 * g for g in range(1, 7)), 6) - 100
print("continuation", cont, "value", sum(max(F(100 * f), cont) for f in range(1, 7)) / 6, "gain", sum(max(F(100 * f), cont) for f in range(1, 7)) / 6 - 350)
print("== L01 numbers (c007, c009, c013, c014, c016, c128-c133, c156)")
print("product ends", 20 * 2 * 300, 60 * 10 * 390, "ratio", F(234000, 12000))
base = math.log(19.5)
print("ln19.5 %.10f" % base, "factor widths", "%.10f %.10f %.10f" % (math.log(3), math.log(5), math.log(1.3)))
red_q = math.log(10 / 2) - math.log(8 / 4)
red_m = math.log(390 / 300) - math.log(360 / 330)
print("reduction quote updates %.6f share %.4f%%" % (red_q, 100 * red_q / base), "reduction minutes %.6f share %.4f%%" % (red_m, 100 * red_m / base))
print("ln1.5 %.4f ln(2.5/1.01) %.4f" % (math.log(1.5), math.log(2.5 / 1.01)))
e10 = F(101, 100) ** 10
print("(1.01)^10 float", float(e10), "exact numerator", e10.numerator, "digits to 20 places", str(e10.numerator * 10**20 // e10.denominator))
rem = e10 - 1 - F(10, 100)
bound = F(10 * 9, 2) * F(101, 100) ** 8 * F(1, 10000)
print("remainder", float(rem), "bound", float(bound), "ratio", float(rem / bound), "bound/rem-1", float(bound / rem - 1))
e20 = F(21, 20) ** 10
print("(1.05)^10", float(e20), "miss", float(e20 - F(3, 2)), "bound x=1/20", float(F(45) * F(21, 20) ** 8 * F(1, 400)))
print("miss share", float((e20 - F(3, 2)) / e20))
print("sqrt midpoint", math.sqrt(12000 * 234000), "ln 4 %.6f ln16 %.4f" % (math.log(4), math.log(16)))
print("== L06 numbers (c110-c127, c147-c152, c179)")
A = sum(F(1, 1) / F(11, 10) ** t for t in (1, 2, 3))
print("A10", A, "A10 float", float(A), "3310/1331 match", A == F(3310, 1331))
I, m = 15000000, 5000
print("NPV(200) exact", -I + m * A * 200, "float", float(-I + m * A * 200), "NPV(1600) exact", -I + m * A * 1600, float(-I + m * A * 1600))
print("NPV(1200) exact", -I + m * A * 1200, float(-I + m * A * 1200), "= -105000000/1331:", -I + m * A * 1200 == F(-105000000, 1331))
print("breakeven 10%", float(I / (m * A)), "=399300/331:", I / (m * A) == F(399300, 331))
print("NPV(1300) =1550000000/1331:", -I + m * A * 1300 == F(1550000000, 1331), float(-I + m * A * 1300))
A8 = sum(F(1, 1) / F(108, 100) ** t for t in (1, 2, 3))
A12 = sum(F(1, 1) / F(112, 100) ** t for t in (1, 2, 3))
print("breakeven 8%", float(I / (m * A8)), "12%", float(I / (m * A12)))
print("NPV 8% at 200,1600", float(-I + m * A8 * 200), float(-I + m * A8 * 1600), "NPV 12% at 200,1600", float(-I + m * A12 * 200), float(-I + m * A12 * 1600))
print("NPV 8% at 1200", float(-I + m * A8 * 1200))
u10 = I / (m * A)
print("margin for break-even 1600 (c152)", float(F(I) / (1600 * A)), "exact", F(15000000 * 1331, 1600 * 3310), float(F(15000000 * 1331, 1600 * 3310)))
print("margin fraction", float(F(1) * u10 / 1600), "fall %", float((1 - u10 / 1600) * 100))
print("c125 NPV", -100 + F(600, 11) + F(6000, 121), "= 500/121:", -100 + F(600, 11) + F(6000, 121) == F(500, 121))
print("c126", F(100000 * 1331, 400 * 3310), float(F(100000 * 1331, 400 * 3310)))
print("c151 slope", (1249.0469 - 1164.1005) / 4)
print("== L04 (c070, c071, c074, c082, c083)")
for v in (10000, 10020, 9985):
    e = F(5) - F(1, 2) * (max(v - 10010, 0) + max(9990 - v, 0))
    print("E at", v, e)
print("c082 d", F(2, 5) * 10 / F(3, 5), float(F(2, 5) * 10 / F(3, 5)))
print("c083 max |I| with 25 I^2 < 100:", max(i for i in range(0, 20) if 25 * i * i < 100))
print("c074 sd at 3 and 10 units", 5 * 3, 5 * 10)
print("== L05 heap bound (c170) and naive counts (c096, c097)", 3 * 200 * int(math.log2(200)), (200 - 8 + 1) * 7, (200 - 32 + 1) * 31)
print("== L02 (c035) P(B), P(A|B)", F(3, 10) * F(1, 2) + F(7, 10) * F(1, 5), F(15, 100) / F(29, 100))
print("== L06 (c125) NPV -100,60,60 at 10%", F(500, 121), float(F(500, 121)))
