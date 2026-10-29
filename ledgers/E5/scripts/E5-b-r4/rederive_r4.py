"""Verifier round 4 (E5 slice b): independent re-derivation of every number in the L04-L06 text changed since ccfdf4c,
and of the cards that cite them. Exact Fractions only; the seeded path is re-drawn with random.Random.

Usage: python3 -I ledgers/E5/scripts/E5-b-r4/rederive_r4.py
"""
import random
from fractions import Fraction as F

fails = []


def chk(name, got, want):
    ok = got == want
    print(f"{name}: got={got} want={want} {'OK' if ok else 'MISMATCH'}")
    if not ok:
        fails.append(name)


# L04 Derivation/Prop 4.2/4.3 at the Lab 1 and M1 parameters
c, b, d, h, G, m = F(3, 4), F(2), F(1, 2), F(1), F(1), F(2)
A = F(1) + F(1) + G  # c0 + b0 + G with Tax 0
D = h * (1 - c) + b * d
chk("L04 A", A, F(3))
chk("L04 D", D, F(5, 4))
chk("L04 Y*", (h * A + b * m) / D, F(28, 5))
chk("L04 i*", (d * A - (1 - c) * m) / D, F(4, 5))
chk("L04 h/D", h / D, F(4, 5))
chk("L04 1/(1-c)", 1 / (1 - c), F(4))
chk("L04 b/D", b / D, F(8, 5))
chk("L04 -(1-c)/D", -(1 - c) / D, F(-1, 5))
chk("L04 E1 ratio di/dY", (F(1, 25)) / (F(2, 25)), F(1, 2))
chk("L04 E1 closed d/h", d / h, F(1, 2))
chk("L04 E3 share", h * (1 - c) / D, F(1, 5))
# M1 at c=1/2,b=2,d=1,h=2,A=4,m=3
c1, b1, d1, h1, A1, m1 = F(1, 2), F(2), F(1), F(2), F(4), F(3)
D1 = h1 * (1 - c1) + b1 * d1
chk("L04 M1 D", D1, F(3))
chk("L04 M1 Y*", (h1 * A1 + b1 * m1) / D1, F(14, 3))
chk("L04 M1 i*", (d1 * A1 - (1 - c1) * m1) / D1, F(5, 6))
chk("L04 M1 IS check", (1 - c1) * F(14, 3) + b1 * F(5, 6), A1)
chk("L04 M1 LM check", d1 * F(14, 3) - h1 * F(5, 6), m1)
chk("L04 M2 h/D", h1 / D1, F(2, 3))
chk("L04 M2 ratio to benchmark", (h1 / D1) / (1 / (1 - c1)), F(1, 3))
chk("L04 M3 b/D", b1 / D1, F(2, 3))
chk("L04 M3 -(1-c)/D", -(1 - c1) / D1, F(-1, 6))
chk("L04 M3 at m 3", F(2, 3) * 1, F(2, 3))
# P2: h(1-c)/D at b=0 ; R1 at d=0
chk("L04 R1 h/D at d=0", h / (h * (1 - c)), 1 / (1 - c))
# misconception 2: output rise 4/5 for G 1->2 at Lab params
Y0 = F(28, 5)
Y2 = (h * (A + 1) + b * m) / D
chk("L04 mis2 dY for G 1->2", Y2 - Y0, F(4, 5))
chk("L04 mis2 di for G 1->2", (d * (A + 1) - (1 - c) * m) / D - F(4, 5), F(2, 5))

# L05 numbers
a, eta, Yb, nu, Pe = F(1160), F(100), F(1000), F(200), F(1)
P0 = (a - Yb + nu * Pe) / (eta + nu)
Y0 = a - eta * P0
chk("L05 P*", P0, F(6, 5))
chk("L05 Y*", Y0, F(1040))
chk("L05 misc demand at P=1", a - eta * 1, F(1060))
chk("L05 misc demand at P=1.6", a - eta * F(8, 5), F(1000))
chk("L05 misc demand fall", (a - eta * 1) - (a - eta * F(8, 5)), F(60))
chk("L05 dP", F(30) / (eta + nu), F(1, 10))
chk("L05 dY", nu * F(30) / (eta + nu), F(20))
chk("L05 output share 2/3", nu / (eta + nu), F(2, 3))
chk("L05 LR P before", (a - Yb) / eta, F(8, 5))
chk("L05 LR P after", (a + 30 - Yb) / eta, F(19, 10))
chk("L05 LR change", F(30) / eta, F(3, 10))
# post-shift point with Pe stuck at 1: Y = 1060, gap 60
a2 = a + 30
P_stuck = (a2 - Yb + nu * Pe) / (eta + nu)
chk("L05 stuck-Pe Y", a2 - eta * P_stuck, F(1060))
chk("L05 stuck-Pe gap", a2 - eta * P_stuck - Yb, F(60))
# Remark 2.3 limit and Part D shares
chk("L05 share at nu 50", F(50, 150), F(1, 3))
chk("L05 share at nu 800", F(800, 900), F(8, 9))
chk("L05 price change nu 400", F(30, 500), F(3, 50))
chk("L05 output change 400->800 increment", F(30) * (F(8, 9) - F(4, 5)), F(8, 3))
# M2
chk("L05 M2 share", F(150, 200), F(3, 4))
chk("L05 M2 dY", F(3, 4) * 40, F(30))
chk("L05 M2 dP", F(40, 200), F(1, 5))
# M1
P_m1 = (F(1100) - F(1000) + F(100) * F(11, 10)) / (F(100) + F(100))
chk("L05 M1 P*", P_m1, F(21, 20))
chk("L05 M1 Y*", F(1100) - F(100) * P_m1, F(995))
# M3
chk("L05 M3 LR before", (F(1100) - F(1000)) / F(100), F(1))
chk("L05 M3 LR after", (F(1140) - F(1000)) / F(100), F(7, 5))
# R2: a=1190, Pe=1.3
chk("L05 R2 P*", (F(190) + F(200) * F(13, 10)) / F(300), F(3, 2))
chk("L05 R2 Y*", F(1190) - F(100) * F(3, 2), F(1040))
# E2 increments
ys = [F(10), F(15), F(20), F(24), F(80, 3)]
chk("L05 E2 increments", [ys[i + 1] - ys[i] for i in range(4)], [F(5), F(5), F(4), F(8, 3)])
# E3 long-run prices
chk("L05 E3 19/10 - 8/5", F(19, 10) - F(8, 5), F(3, 10))
# Lab 1 Part B expected exact fractions
# misconception: shock of 30, output change share (2/3 of 30 = 20)
chk("L05 mis2 share of 30", F(2, 3) * 30, F(20))
# R1 (non-linear) is a proof, no numbers.

