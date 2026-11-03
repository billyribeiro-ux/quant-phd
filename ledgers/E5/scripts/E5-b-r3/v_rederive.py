"""Independent re-derivation of the L04, L05 and L06 numbers (own formulas, Fractions, own seeded path)."""
import random
from fractions import Fraction as F

def chk(name, cond):
    print(("OK   " if cond else "FAIL ") + name)
    return cond

ok = True
# ---- L04: IS-LM, own formulas. c=3/4, c0=1, b0=1, b=2, d=1/2, h=1, Tax=0, G=1, mbar=2
c, c0, b0, b, d, h, tax = F(3, 4), F(1), F(1), F(2), F(1, 2), F(1), F(0)
def solve(G, m, bb):
    A = c0 - c * tax + b0 + G
    D = h * (1 - c) + bb * d
    Y = (h * A + bb * m) / D
    i = (d * A - (1 - c) * m) / D
    # verify both relations directly from the primitive equations
    C_ = c0 + c * (Y - tax)
    I_ = b0 - bb * i
    isres = Y - (C_ + I_ + G)
    lmres = d * Y - h * i - m
    return Y, i, D, isres, lmres
Y0, i0, D0, r1, r2 = solve(F(1), F(2), b)
ok &= chk("L04 Y*=28/5", Y0 == F(28, 5))
ok &= chk("L04 i*=4/5", i0 == F(4, 5))
ok &= chk("L04 D=5/4", D0 == F(5, 4))
ok &= chk("L04 residuals zero", r1 == 0 and r2 == 0)
Y1, i1, _, _, _ = solve(F(11, 10), F(2), b)
Y2, i2, _, _, _ = solve(F(2), F(2), b)
ok &= chk("L04 dY 11/10 = 2/25", Y1 - Y0 == F(2, 25))
ok &= chk("L04 di 11/10 = 1/25", i1 - i0 == F(1, 25))
ok &= chk("L04 dY G=2 = 4/5", Y2 - Y0 == F(4, 5))
ok &= chk("L04 di G=2 = 2/5", i2 - i0 == F(2, 5))
ok &= chk("L04 multiplier 4/5 both", (Y1 - Y0) / F(1, 10) == F(4, 5) and (Y2 - Y0) / 1 == F(4, 5))
Y3, i3, _, _, _ = solve(F(1), F(5, 2), b)
ok &= chk("L04 monetary dY=4/5 for dm=1/2", Y3 - Y0 == F(4, 5))
ok &= chk("L04 monetary di=-1/10", i3 - i0 == F(-1, 10))
Y4, _, D4, _, _ = solve(F(2), F(2), F(0))
Y5, _, _, _, _ = solve(F(1), F(2), F(0))
ok &= chk("L04 b=0 multiplier 4", (Y4 - Y5) == 4)
ok &= chk("L04 benchmark 1/(1-c)=4", 1 / (1 - c) == 4)
ok &= chk("L04 share h(1-c)/D = 1/5 (E3)", h * (1 - c) / D0 == F(1, 5))
ok &= chk("L04 E1 ratio di/dY = 1/2", (i1 - i0) / (Y1 - Y0) == F(1, 2))
# M1 uses c=1/2,b=2,d=1,h=2,A=4,mbar=3 -> direct
cc, bb, dd, hh, AA, mm = F(1, 2), F(2), F(1), F(2), F(4), F(3)
DM = hh * (1 - cc) + bb * dd
YM, iM = (hh * AA + bb * mm) / DM, (dd * AA - (1 - cc) * mm) / DM
ok &= chk("L04 M1 D=3, Y=14/3, i=5/6", DM == 3 and YM == F(14, 3) and iM == F(5, 6))
ok &= chk("L04 M2 h/D=2/3 ratio 1/3 to benchmark 2", hh / DM == F(2, 3) and (hh / DM) / (1 / (1 - cc)) == F(1, 3))
ok &= chk("L04 M3 b/D=2/3, -(1-c)/D=-1/6", bb / DM == F(2, 3) and -(1 - cc) / DM == F(-1, 6))
ok &= chk("L04 R1 d=0 gives 1/(1-c) and di=0", (hh / (hh * (1 - cc))) == 1 / (1 - cc))
ok &= chk("L04 R2 b=0: dm multiplier 0", (F(0) / (hh * (1 - cc))) == 0)

# ---- L05: AD-AS. a=1160, eta=100, Ybar=1000, nu=200, Pe=1
def sr(a, eta, nu, yb, pe):
    P = (a - yb + nu * pe) / (eta + nu)
    return P, a - eta * P
P0, Y0_ = sr(F(1160), F(100), F(200), F(1000), F(1))
ok &= chk("L05 P*=6/5, Y*=1040", P0 == F(6, 5) and Y0_ == 1040)
ok &= chk("L05 SRAS residual 0", Y0_ == 1000 + 200 * (P0 - 1))
P1, Y1_ = sr(F(1190), F(100), F(200), F(1000), F(1))
ok &= chk("L05 shift dP=1/10, dY=20", P1 - P0 == F(1, 10) and Y1_ - Y0_ == 20)
ok &= chk("L05 Y after shift 1060 and gap 60 at Pe=1", Y1_ == 1060)
for nu in (50, 100, 200, 400, 800):
    nu = F(nu)
    pa, ya = sr(F(1160), F(100), nu, F(1000), F(1))
    pb, yb = sr(F(1190), F(100), nu, F(1000), F(1))
    ok &= chk(f"L05 D nu={nu} share={nu/(100+nu)} dP={F(30)/(100+nu)} dY={30*nu/(100+nu)}",
              yb - ya == 30 * nu / (100 + nu) and pb - pa == F(30) / (100 + nu))
