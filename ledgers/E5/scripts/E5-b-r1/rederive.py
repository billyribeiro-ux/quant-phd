"""Independent re-derivation of every numeric claim in E5 L04, L05 and L06 (exact Fractions, no lab code reused).

Usage: python3 -I ledgers/E5/scripts/E5-b-r1/rederive.py
Each check prints CHECK <name> <expected> <recomputed> OK|MISMATCH. Exit 1 on any mismatch.
"""
import random
import sys
from fractions import Fraction as F

sys.set_int_max_str_digits(0)

fails = []


def show(x):
    t = str(x)
    return t if len(t) <= 60 else f"~{float(x):.12g} (exact value has {len(t)} characters)"


def chk(name, expected, got):
    ok = expected == got
    print(f"CHECK {name} expected={show(expected)} recomputed={show(got)} {'OK' if ok else 'MISMATCH'}")
    if not ok:
        fails.append(name)


# ---------- L04 IS-LM ----------
c, c0, b0, b, d, h, tax, G, mbar = F(3, 4), F(1), F(1), F(2), F(1, 2), F(1), F(0), F(1), F(2)
A = lambda g: c0 - c * tax + b0 + g
Dn = lambda bb: h * (1 - c) + bb * d
Ys = lambda g, m, bb: (h * A(g) + bb * m) / Dn(bb)
Is = lambda g, m, bb: (d * A(g) - (1 - c) * m) / Dn(bb)
chk("L04 A(G=1)", F(3), A(G))
chk("L04 D", F(5, 4), Dn(b))
chk("L04 Y*", F(28, 5), Ys(G, mbar, b))
chk("L04 i*", F(4, 5), Is(G, mbar, b))
y0, i0 = Ys(G, mbar, b), Is(G, mbar, b)
chk("L04 IS residual", F(0), y0 - (c0 + c * (y0 - tax) + b0 - b * i0 + G))
chk("L04 LM residual", F(0), d * y0 - h * i0 - mbar)
y1, i1 = Ys(F(11, 10), mbar, b), Is(F(11, 10), mbar, b)
chk("L04 dY G->11/10", F(2, 25), y1 - y0)
chk("L04 multiplier G->11/10", F(4, 5), (y1 - y0) / F(1, 10))
chk("L04 di G->11/10", F(1, 25), i1 - i0)
y2, i2 = Ys(F(2), mbar, b), Is(F(2), mbar, b)
chk("L04 dY G->2", F(4, 5), y2 - y0)
chk("L04 di G->2", F(2, 5), i2 - i0)
chk("L04 benchmark 1/(1-c)", F(4), 1 / (1 - c))
chk("L04 h/D", F(4, 5), h / Dn(b))
ym, im = Ys(G, F(5, 2), b), Is(G, F(5, 2), b)
chk("L04 dY mbar 2->5/2", F(4, 5), ym - y0)
chk("L04 monetary multiplier", F(8, 5), (ym - y0) / F(1, 2))
chk("L04 di per unit mbar", F(-1, 5), (im - i0) / F(1, 2))
chk("L04 b/D", F(8, 5), b / Dn(b))
chk("L04 -(1-c)/D", F(-1, 5), -(1 - c) / Dn(b))
y0b, y1b = Ys(G, mbar, F(0)), Ys(F(2), mbar, F(0))
chk("L04 Part D multiplier b=0", F(4), (y1b - y0b) / F(1))
chk("L04 share h(1-c)/D", F(1, 5), h * (1 - c) / Dn(b))
chk("L04 ratio di/dY E1", F(1, 2), ((i2 - i0) / (y2 - y0)))
# M1-M3 (c=1/2,b=2,d=1,h=2,A=4,m=3)
cc, bb, dd, hh, AA, mm = F(1, 2), F(2), F(1), F(2), F(4), F(3)
DD = hh * (1 - cc) + bb * dd
chk("L04 M1 D", F(3), DD)
chk("L04 M1 Y*", F(14, 3), (hh * AA + bb * mm) / DD)
chk("L04 M1 i*", F(5, 6), (dd * AA - (1 - cc) * mm) / DD)
chk("L04 M2 spending mult", F(2, 3), hh / DD)
chk("L04 M2 benchmark", F(2), 1 / (1 - cc))
chk("L04 M3 dY/dm", F(2, 3), bb / DD)
chk("L04 M3 di/dm", F(-1, 6), -(1 - cc) / DD)
chk("L04 P3 IS slope (c=1/2, b=2)", F(-1, 4), -(1 - cc) / bb)
# E2
chk("L04 E2 -(1/4)/(5/4)", F(-1, 5), -(F(1, 4)) / F(5, 4))
# R2 b=0 monetary multiplier
chk("L04 R2 b/D at b=0", F(0), F(0) / Dn(F(0)))
# quiz numeric: spending multiplier at b=0 with c=3/4,h=1
chk("L04 quiz b=0 multiplier", F(4), h / (h * (1 - c)))