# L06 numbers
kappa, nu6, un = F(200), F(200), F(5, 100)
P_prev = F(6, 5)
pi_e = P_prev * (1 + F(3, 100))
beta6 = kappa / (nu6 * P_prev)
chk("L06 beta at 6/5", beta6, F(5, 6))
chk("L06 beta at 1", kappa / (nu6 * 1), F(1))
chk("L06 Part A pe", pi_e, F(309, 250))
u_a = F(6, 100)
P_a = pi_e - kappa * (u_a - un) / nu6
chk("L06 Part A price", P_a, F(1226, 1000))
chk("L06 Part A inflation", (P_a - P_prev) / P_prev, F(13, 600))
chk("L06 Part A form", F(3, 100) - beta6 * (u_a - un), F(13, 600))
chk("L06 misc1 change at gap -0.01", -beta6 * (F(4, 100) - un), F(1, 120))
chk("L06 misc2 change at 3pct", -beta6 * (F(3, 100) - un), F(1, 60))
chk("L06 E1 4pct change", -(F(5, 6)) * (F(4, 100) - un), F(1, 120))
chk("L06 M1 beta", F(100) / (F(200) * 1), F(1, 2))
chk("L06 M1 pi", F(4, 100) - F(1, 2) * F(2, 100), F(3, 100))
chk("L06 M2 beta", F(200) / (F(200) * F(5, 4)), F(4, 5))
chk("L06 M2 pi", F(4, 100) - F(4, 5) * F(-1, 100), F(48, 1000))
chk("L06 M3 change at gap 0.03", -F(1, 2) * F(3, 100), F(-3, 200))
chk("L06 M3 pi at gap 0.03", F(2, 100) - F(1, 2) * F(3, 100), F(5, 1000))
chk("L06 R2 u", un + F(1, 100) / F(5, 6), F(31, 500))
chk("L06 R2 as percent", (un + F(1, 100) / F(5, 6)) * 100, F(62, 10))
chk("L06 R1 ratio", (1 / (F(5, 6))) / (1 / 1) * 1 if False else F(1) / (F(5, 6)), F(6, 5))
chk("L06 E3 58bp slope*gap", -(F(5, 6)) * F(58, 10000), F(-29, 6000))
chk("L06 E3 5.5pct", -(F(5, 6)) * F(5, 1000) * 1, F(-1, 240))
chk("L06 quiz q6 pi", F(3, 100) - F(5, 6) * F(1, 100), F(13, 600))
chk("L06 quiz q9 pi", F(4, 100) - F(4, 5) * F(-1, 100), F(48, 1000))

# Part C grid signs and values at P=6/5
for step in range(-4, 5):
    u = un + F(step, 200)
    ch = -beta6 * (u - un)
    if step == 0:
        assert ch == 0
    print(f"L06 PartC grid step {step}: u={float(u)*100:.1f}% change={float(ch):.6f}")

# Seeded path re-draw (independent loop, same RNG call sequence as the lab)
rng = random.Random(20261028)
P, pi = F(6, 5), F(3, 100)
zero_gap = no_change = 0
pos_gap_neg_change = 0
neg_gap_pos_change = 0
all_ok = True
rows = []
for t in range(1, 13):
    draw = rng.randint(-100, 100)
    gap = F(draw, 10000)
    u = un + gap
    pe_t = P * (1 + pi)
    Pn = pe_t - kappa * (u - un) / nu6
    pin = (Pn - P) / P
    all_ok &= pin == pi - (kappa / (nu6 * P)) * (u - un)
    zero_gap += gap == 0
    no_change += pin == pi
    if gap > 0:
        pos_gap_neg_change += (pin - pi) < 0
    if gap < 0:
        neg_gap_pos_change += (pin - pi) > 0
    rows.append((t, draw, float(pin), float(pin - pi)))
    P, pi = Pn, pin
print("path rows (t, gap_bp, inflation, change):")
for r in rows:
    print(f"  {r[0]:2d} {r[1]:5d} {r[2]:.6f} {r[3]:+.6f}")
chk("L06 path identity every period", all_ok, True)
chk("L06 path zero_gap_periods", zero_gap, 0)
chk("L06 path no_change_periods", no_change, 0)
chk("L06 path positive gaps", sum(1 for r in rows if r[1] > 0), 9)
chk("L06 path negative gaps", sum(1 for r in rows if r[1] < 0), 3)
chk("L06 path pos gap with negative change", pos_gap_neg_change, 9)
chk("L06 path neg gap with positive change", neg_gap_pos_change, 3)

print("ALL_OK" if not fails else f"FAILS: {fails}")