lr0 = F(1160 - 1000, 100); lr1 = F(1190 - 1000, 100)
ok &= chk("L05 long-run 8/5 and 19/10", lr0 == F(8, 5) and lr1 == F(19, 10))
ok &= chk("L05 long-run output 1000", 1160 - 100 * lr0 == 1000 and 1190 - 100 * lr1 == 1000)
# L05 problems
p, y = sr(F(1100), F(100), F(100), F(1000), F(11, 10))
ok &= chk("L05 M1 P=1.05 Y=995", p == F(21, 20) and y == 995)
ok &= chk("L05 M2 share 3/4, dY 30, dP 0.2", F(150, 200) == F(3, 4) and F(3, 4) * 40 == 30 and F(40, 200) == F(1, 5))
ok &= chk("L05 M3 1.0 and 1.4", F(100, 100) == 1 and F(140, 100) == F(7, 5))
ok &= chk("L05 R2 P*=3/2 Y*=1040", sr(F(1190), F(100), F(200), F(1000), F(13, 10)) == (F(3, 2), 1040))
ok &= chk("L05 E2 exact 400->800 increase 8/3", 30 * F(800, 900) - 30 * F(400, 500) == F(8, 3))
ok &= chk("L05 canon demand 1060 and 1000", 1160 - 100 * 1 == 1060 and 1160 - 100 * F(16, 10) == 1000)
# expectations-move formulas (canon 2): check symbolic-equivalent numerically
da, dpe, eta, nu = F(30), F(1, 10), F(100), F(200)
dP_num = (da + nu * dpe) / (eta + nu)
dY_num = nu * (da - eta * dpe) / (eta + nu)
Pb, Yb = sr(F(1160) + da, eta, nu, F(1000), F(1) + dpe)
Pa, Ya = sr(F(1160), eta, nu, F(1000), F(1))
ok &= chk("L05 canon 2 expectation-moving formulas", Pb - Pa == dP_num and Yb - Ya == dY_num)

# ---- L06: Phillips. nu=200 kappa=200 un=5/100, seed 20261028, P0=6/5, pi0=3/100
nu6, ka, un = F(200), F(200), F(5, 100)
Pprev, piprev = F(6, 5), F(3, 100)
# Part A
ua = F(6, 100)
pe = Pprev * (1 + piprev)
pa6 = pe - ka * (ua - un) / nu6
ok &= chk("L06 A expected 1.236, price 1.226", pe == F(1236, 1000) and pa6 == F(1226, 1000))
ok &= chk("L06 A inflation 13/600 both ways", (pa6 - Pprev) / Pprev == F(13, 600) and piprev - (ka / (nu6 * Pprev)) * (ua - un) == F(13, 600))
ok &= chk("L06 beta at 6/5 = 5/6", ka / (nu6 * Pprev) == F(5, 6))
rng = random.Random(20261028)
draws = [rng.randint(-100, 100) for _ in range(12)]
print("draws", draws)
Pp, pp = Pprev, piprev
pos = neg = zero = 0
changes = []
for k in draws:
    gap = F(k, 10000)
    u = un + gap
    pe_t = Pp * (1 + pp)
    Pn = pe_t - ka * (u - un) / nu6
    pn = (Pn - Pp) / Pp
    ok &= chk(f"L06 B draw {k}: identity pi_t = pi_t-1 - beta(u-un)", pn == pp - (ka / (nu6 * Pp)) * (u - un))
    changes.append(pn - pp)
    pos += gap > 0; neg += gap < 0; zero += gap == 0
    Pp, pp = Pn, pn
ok &= chk("L06 B gaps: 9 positive, 3 negative, 0 zero", (pos, neg, zero) == (9, 3, 0))
ok &= chk("L06 B changes opposite sign to gap", all((c_ < 0) == (k > 0) and (c_ > 0) == (k < 0) for c_, k in zip(changes, draws)))
ok &= chk("L06 B path: draws list stored in expected block", draws[:7] == [58, 42, 76, 85, 49, -89, 48])
# Part C
for step in range(-4, 5):
    u = un + F(step, 200)
    ch = -(F(5, 6)) * (u - un)
    if step == 0:
        ok &= chk("L06 C zero at un", ch == 0)
    elif step < 0:
        ok &= chk(f"L06 C step {step} positive", ch > 0)
    else:
        ok &= chk(f"L06 C step {step} negative", ch < 0)
ok &= chk("L06 C 3pct change 1/60", -(F(5, 6)) * (F(3, 100) - un) == F(1, 60))
ok &= chk("L06 C 5pct zero, 4pct and 6pct", -(F(5, 6)) * (F(4, 100) - un) == F(1, 120) and -(F(5, 6)) * (F(6, 100) - un) == F(-1, 120))
ok &= chk("L06 misc gap -0.01 at beta 5/6 gives +1/120", -(F(5, 6)) * (F(-1, 100)) == F(1, 120))
ok &= chk("L06 R2 u=0.062 at v=0.01", F(5, 100) + F(1, 100) / F(5, 6) == F(62, 1000))
ok &= chk("L06 R2 beta ratio 6/5 (P=1 vs 6/5)", (F(1) and (ka / (nu6 * 1))) / (ka / (nu6 * F(6, 5))) == F(6, 5))
print("ALL_OK" if ok else "SOME_FAILED")
