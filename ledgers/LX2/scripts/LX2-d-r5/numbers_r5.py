"""LX2-d round 5: independent recomputation of every number the LX2 lessons print or derive (exact Fractions)."""
from fractions import Fraction as F
import math

# L04 Part A errors (periods 1-24), read from the printed table
e = [4, 3, 2, 11, 7, 0, 4, -1, 6, 6, 5, -3, -1, 8, 2, 6, 8, -1, 8, -2, 9, 4, -2, -1]
h = [1 if abs(x) <= 2 else 0 for x in e]
print("A: sum", sum(e), "hits", sum(h), "hit rate", F(sum(h), 24), "bias", F(sum(e), 24), "MAE", F(sum(abs(x) for x in e), 24))
print("B: first12 hit", F(sum(h[:12]), 12), "bias", F(sum(e[:12]), 12), "| last12 hit", F(sum(h[12:]), 12), "bias", F(sum(e[12:]), 12))
print("E2: sum of periods 1-12 errors", sum(e[:12]))
print("hits in periods 13-24:", [t + 1 for t in range(12, 24) if h[t]])
# Part D: pairs (V in -4..4, U in -6..6) with |1+V-U| <= 2
pairs = [(v, u) for v in range(-4, 5) for u in range(-6, 7)]
hit_pairs = [(v, u) for v, u in pairs if abs(1 + v - u) <= 2]
print("D: pairs", len(pairs), "hit pairs", len(hit_pairs), "P(hit)=", F(len(hit_pairs), len(pairs)), round(len(hit_pairs) / len(pairs), 4))
print("D: E[e]=", F(sum(1 + v - u for v, u in pairs), len(pairs)))
# R2 (L04 Problem): hit counts by band
for b in range(0, 4):
    c = sum(1 for v, u in pairs if abs(1 + v - u) <= b)
    print("R2 band", b, "pairs", c, F(c, 117), round(c / 117, 4))
# E3: standard error and gap
var_e = F(81 - 1, 12) + F(169 - 1, 12)
se = math.sqrt(float(var_e / 24))
gap = F(41, 12) - 1
print("E3: Var(e)=", var_e, "se=", round(se, 4), "gap=", gap, float(gap), "z=", round(float(gap) / se, 3))
# M2 rounding: -7/3 displayed to 4 places; ties away from zero
def disp(x):
    s = "-" if x < 0 else ""
    u = math.floor(abs(x) * 10**4 + F(1, 2))
    return f"{s}{u // 10**4}.{u % 10**4:04d}"
print("M2:", disp(F(-7, 3)), "M3:", disp(F(44, 12)), "A bias:", disp(F(41, 12)), "A hit:", disp(F(3, 8)))
# L03 ratio table and comparisons
ratios = {0: F(6, 97), 1: F(3, 104), 2: F(5, 34), 3: F(6, 29), 4: F(17, 50), 5: F(21, 37)}
print("L03 ratios:", {k: str(v) for k, v in ratios.items()}, "max", max(ratios.values()))
print("3*97 =", 3 * 97, " 6*104 =", 6 * 104, " 21*50 =", 21 * 50, " 17*37 =", 17 * 37, " 6/29-5/34 =", F(6, 29) - F(5, 34))
print("L03 cancels sum", 6 + 3 + 10 + 12 + 17 + 21, "fills sum", 97 + 104 + 68 + 58 + 50 + 37, "= 2*207:", 97 + 104 + 68 + 58 + 50 + 37 == 2 * 207)
print("L03 M3 C_t =", 1000 - 120 - 2 * 300 - 40)