# ---------- L05 AD-AS ----------
ybar, eta, nu, pe, a0 = F(1000), F(100), F(200), F(1), F(1160)


def sr(a, e, n, yb, p_e):
    p = (a - yb + n * p_e) / (e + n)
    return p, a - e * p


p0, y0s = sr(a0, eta, nu, ybar, pe)
chk("L05 P*", F(6, 5), p0)
chk("L05 Y*", F(1040), y0s)
chk("L05 AS residual", F(0), y0s - (ybar + nu * (p0 - pe)))
p1, y1s = sr(a0 + 30, eta, nu, ybar, pe)
chk("L05 dP shock 30", F(1, 10), p1 - p0)
chk("L05 dY shock 30", F(20), y1s - y0s)
chk("L05 output share", F(2, 3), nu / (eta + nu))
chk("L05 price share per a", F(1, 300), 1 / (eta + nu))
for slope, share_e, dp_e, dy_e in [(50, F(1, 3), F(1, 5), F(10)), (100, F(1, 2), F(3, 20), F(15)),
                                   (200, F(2, 3), F(1, 10), F(20)), (400, F(4, 5), F(3, 50), F(24)),
                                   (800, F(8, 9), F(1, 30), F(80, 3))]:
    pa, ya = sr(a0, eta, F(slope), ybar, pe)
    pb, yb = sr(a0 + 30, eta, F(slope), ybar, pe)
    chk(f"L05 Part D nu={slope} share", share_e, F(slope) / (eta + F(slope)))
    chk(f"L05 Part D nu={slope} dP", dp_e, pb - pa)
    chk(f"L05 Part D nu={slope} dY", dy_e, yb - ya)
lr0, lr1 = (a0 - ybar) / eta, (a0 + 30 - ybar) / eta
chk("L05 LR price before", F(8, 5), lr0)
chk("L05 LR price after", F(19, 10), lr1)
chk("L05 LR dP = da/eta", F(3, 10), lr1 - lr0)
chk("L05 LR fixed point", lr1, sr(a0 + 30, eta, nu, ybar, lr1)[0])
chk("L05 E1 nu=400 dY", F(24), F(4, 5) * 30)
chk("L05 E1 nu=400 dP", F(3, 50), F(30, 500))
chk("L05 E2 increment 800-400", F(8, 3), 30 * (F(8, 9) - F(4, 5)))
# M1 (a=1100, eta=100, ybar=1000, nu=100, pe=1.1)
pm, ym_ = sr(F(1100), F(100), F(100), ybar, F(11, 10))
chk("L05 M1 P*", F(21, 20), pm)
chk("L05 M1 Y*", F(995), ym_)
# M2 (eta=50 nu=150 da=40)
chk("L05 M2 share", F(3, 4), F(150) / F(200))
chk("L05 M2 dY", F(30), F(3, 4) * 40)
chk("L05 M2 dP", F(1, 5), F(40) / F(200))
# M3 (a=1100 -> 1140)
chk("L05 M3 LR before", F(1), (F(1100) - ybar) / F(100))
chk("L05 M3 LR after", F(7, 5), (F(1140) - ybar) / F(100))
# P2/P3 numeric
chk("L05 P3 identity", F(0), (F(1100) - ybar) / F(100) - ((F(1100) - ybar + F(100) * ((F(1100) - ybar) / F(100))) / F(200)))
# R2: a=1190, pe=1.3
pr2, yr2 = sr(F(1190), eta, nu, ybar, F(13, 10))
chk("L05 R2 P*", F(3, 2), pr2)
chk("L05 R2 Y*", F(1040), yr2)
# R3 gap
chk("L05 R3 output gap", F(60), sr(F(1190), eta, nu, ybar, F(1))[1] - ybar)
# misconception: demand values
chk("L05 misc demand P=1", F(1060), F(1160) - 100 * 1)
chk("L05 misc demand P=1.6", F(1000), F(1160) - 100 * F(16, 10))

