"""Round 3: independent recomputation of every number in FC1-a prose (L01-L03, hub quiz and placement)."""
from fractions import Fraction as F
import math

def half_up_cents(x):
    return math.floor(x * 100 + F(1, 2))

# L01 Example 3.3
d, rho = F(1000), F(1, 10)
S = lambda n: d * (1 - (1 - rho) ** (n + 1)) / rho
print("S1", S(1), "S2", S(2), "S10", float(S(10)), "S10 cents", half_up_cents(S(10)))
print("mult10 exact", float(S(10) / d), "4dp", round(float(S(10)/d), 4), "4dp*1000", round(float(S(10)/d), 4) * 1000)
# Example 3.6
lim = F(1000) / (1 - F(45, 100))
print("ex3.6 limit", float(lim), "cents", half_up_cents(lim), "pct of 10000", float(lim / 10000 * 100))
# Lab C half share cents total stage 10 (exact sum)
path = [F(1000)]
for _ in range(10):
    path.append(F(1, 2) * (1 - rho) * path[-1])
tot = sum(path)
print("halfshare stage10 total cents", half_up_cents(tot), "limit cents", half_up_cents(F(1000) / (1 - F(1, 2) * (1 - rho))))
# E2 ratio
print("E2 ratio", F(181818, 1000000), float(F(181818, 1000000) * 100), "2/11", F(2, 11), float(F(2, 11)))
# M2
rho2 = F(1, 4)
print("M2 S2", F(800) * (1 - (1 - rho2) ** 3) / rho2, [800, 600, 450], 800 + 600 + 450)
# M1, M3, quiz
print("M3 equity", 300 - 320)
# placement
print("placement 7/9", float(F(7, 9) * 100), "80% of 9", F(80, 100) * 9)
print("hours", float(F(50, 70) * 100), float(F(20, 70) * 100))
print("110/1.1", F(110) / F(11, 10), "1.05^2*1000", F(1000) * F(105, 100) ** 2)
print("S2 example", F(1000) * (1 + F(9, 10) + F(81, 100)))
# L01 quiz numbers
print("L01 q4 S2 half", F(1) * (1 + F(1, 2) + F(1, 4)))
# L02 numbers
print("L02 E2 75pct", F(3, 4) * 100)
# L03 numbers
print("ex1.4 rel", F(30, 5000), float(F(30, 5000) * 100))
print("E3 rel", F(6, 20000), float(F(6, 20000) * 100))
print("M1 L03 cash", 10002 * 50 - 9998 * 50, "sQ", 4 * 50)
print("M2 L03", 10008 * 80, 10006 * 80, 10006 * 80 - 10008 * 80, 2 * 160, 1 * 80 * (10010 - 10004), 320 - 480)
print("ex2.5", -9998 * 100 + 9992 * 100, 2 * 200, -1 * 100 * (10000 - 9990), 400 - 1000)
print("R2", 10002 * 100 - 9988 * 100, -1 * 100 * (9990 - 10000))
print("q7 L03 103", 3 * 1000 / 2, 2 * 1000)
print("L03 tie profit", (102 - 100) * 1000 / 2)
print("L03 q1", 10002 - 9998)
print("L03 P3 'Q/2' k>2: 2(k-1)>k at k=3", 2 * (3 - 1) > 3)
