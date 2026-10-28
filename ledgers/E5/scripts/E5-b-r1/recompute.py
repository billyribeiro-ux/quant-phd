"""Independent recomputation of the numbers printed or claimed on E5 L04-L06 (verifier script, not the lab code)."""
from fractions import Fraction as F
import random

def ok(name, cond):
    print(("PASS " if cond else "FAIL ") + name)

# ---- L04 IS-LM, parameters c=3/4, c0=1, b0=1, b=2, d=1/2, h=1, Tax=0, G=1, mbar=2
c, c0, b0, b, d, h, tax, mbar = F(3,4), F(1), F(1), F(2), F(1,2), F(1), F(0), F(2)
def eq(G, m, bb):
    A = c0 - c*tax + b0 + G
    D = h*(1-c) + bb*d
    Y = (h*A + bb*m)/D
    i = (d*A - (1-c)*m)/D
    # independent check: solve the 2x2 system with Fraction Gaussian elimination
    # (1-c)Y + bb*i = A ; d*Y - h*i = m
    det = (1-c)*(-h) - bb*d
    Y2 = (A*(-h) - bb*m)/det
    i2 = ((1-c)*m - d*A)/det
    assert (Y, i) == (Y2, i2)
    return Y, i, A, D
Y0, i0, A0, D0 = eq(F(1), mbar, b)
ok("L04 A: Y*=28/5", Y0 == F(28,5)); ok("L04 A: i*=4/5", i0 == F(4,5)); ok("L04 A: D=5/4", D0 == F(5,4))
Y1, i1, _, _ = eq(F(11,10), mbar, b); Y2_, i2_, _, _ = eq(F(2), mbar, b)
ok("L04 B: dY step 1.1 = 2/25", Y1-Y0 == F(2,25)); ok("L04 B: multiplier 4/5 (step 1.1)", (Y1-Y0)/F(1,10) == F(4,5))
ok("L04 B: di step 1.1 = 1/25", i1-i0 == F(1,25)); ok("L04 B: dY step 2 = 4/5", Y2_-Y0 == F(4,5))
ok("L04 B: di step 2 = 2/5", i2_-i0 == F(2,5))
ok("L04 C: monetary multiplier 8/5", (eq(F(1), F(5,2), b)[0]-Y0)/F(1,2) == F(8,5))
ok("L04 C: di per unit -1/5", (eq(F(1), F(5,2), b)[1]-i0)/F(1,2) == F(-1,5))
ok("L04 D: b=0 multiplier 4", (eq(F(2), mbar, F(0))[0]-eq(F(1), mbar, F(0))[0]) == 4)
# E1 printed ratio (di/dY) equals d/h
ok("L04 E1: di/dY = 1/2 (step 1.1)", (i1-i0)/(Y1-Y0) == F(1,2))
# E3 share: multiplier at b=2 over benchmark at b=0 = 1/5 ; closed form h(1-c)/D
share = (F(4,5))/4
ok("L04 E3: share 1/5", share == F(1,5)); ok("L04 E3: D/(h(1-c)) = 5 (reciprocal of share)", D0/(h*(1-c)) == 5)
# Misconception: benchmark 1/(1-c)=4
ok("L04 benchmark 1/(1-c)=4", 1/(1-c) == 4)

# Quiz numeric
ok("L04 quiz: Y*=5.6", float(Y0) == 5.6)

# ---- L05
a, bb5, Ybar, s, Pe = F(1160), F(100), F(1000), F(200), F(1)
P0 = (a - Ybar + s*Pe)/(bb5+s); Yc0 = a - bb5*P0
ok("L05 A: P*=6/5", P0 == F(6,5)); ok("L05 A: Y*=1040", Yc0 == 1040)
P1 = ((a+30) - Ybar + s*Pe)/(bb5+s); Yc1 = (a+30) - bb5*P1
ok("L05 B: dP=1/10", P1-P0 == F(1,10)); ok("L05 B: dY=20", Yc1-Yc0 == 20)
ok("L05 B: P1=13/10, Y1=1060", P1 == F(13,10) and Yc1 == 1060)
for slope in (50,100,200,400,800):
    sl = F(slope)
    pa = (a-Ybar+sl*Pe)/(bb5+sl); pb = ((a+30)-Ybar+sl*Pe)/(bb5+sl)
    ya = a-bb5*pa; yb = (a+30)-bb5*pb
    print("L05 D s=%d share=%s dP=%s dY=%s" % (slope, float(sl/(bb5+sl)), float(pb-pa), float(yb-ya)))
