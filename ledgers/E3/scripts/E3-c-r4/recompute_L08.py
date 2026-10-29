"""Round 4: independent recomputation of L08 numbers, exact fractions and floats."""
import math
from fractions import Fraction as F

W1, W0p = 110000, 95000
def ce(p):  # CRRA gamma=2, u=-1/W, p=P(red) on W1
    return 1 / (p / W1 + (1 - p) / W0p)
half = F(1, 2)
print("EU CE exact =", ce(half), "=", float(ce(half)), "| 4180000/41 =", 4180000 / 41)
print("EU CE at 1/4 =", float(ce(F(1, 4))), "| 1672000/17 =", 1672000 / 17, "| expected final wealth 0.25*110000+0.75*95000 =", .25*110000+.75*95000)
print("CE at 3/4 =", float(ce(F(3, 4))), "=> M3 claim 105822.78")
print("maxmin over {30..60}/90 : CE at 1/3 =", float(ce(F(1, 3))), "| CE at 2/3 =", float(ce(F(2, 3))))
# alpha-MEU tau=1/2 over 30..60
ps = [F(k, 90) for k in range(30, 61)]
invs = [p / W1 + (1 - p) / W0p for p in ps]
tau = F(1, 2)
print("alpha-MEU tau=1/2 CE =", float(1 / (tau * max(invs) + (1 - tau) * min(invs))), "exact eq EU:", 1 / (tau * max(invs) + (1 - tau) * min(invs)) == ce(half))
print("avg prior =", sum(ps) / len(ps), "midpoint extremes =", (F(1, 3) + F(2, 3)) / 2)
print("premium 102500 - EU CE =", 102500 - 4180000 / 41, "exact 22500/41 =", 22500 / 41, "CU =", (102500 - 4180000/41) / 100)
print("maxmin - W0 =", 99523.8095 - 100000)
# prospect
v = 0.5 * math.sqrt(100) + 0.5 * (-2 * math.sqrt(50))
inv = -((-v / 2) ** 2)
print("prospect V =", v, "inverse CU =", inv, "wealth =", 100000 + 100 * inv)
print("prospect V printed -2.071068; inverse -1.072330 =", round(inv, 6), "wealth 99892.7670 =", round(100000 + 100 * inv, 4))
# Example 2.5
print("Ex2.5 known red = ", float(1 / (F(1, 3) / 110000 + F(2, 3) / 100000)), "known black =", float(1 / (F(2, 3) / 110000 + F(1, 3) / 100000)))
print("Ex2.5 exact known red", 1 / (F(1, 3) / 110000 + F(2, 3) / 100000), "black", 1 / (F(2, 3) / 110000 + F(1, 3) / 100000))
print("E1 diff 103125-100000 =", 103125 - 100000, "cents =", (103125 - 100000) / 100, "CU")
print("Model4 maxmin value 1/(1/3/110000+2/3/95000) = %.10f" % (1 / (F(1,3)/110000 + F(2,3)/95000) if False else float(1 / (F(1,3)/110000 + F(2,3)/95000))))
# Remark 4.2 numbers
g = lambda p: p / W1 + (1 - p) / W0p
print("g affine check: g(1/3)+g(2/3) =", g(F(1,3)) + g(F(2,3)), "= 2 g(1/2) =", 2 * g(half))
# Remark 2.3 / Thm 2.2 numbers
print("CE maxmin 99523.8095 <= 101951.2195:", 99523.8095 <= 101951.2195)
# Lab 1 part A closed-check: EZ CE with a=-1
# Quiz E1 etc.
print("R2 black known 106451.6129 >", 103125, ":", 106451.6129 > 103125)
