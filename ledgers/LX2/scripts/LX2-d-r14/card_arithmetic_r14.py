"""Round-14 recomputation of every number the LX2 cards state (independent of the lab code).

Run: python3 -I card_arithmetic_r14.py. Uses only fractions and math; no lesson or lab code is imported.
"""

import math
from fractions import Fraction as F


def disp(x: F) -> str:
    sign = "-" if x < 0 else ""
    units = math.floor(abs(x) * 10**4 + F(1, 2))
    return f"{sign}{units // 10**4}.{units % 10**4:04d}"


# Prop 4.4 / card c079: pairs (V,U), V in -4..4 (9 values), U in -6..6 (13 values); hit iff |1+V-U| <= 2
pairs = [(v, u) for v in range(-4, 5) for u in range(-6, 7)]
hits = [(v, u) for v, u in pairs if abs(1 + v - u) <= 2]
print("pairs", len(pairs), "hits", len(hits), "P(hit)", F(len(hits), len(pairs)), "=", disp(F(len(hits), len(pairs))))
print("E[e] by enumeration", F(sum(1 + v - u for v, u in pairs), len(pairs)))
print("8*5+4 =", 8 * 5 + 4)
# card c085 / c100: the 24 printed errors of Lab 1 Part A, read from the run output
errors = [4, 3, 2, 11, 7, 0, 4, -1, 6, 6, 5, -3, -1, 8, 2, 6, 8, -1, 8, -2, 9, 4, -2, -1]
hit_flags = [abs(e) <= 2 for e in errors]
print("Part A hits", sum(hit_flags), "of", len(errors), "hit rate", F(sum(hit_flags), len(errors)), disp(F(sum(hit_flags), len(errors))))
print("Part A bias", F(sum(errors), len(errors)), disp(F(sum(errors), len(errors))), "sum", sum(errors))
# card c086: Part C errors +3,-3,+3,-3
pc = [3, -3, 3, -3]
print("Part C bias", F(sum(pc), 4), "hit rate", F(sum(abs(e) <= 2 for e in pc), 4), "MAE", F(sum(abs(e) for e in pc), 4))
# card c053 / Lab 1 cancel-to-fill: ratio comparison, exact
print("3/104 vs 6/97: 3*97 =", 3 * 97, "6*104 =", 6 * 104, "less?", 3 * 97 < 6 * 104, "decimals", disp(F(3, 104)), disp(F(6, 97)))
print("largest 21/37 =", disp(F(21, 37)), "17/50 =", disp(F(17, 50)), "compare", F(21, 37) > F(17, 50))
# card c051/c054: Prop 2.2 example from L03 M3 (not a card; included as an arithmetic cross-check of the identity form)
# E3-style check used by the lesson (L04 Problem E3)
var_v = F(9 * 9 - 1, 12)
var_u = F(13 * 13 - 1, 12)
var_e = var_v + var_u
print("Var V", var_v, "Var U", var_u, "Var e", var_e)
se = math.sqrt(float(var_e / 24))
gap = F(41, 12) - 1
print("se", round(se, 4), "gap", gap, float(gap), "gap/se", round(float(gap) / se, 3))
# card c073 rounding rule check on -7/3 (lesson M2)
print("disp(-7/3) =", disp(F(-7, 3)))