ok("L05 E2: printed increases 5,5,4 and 8/3 (=2.666667)", (15-10)==5 and (20-15)==5 and (24-20)==4 and round(float(F(8,3)),6)==2.666667)
ok("L05 E2: 30*(8/9-4/5)=8/3", 30*(F(8,9)-F(4,5)) == F(8,3))
lr0 = (a-Ybar)/bb5; lr1 = (a+30-Ybar)/bb5
ok("L05 C: LR prices 8/5 and 19/10", lr0 == F(8,5) and lr1 == F(19,10))
ok("L05 C: dP_LR=3/10", lr1-lr0 == F(3,10))
ok("L05 canon: with Pe=1 after shift Y=1060, gap 60", (a+30) - bb5*(((a+30)-Ybar+s*Pe)/(bb5+s)) - Ybar == 60)
ok("L05 misc: demand at P=1.6 is 1000", a - bb5*F(16,10) == 1000)
ok("L05 R2: next SR eq with Pe=1.3 is P=3/2, Y=1040", ((F(1190)-Ybar+s*F(13,10))/(bb5+s) == F(3,2)) and (F(1190)-bb5*F(3,2) == 1040))
# L05-M1, M2, M3
ok("L05 M1: P*=1.05, Y*=995", (F(1100)-F(1000)+F(100)*F(11,10))/F(200) == F(21,20) and F(1100)-F(100)*F(21,20) == 995)
ok("L05 M2: share 3/4, dY 30, dP 0.2", F(150,200)==F(3,4) and F(3,4)*40==30 and F(40,200)==F(1,5))
ok("L05 M3: LR 1 and 1.4", (F(1100)-F(1000))/F(100)==1 and (F(1140)-F(1000))/F(100)==F(14,10))
ok("L05 E1: 400/500, dY 24, dP 0.06", F(400,500)==F(4,5) and F(4,5)*30==24 and F(30,500)==F(6,100))

# ---- L06
kappa, s6, un, P_start, pi0 = F(200), F(200), F(5,100), F(6,5), F(3,100)
u_a = F(6,100); pe_a = P_start*(1+pi0); pA = pe_a - kappa*(u_a-un)/s6
piA = (pA-P_start)/P_start
beta = kappa/(s6*P_start)
ok("L06 A: pi_levels == 13/600", piA == F(13,600))
ok("L06 A: Phillips form equals levels", pi0 - beta*(u_a-un) == piA)
# Part B: recompute seeded path independently
rng = random.Random(20261028)
P, pi = P_start, pi0
rows = []
for t in range(1, 13):
    dr = rng.randint(-100, 100)
    gap = F(dr, 10000)
    u = un + gap
    pe = P*(1+pi)
    Pn = pe - kappa*(u-un)/s6
    pin = (Pn-P)/P
    rows.append((t, dr, float(u*100), float(pin), float(pin-pi), pin == pi - (kappa/(s6*P))*(u-un)))
    P, pi = Pn, pin
for r in rows:
    print("L06 B t=%d draw=%d u=%.2f%% pi=%.6f change=%.6f identity=%s" % (r[0], r[1], r[2], r[3], r[4], r[5]))
ok("L06 B: 12 identities hold", all(r[5] for r in rows))
signs = [(r[1], r[4]) for r in rows]
ok("L06 E2: 9 positive gaps, 3 negative", sum(1 for x in signs if x[0] > 0) == 9 and sum(1 for x in signs if x[0] < 0) == 3)
ok("L06 E2: opposite signs in all 12", all((x[0] > 0 and x[1] < 0) or (x[0] < 0 and x[1] > 0) for x in signs))
ok("L06 E3: beta1 = 5/6", beta == F(5,6))
ok("L06 E3: -(5/6)(0.0058) = -0.0048333", abs(float(-F(5,6)*F(58,10000)) + 0.0048333333) < 1e-9)
ok("L06 E3: 5.5% row change -(5/6)(0.005) = -0.004167", abs(float(-F(5,6)*F(5,1000)) + 0.0041666667) < 1e-9)
ok("L06 Part C 3%: change 1/60 = 0.016667", -beta*(F(3,100)-un) == F(1,60))
ok("L06 R2: u=0.062", un + F(1,100)/(F(5,6)) == F(62,1000))
ok("L06 R1: ratio 6/5", (1/F(1)) / (F(1)/F(6,5)) == F(6,5))
ok("L06 M1: beta=0.5, pi=0.03", F(100)/(F(200)*1) == F(1,2) and F(4,100)-F(1,2)*F(2,100) == F(3,100))
ok("L06 M2: beta=0.8, pi=0.048", F(200)/(F(200)*F(5,4)) == F(4,5) and F(4,100)-F(4,5)*F(-1,100) == F(48,1000))
ok("L06 M3: at gap 0.03 pi=0.005, falls 0.015", F(2,100)-F(1,2)*F(3,100) == F(5,1000))
ok("L06 misc: misconception gap -0.01 change +0.008333", abs(float(-F(5,6)*F(-1,100)) - 0.0083333) < 1e-6)
ok("L06 E1: -(5/6)(-0.01)=1/120", -F(5,6)*F(-1,100) == F(1,120))

# ---- L06 Part C grid: printed rows (out-L06 Part C) recomputed with fmt = exact rounded half-even at 6 places
def fmt6(x):
    scaled = round(x * 10**6)
    sign = "-" if scaled < 0 else ""
    whole, frac = divmod(abs(scaled), 10**6)
    return f"{sign}{whole}.{frac:06d}"
printed = {}
for line in open("/tmp/E5-v/E5-b/out-L06.txt", encoding="utf-8"):
    if line.startswith("unemployment ") and "percent change" in line:
        parts = line.split()
        printed[parts[1]] = parts[-1]
grid_ok = True
for step in range(-4, 5):
    u = F(5, 100) + F(step, 200)
    change = -(F(5, 6)) * (u - F(5, 100))
    key = fmt6(u * 100)
    if printed.get(key) != fmt6(change):
        grid_ok = False
        print("GRID MISMATCH", key, printed.get(key), fmt6(change))
ok("L06 Part C: nine printed grid rows equal -(5/6)(u-0.05) at six places", grid_ok and len(printed) == 9)
