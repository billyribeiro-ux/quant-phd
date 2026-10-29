"""Independent recomputation of the E5 L04-L06 printed values, from the model formulas, in Fractions.

Run: python -I ledgers/E5/scripts/E5-b-r2/recompute_r2.py (from the checkout root). Prints PASS/FAIL per check.
"""
import random
from fractions import Fraction as F

fails = 0


def check(label, got, want):
    global fails
    ok = got == want
    fails += not ok
    shown = "" if "identity" in label else got
    print(("PASS" if ok else "FAIL"), label, shown)


# L04 IS-LM, own implementation: solve the 2x2 system directly
c, c0, i0, b, d, h, tax = F(3, 4), F(1), F(1), F(2), F(1, 2), F(1), F(0)


def solve(G, m, bb):
    A = c0 - c * tax + i0 + G
    # (1-c)Y + bb*i = A ; d*Y - h*i = m  -> Cramer
    det = (1 - c) * (-h) - bb * d
    Y = (A * (-h) - bb * m) / det
    I = ((1 - c) * m - d * A) / det
    return Y, I


y0, r0 = solve(F(1), F(2), b)
y1, r1 = solve(F(11, 10), F(2), b)
y2, r2 = solve(F(2), F(2), b)
check("L04 Y*", y0, F(28, 5))
check("L04 i*", r0, F(4, 5))
check("L04 dY G 1->11/10", y1 - y0, F(2, 25))
check("L04 di G 1->11/10", r1 - r0, F(1, 25))
check("L04 mult step to 2", (y2 - y0) / 1, F(4, 5))
check("L04 di step to 2", r2 - r0, F(2, 5))
ym, rm = solve(F(1), F(5, 2), b)
check("L04 monetary mult", (ym - y0) / F(1, 2), F(8, 5))
check("L04 monetary di per unit", (rm - r0) / F(1, 2), F(-1, 5))
yb0, _ = solve(F(1), F(2), F(0))
yb1, _ = solve(F(2), F(2), F(0))
check("L04 b=0 multiplier", (yb1 - yb0), F(4))
check("L04 E1 ratio", (F(1, 25)) / F(2, 25), F(1, 2))
check("L04 E3 share", F(4, 5) / 4, F(1, 5))
# L04 M1 directly: c=1/2, b=2, d=1, h=2, A=4, m=3
Dm = 2 * F(1, 2) + 2 * 1
check("L04 M1 D", Dm, F(3))
check("L04 M1 Y*", (2 * 4 + 2 * 3) / Dm, F(14, 3))
check("L04 M1 i*", (1 * 4 - F(1, 2) * 3) / Dm, F(5, 6))
check("L04 M1 IS residual", F(1, 2) * F(14, 3) + 2 * F(5, 6), F(4))

# L05 AD-AS, own implementation
a, eta, Yb, nu, Pe = F(1160), F(100), F(1000), F(200), F(1)
P = (a - Yb + nu * Pe) / (eta + nu)
check("L05 P*", P, F(6, 5))
check("L05 Y*", a - eta * P, F(1040))
P1 = (a + 30 - Yb + nu * Pe) / (eta + nu)
check("L05 dP", P1 - P, F(1, 10))
check("L05 dY", (a + 30 - eta * P1) - (a - eta * P), F(20))
check("L05 LR P before", (a - Yb) / eta, F(8, 5))
check("L05 LR P after", (a + 30 - Yb) / eta, F(19, 10))
for slope in (F(50), F(100), F(200), F(400), F(800)):
    Pa = (a - Yb + slope * Pe) / (eta + slope)
    Pb = (a + 30 - Yb + slope * Pe) / (eta + slope)
    dy = (a + 30 - eta * Pb) - (a - eta * Pa)
    print("L05 Part D nu", slope, "share", float(slope / (eta + slope)), "dY", float(dy), "dP", float(Pb - Pa))
    check(f"L05 dY nu={slope}", dy, 30 * slope / (eta + slope))
check("L05 R2 P*", (1190 - 1000 + 200 * F(13, 10)) / 300, F(3, 2))
check("L05 M1 P*", (1100 - 1000 + 100 * F(11, 10)) / 200, F(21, 20))
check("L05 M2 dY", F(3, 4) * 40, F(30))
check("L05 E2 exact", 30 * (F(8, 9) - F(4, 5)), F(8, 3))

# L06 Phillips, own implementation with its own RNG use (random.Random seed as in the lab)
nu6, kap, un, Pstart, pistart = F(200), F(200), F(5, 100), F(6, 5), F(3, 100)
pe = Pstart * (1 + pistart)
Pn = pe - kap * (F(6, 100) - un) / nu6
check("L06 A inflation", (Pn - Pstart) / Pstart, F(13, 600))
check("L06 A form", pistart - (kap / (nu6 * Pstart)) * (F(6, 100) - un), F(13, 600))
rng = random.Random(20261028)
P_, pi_ = Pstart, pistart
gaps = []
for t in range(12):
    draw = rng.randint(-100, 100)
    gaps.append(draw)
    u = un + F(draw, 10000)
    pe_t = P_ * (1 + pi_)
    Pn = pe_t - kap * (u - un) / nu6
    new_pi = (Pn - P_) / P_
    beta = kap / (nu6 * P_)
    check(f"L06 B t{t+1} identity", new_pi, pi_ - beta * (u - un))
    P_, pi_ = Pn, new_pi
print("L06 gap draws (bp):", gaps)
pos = [g for g in gaps if g > 0]
neg = [g for g in gaps if g < 0]
print("L06 positive-gap periods", len(pos), "negative", len(neg), "zero", gaps.count(0))
check("L06 M2 pi", F(4, 100) - F(8, 10) * F(-1, 100), F(48, 1000))
check("L06 E1 change 4pct", -(F(5, 6)) * (F(4, 100) - un), F(1, 120))
check("L06 E3 beta1", kap / (nu6 * F(6, 5)), F(5, 6))
check("L06 R2 u", un + F(1, 100) / F(5, 6), F(31, 500))
check("L06 M3 change", F(-3, 100) * F(1, 2) * 1, F(-3, 200))
print("FAILS", fails)
