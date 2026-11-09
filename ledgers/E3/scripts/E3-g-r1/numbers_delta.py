from fractions import Fraction as F
w1, wl, w0 = 110000, 95000, 100000
def ce(p):  # CRRA u=-1/w, CE = 1/E[1/w] for red probability p
    return 1 / (p / w1 + (1 - p) / wl)
pmin, pmax = F(1, 3), F(2, 3)
mx = 1 / (float(pmin) / w1 + float(1 - pmin) / wl)
print("maxmin CE at p=1/3 (min over set, red 30..60 of 90):", round(mx, 4))
print("worst-prior check gives 99523.8095 ->", round(mx, 4) == 99523.8095)
mid = ce(0.5)
print("EU CE at pbar=1/2:", round(mid, 4), "(stated 101951.2195)")
print("risk premium 102500 - CE:", round(102500 - mid, 4), "(stated 548.7805)")
print("initial wealth minus maxmin CE:", round(w0 - 99523.8095, 4), "(stated 476.1905)")
print("maxmin CE below initial wealth:", 99523.8095 < w0)
# Remark 3.4 / row L05 line 499: exponents r^g vs r^(1/psi) differ for r != 1 iff g != 1/psi
import math
bad = []
for g in [0.5, 1.5, 2.0, 3.0]:
    for psi in [0.25, 0.5, 2.0, 3.0]:
        for r in [0.2, 0.5, 0.9, 1.1, 2.0, 4.0]:
            a, b = r ** g, r ** (1 / psi)
            same = math.isclose(a, b, rel_tol=1e-12)
            if same != (abs(g - 1 / psi) < 1e-12):
                bad.append((g, psi, r))
print("Remark 3.4 exponent-equality grid mismatches:", bad)
# MRS closed forms at (2,4), beta 0.9, gamma 2, psi 0.5 (L05 lab point)
beta, g, psi, c0, c1 = 0.9, 2.0, 0.5, 2.0, 4.0
print("MRS_EZ closed form:", round((1 - beta) / beta * (c1 / c0) ** (1 / psi), 6))
print("MRS_U closed form:", round((1 - beta) / beta * (c1 / c0) ** g, 6))
print("diagonal c1=c0 both:", (1 - beta) / beta, (1 - beta) / beta)