# ---------- L06 Phillips ----------
kap, nu6, un, P0, pi0 = F(200), F(200), F(5, 100), F(6, 5), F(3, 100)
beta = lambda P: kap / (nu6 * P)
chk("L06 beta at P=6/5", F(5, 6), beta(P0))
chk("L06 beta at P=1", F(1), beta(F(1)))
chk("L06 M1 beta", F(1, 2), F(100) / (F(200) * 1))
chk("L06 M1 pi", F(3, 100), F(4, 100) - F(1, 2) * F(2, 100))
chk("L06 M2 beta", F(4, 5), F(200) / (F(200) * F(5, 4)))
chk("L06 M2 pi", F(48, 1000), F(4, 100) - F(4, 5) * F(-1, 100))
chk("L06 M3 at u=un", F(2, 100), F(2, 100) - F(1, 2) * 0)
chk("L06 M3 at u=un+0.03", F(5, 1000), F(2, 100) - F(1, 2) * F(3, 100))
pe_a = P0 * (1 + pi0)
pa_ = pe_a - kap * (F(6, 100) - un) / nu6
chk("L06 Part A pe", F(1236, 1000), pe_a)
chk("L06 Part A price", F(1226, 1000), pa_)
chk("L06 Part A inflation levels", F(13, 600), (pa_ - P0) / P0)
chk("L06 Part A Phillips", F(13, 600), pi0 - beta(P0) * (F(6, 100) - un))
chk("L06 E1 change at 4%", F(1, 120), -(F(5, 6)) * (F(4, 100) - un))
chk("L06 misc1 change at -0.01", F(1, 120), -(F(5, 6)) * F(-1, 100))
chk("L06 misc2 change at 3%", F(1, 60), -(F(5, 6)) * (F(3, 100) - un))
chk("L06 E3 beta1", F(5, 6), kap / (nu6 * P0))
chk("L06 E3 change period1", F(-5, 6) * F(58, 10000), -(F(5, 6)) * F(58, 10000))
chk("L06 E3 5.5% change", F(-5, 6) * F(5, 1000), -(F(5, 6)) * (F(55, 1000) - un))
chk("L06 R1 ratio", F(6, 5), F(1) / (F(5, 6)))
chk("L06 R2 u*", F(62, 1000), un + F(1, 100) / F(5, 6))
chk("L06 quiz q4", F(1, 120), -(F(5, 6)) * (F(4, 100) - un))
chk("L06 quiz q6", F(13, 600), F(3, 100) - F(5, 6) * F(1, 100))
chk("L06 quiz q9", F(48, 1000), F(4, 100) - F(8, 10) * F(-1, 100))

# Part B seeded path: recompute inflation by the Phillips recursion (no price levels), compare to printed values.
printed = {1: (58, "0.025167", "-0.004833"), 2: (42, "0.021753", "-0.003414"), 3: (76, "0.015706", "-0.006046"),
           4: (85, "0.009048", "-0.006658"), 5: (49, "0.005245", "-0.003804"), 6: (-89, "0.012117", "0.006873"),
           7: (48, "0.008455", "-0.003662"), 8: (75, "0.002781", "-0.005674"), 9: (-46, "0.006252", "0.003470"),
           10: (-91, "0.013074", "0.006823"), 11: (27, "0.011076", "-0.001998"), 12: (38, "0.008295", "-0.002782")}
rng = random.Random(20261028)
pi_prev, P_prev = pi0, P0
zero_gap = no_change = 0
for t in range(1, 13):
    draw = rng.randint(-100, 100)
    gap = F(draw, 10000)
    u = un + gap
    pi_t = pi_prev - beta(P_prev) * (u - un)     # Phillips form with A3 (pi^e = pi_{t-1})
    P_t = P_prev * (1 + pi_t)
    pi_t_from_levels = (P_t - P_prev) / P_prev
    chk(f"L06 Part B t={t} identity", pi_t, pi_t_from_levels)
    pr_draw, pr_infl, pr_change = printed[t]
    chk(f"L06 Part B t={t} draw", pr_draw, draw)
    chk(f"L06 Part B t={t} inflation(6dp)", pr_infl, f"{float(round(pi_t * 10**6) / 10**6):.6f}")
    chk(f"L06 Part B t={t} change(6dp)", pr_change, f"{float(round((pi_t - pi_prev) * 10**6) / 10**6):.6f}")
    zero_gap += gap == 0
    no_change += pi_t == pi_prev
    pi_prev, P_prev = pi_t, P_t
chk("L06 Part B zero_gap_periods", 0, zero_gap)
chk("L06 Part B no_change_periods", 0, no_change)

print("MISMATCHES:", fails if fails else "none")
raise SystemExit(1 if fails else 0)
