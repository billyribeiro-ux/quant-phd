"""Re-derive the numbers printed on the changed and new cards (round 15) from first principles.

Usage: python3 -I card_arithmetic_check_r15.py
Covers LX2-c079 (44/117), LX2-c078 (E[e_t] = 1), LX2-c086 (bias 0, MAE 3), LX2-c100 (41/12, 3.4167),
LX2-c085 (3/8, 0.3750) and LX2-c053 (3 x 97 < 6 x 104). Every value is computed with exact fractions.
"""
from fractions import Fraction as F

pairs = [(v, u) for v in range(-4, 5) for u in range(-6, 7)]  # forecast draw V in -4..4, realised draw U in -6..6
hits = [(v, u) for v, u in pairs if -3 <= v - u <= 1]  # hit at band 2: |1 + V - U| <= 2
p_hit = F(len(hits), len(pairs))
print("c079 pairs", len(pairs), "hits", len(hits), "P(hit)", p_hit, "decimal", round(float(p_hit), 4))
print("c079 check 8*5+4 =", 8 * 5 + 4)
mean_v = F(sum(v for v, _ in pairs), len(pairs))
mean_u = F(sum(u for _, u in pairs), len(pairs))
print("c078 E[e] = 1 + E[V] - E[U] =", 1 + mean_v - mean_u)
errors = [3, -3, 3, -3]  # Part C printed errors
print("c086 bias", F(sum(errors), len(errors)), "MAE", F(sum(abs(e) for e in errors), len(errors)))
print("c100 41/12 =", round(41 / 12, 4), "; 82/24 =", F(82, 24), "; sum of 24 errors must be 82")
print("c085 9/24 =", F(9, 24), "decimal", round(9 / 24, 4))
print("c053 3*97 =", 3 * 97, "< 6*104 =", 6 * 104, "->", 3 * 97 < 6 * 104)
