"""Independent recomputation of the L05, L06 and L08 prose numbers (verifier round 14, slice e)."""
from fractions import Fraction as F
import math

# L05: risky tree, gamma = 2, psi = 1/2, beta = 9/10, c0 = 2
def ce(outs, g):
    s = 1 - g
    return sum(p * c ** s for p, c in outs) ** (1 / s)

tree = [(0.5, 1.0), (0.5, 4.0)]
print("L05 CE gamma .5, 2, 3:", [round(ce(tree, g), 4) for g in (0.5, 2.0, 3.0)])
beta = F(9, 10); a = 1 - 1 / F(1, 2)  # psi = 1/2 -> a = -1
ce1 = F(8, 5)
V0 = ((1 - beta) * F(2) ** a + beta * ce1 ** a) ** (1 / a) if False else 1 / ((1 - beta) * F(1, 2) + beta * F(5, 8))
print("L05 V0 exact", V0, " 80/49 =", F(80, 49))
U = (1 - beta) * (-F(1, 2)) + beta * (F(1, 2) * (-1) + F(1, 2) * (-F(1, 4)))
print("L05 U exact", U, " -49/80 =", F(-49, 80), "(1-g)U == V0^(1-g):", -U == V0 ** -1)
print("L05 E1 case p=(1/4,3/4) on c1=(1,4): CE", 1 / (F(1, 4) + F(3, 4) * F(1, 4)), "V0", 1 / ((1 - beta) / 2 + beta * F(7, 16)), " 160/71 =", F(160, 71))
print("L05 R1 remark CE 8/5 and 12/5:", 1 / (F(1, 2) + F(1, 2) * F(1, 4)), 1 / (F(1, 2) * F(1, 2) + F(1, 2) * F(1, 3)))
# L05 M1: gamma 2, c1 = 1 (1/4), 3 (3/4)
print("L05 M1 CE", 1 / (F(1, 4) + F(3, 4) * F(1, 3)), "mean", F(1, 4) + F(9, 4))
# L05 M2: beta=1/2, psi=1/2, c0=1, c1=3
print("L05 M2 V0", 1 / (F(1, 2) * 1 + F(1, 2) * F(1, 3)))
# L05 Lab (4,4) vs (1,10): psi=2 (a=1/2), gamma=2, beta=1/2
eu = lambda c0, c1: 0.5 * (-1 / c0) + 0.5 * (-1 / c1)
ez = lambda c0, c1: (0.5 * c0 ** 0.5 + 0.5 * c1 ** 0.5) ** 2
print("L05 U(4,4), U(1,10):", eu(4, 4), eu(1, 10), " V0(4,4), V0(1,10):", round(ez(4, 4), 4), round(ez(1, 10), 4))
# L05 EIS analytic: MRS at (2,4), psi=1/2, beta=0.9
print("L05 MRS closed form (2,4):", (0.1 / 0.9) * (4 / 2) ** 2)

# L06
g, l, p = 1000, 600, 0.5
print("L06 EV", p * g - (1 - p) * l, "lam*", p * g / ((1 - p) * l), "W(1.5)", p * g - (1 - p) * 1.5 * l, "W(2)", p * g - (1 - p) * 2 * l)
print("L06 power threshold", math.sqrt(1000 / 600), "W(2) power", 0.5 * 1000 ** 0.5 - 0.5 * 2 * 600 ** 0.5)
print("L06 M1 lam*", (1 / 3 * 900) / (2 / 3 * 300), "W(2)", 1 / 3 * 900 - 2 / 3 * 2 * 300)
print("L06 remark 2.5 combined at lam=2:", 0.25 * 2000 + 0.5 * 400 - 0.25 * 2 * 1200, " separate:", 2 * (500 - 600 * 1.0 * 0 - 300 * 2))
print("L06 lam=3/2 combined", 700 - 300 * 1.5, "separate", 1000 - 600 * 1.5)
print("L06 alpha=1/2 R2 value", 0.5 * 800 ** 0.5 * (1 - 1), " R1 lambda_R for p=1/3:", (1 / 3) / (2 / 3) * math.sqrt(2))

# L08
w1, wl = 110000, 95000
eu_ce = 1 / (0.5 / w1 + 0.5 / wl)
print("L08 EU CE", eu_ce, F(4180000, 41), float(F(4180000, 41)))
vp = 0.5 * math.sqrt(100) + 0.5 * (-2 * math.sqrt(50))
inv = -((-vp / 2) ** 2)
print("L08 prospect V", vp, "CE change", inv, "wealth", 100000 + 100 * inv)
print("L08 maxmin", 1 / (1 / 3 / w1 + 2 / 3 / wl), "P=3/4 CE", 1 / (0.75 / w1 + 0.25 / wl), "P=1/4 CE", 1 / (0.25 / w1 + 0.75 / wl))
print("L08 M1 exact 1672000/17", F(1672000, 17), float(F(1672000, 17)), " 8360000/85", F(8360000, 85))
print("L08 M3 tau=0 value", 1 / (0.75 / w1 + 0.25 / wl))
print("L08 premium", 102500 - eu_ce, F(22500, 41), float(F(22500, 41)), "CU", (102500 - eu_ce) / 100)
print("L08 known red", 1 / ((1 / 3) / 110000 + (2 / 3) / 100000), "known black", 1 / ((2 / 3) / 110000 + (1 / 3) / 100000))
print("L08 Remark 4.2 means", (1 / 3 + 2 / 3) / 2, "avg prior", F(sum(range(30, 61)), 31 * 90))
print("L08 Example 2.5 known red 1/3 CE; alt wealth 100000/110000 check", 1 / ((1 / 3) / 110000 + (2 / 3) / 100000))
print("L08 Remark 2.3 maxmin 99523.8095 avg 101951.2195", round(1 / (1 / 3 / w1 + 2 / 3 / wl), 4), round(eu_ce, 4))
