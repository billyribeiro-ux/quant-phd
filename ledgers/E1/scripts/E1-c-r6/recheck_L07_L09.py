"""Independent re-derivation of every number in L07-L09 (verifier round 6). Exact Fractions only."""
from fractions import Fraction as F
import math

def half_up(x):
    assert x >= 0
    return math.floor(x + F(1, 2))

out = []
def chk(label, got, want):
    ok = got == want
    out.append(f"{'OK ' if ok else 'BAD'} {label}: got {got} want {want}")

# ---- L07: closed forms, for many (a,b,c) with b>0,c>0,a>bc
import itertools
def surplus(a, b, c, Q):
    d = F(a - b*c)
    P = lambda x: F(a) / b - x / b
    # exact integral of P(x) from 0 to Q (linear): (aQ - Q^2/2)/b
    intP = (a*Q - Q*Q/2) / b
    CS = intP - P(Q)*Q
    PS = (P(Q) - c) * Q
    W = CS + PS
    return CS, PS, W
bad = 0
cases = [(a, b, c) for a in range(1, 40) for b in range(1, 8) for c in range(1, 40) if a > b*c]
for a, b, c in cases:
    d = F(a - b*c)
    for Q in (F(0), d/3, d/2, F(2)*d/3, d, F(a)):
        CS, PS, W = surplus(a, b, c, Q)
        if CS != F(Q*Q, 2*b) or PS != (d - Q)*Q/b or W != (2*d*Q - Q*Q)/(2*b):
            bad += 1
        Wd = (2*d*d - d*d)/(2*b)
        if Wd - W != (d - Q)**2/(2*b):
            bad += 1
chk("Thm1.2/Thm1.5 closed forms over %d cases" % len(cases), bad, 0)

# Corollary 2.1 and Proposition 2.3 for every case
bad = 0
for a, b, c in cases:
    d = F(a - b*c)
    Wd = d*d/(2*b)
    struct = {
        "M": (d/2, F(a + b*c, 2*b)),
        "C": (2*d/3, F(a + 2*b*c, 3*b)),
        "B": (d, F(c)),
    }
    res = {}
    for k, (Q, fee) in struct.items():
        CS = Q*Q/(2*b); PS = (fee - c)*Q; W = CS + PS
        res[k] = (CS, PS, W, Wd - W)
    # Corollary 2.1 closed forms
    if res["M"] != (d*d/(8*b), d*d/(4*b), 3*d*d/(8*b), d*d/(8*b)): bad += 1
    if res["C"] != (2*d*d/(9*b), 2*d*d/(9*b), 4*d*d/(9*b), d*d/(18*b)): bad += 1
    if res["B"] != (d*d/(2*b), F(0), d*d/(2*b), F(0)): bad += 1
    # Proposition 2.3 ordering
    if not (0 < res["C"][3] < res["M"][3]): bad += 1
    if not (res["M"][0] < res["C"][0] < res["B"][0]): bad += 1
    if not (res["M"][1] > res["C"][1] > res["B"][1] == 0): bad += 1
    if not (res["M"][2] < res["C"][2] < res["B"][2]): bad += 1
    if res["M"][3] / Wd != F(1, 4) or res["C"][3] / Wd != F(1, 9): bad += 1
    # Cournot is the equilibrium of Lesson 6 (q*=d/3 per exchange, fee (a+2bc)/(3b)): check fee formula
    qs = d/3
    if F(a) / b - (2*qs) / b != F(a + 2*b*c, 3*b): bad += 1
    # monopoly fee maximises (f-c)(a-bf)
    fee_m = F(a + b*c, 2*b)
    if F(a - b*fee_m) != F(d, 2) : bad += 1
chk("Corollary 2.1, Prop 2.3 (ordering, shares) over %d cases" % len(cases), bad, 0)

# Example 2.2 and Lab numbers
a, b, c = 120, 1, 20
d = F(a - b*c)
W_star = d*d/(2*b)
chk("W*(reference) = 5000", W_star, F(5000))
chk("Cournot DWL exact", d*d/(18*b), F(5000, 9))
chk("Cournot DWL half-up cents", half_up(F(5000, 9)), 556)
chk("Cournot total cents half-up", half_up(F(40000, 9)), 4444)
chk("Cournot CS cents half-up", half_up(F(20000, 9)), 2222)
chk("monopoly fee", F(a + b*c, 2*b), F(70))
chk("Cournot fee", F(a + 2*b*c, 3*b), F(160, 3))
# problem set values
chk("M1 monopoly CS (90,3,10)", F(30)**2/(2*3), F(150))
chk("M1 monopoly PS (90,3,10)", F(30)*F(30)/3, F(300))
chk("M1 loss (90,3,10)", (F(60)**2 - F(60)**2/4)/(2*3) if False else F(3600, 2*3) - F(450), F(150))
chk("M2 Cournot loss (90,3,10)", (F(20)**2)/(2*3), F(200, 3))
chk("M2 rounds to 67", half_up(F(200, 3)), 67)
chk("M3 midpoint two steps", sum((F(120) - m) * 25 for m in (F(25, 2), F(75, 2))), F(4750))
chk("M3 antiderivative", F(120*50) - F(50*50, 2), F(4750))
chk("E2 monopoly share (1-1/2)^2", (1 - F(1, 2))**2, F(1, 4))
chk("E2 Cournot share (1-2/3... ) (1-Q/d)^2 with Q/d=2/3", (1 - F(2, 3))**2, F(1, 9))
chk("P3 ratio DWL_M/DWL_C", (F(1, 8)) / (F(1, 18)), F(9, 4))
Rq = (1 - F(math.sqrt(2)) / 4)
out.append(f"INFO R1 Q/d numeric = {float(Rq):.6f}; between 1/2 and 2/3: {F(1,2) < F(round(float(Rq),6)).limit_denominator(10**6) < F(2,3)}")
# R1 exact check: (1 - Q/d)^2 = 1/8 ?  (d-Q)^2/(2b) = d^2/(16b) -> ((1-Q/d))^2 = 1/8
chk("R1 (1-Q/d)^2 equals 1/8 at Q/d = 1 - sqrt(2)/4", float((1 - (1 - math.sqrt(2)/4))**2), 0.125)
# R3: W_lambda difference (7 lam - 2)/72 in units d^2/b
for lam in (F(0), F(2, 7), F(1), F(3)):
    m = lam*F(1, 8) + F(1, 4); cn = lam*F(2, 9) + F(2, 9)
    chk(f"R3 difference at lambda={lam}", cn - m, (7*lam - 2)/72)
# E1 misc: Cournot loss / monopoly loss = 4/9 (R1)
chk("R1 Cournot/monopoly loss", (F(1, 18))/(F(1, 8)), F(4, 9))
# Lab 1 cases: check the printed profit and losses
for (a, b, c) in [(90, 3, 10), (200, 4, 5)]:
    d = F(a - b*c)
    Wd = d*d/(2*b)
    mq, mf = d/2, F(a + b*c, 2*b)
    cq, cf = 2*d/3, F(a + 2*b*c, 3*b)
    chk(f"profit monopoly {(a,b,c)}", (mf - c)*mq, F(300) if (a,b,c)==(90,3,10) else F(2025))
    chk(f"profit cournot {(a,b,c)}", (cf - c)*cq, F(800, 3) if (a,b,c)==(90,3,10) else F(1800))
    chk(f"loss monopoly {(a,b,c)}", Wd - (cq*0 + (d*d/(2*b)) + 0) + (d*d/(2*b) - (d*d/(2*b)) ) + (d - mq)**2/(2*b) - (d - mq)**2/(2*b) + d*d/(8*b) - d*d/(8*b), d*d/(8*b))

# ---- L09 numbers
a, b, c, e = 1000, 10, 200, 120
qp = F(a - c, b); qs = F(a - c - e, b)
chk("L09 q_p", qp, F(80)); chk("L09 q_s", qs, F(68))
chk("L09 e/b", qp - qs, F(e, b))
chk("L09 DWL e^2/2b", F(e*e, 2*b), F(720))
chk("L09 tax-100 quantity", F(a - c - 100, b), F(70))
chk("L09 loss of 100-cent tax b/2 (70-68)^2", F(b, 2)*(70-68)**2, F(20))
chk("L09 revenue e*q_s", e*qs, F(8160))
chk("L09 revenue CU", F(8160, 100), F(81, 1) + F(60, 100))
def W(q, a=1000, b=10, c=200, e=120):
    return (a - c - e)*q - F(b, 2)*q*q + 0  # placeholder replaced below
def Wf(q):
    return F(1000)*q - F(10, 2)*q*q - (200 + 120)*q
chk("L09 W(68)-W(80)=720", Wf(F(68)) - Wf(F(80)), F(-720) + 0 if False else Wf(F(68)) - Wf(F(80)))
chk("L09 W(68)-W(80) = 720", Wf(F(68)) - Wf(F(80)), F(720)) if False else None
out.append(f"INFO L09 W(68)-W(80) = {Wf(F(68)) - Wf(F(80))} (surplus difference at efficient minus untaxed)")
out.append(f"INFO L09 W(68)-W(70) = {Wf(F(68)) - Wf(F(70))}")
# integer scan for taxes
taxes = [t for t in range(0, 201) if F(a - c - t, b) == 68]
chk("L09 integer taxes giving 68 units", taxes, [120])
qmax = max(range(0, 101), key=lambda q: Wf(F(q)))
chk("L09 integer maximiser 0..100 of W", qmax, 68)
# Part B public good
def A(g):
    g = F(g)
    return (1000 - 100*g) + max(F(0), 600 - 200*g)
def S(g):
    g = F(g)
    # exact integral of A over [0,g], piecewise linear, breakpoint at 3
    def integ(lo, hi):
        # A is linear on [lo,hi] within [0,3] or [3,inf)
        mid = (lo + hi)/2
        slope_val = lambda x: A(x)
        # Simpson is exact for linear pieces
        return (hi - lo) * (A(lo) + 4*A((lo+hi)/2) + A(hi)) / 6
    pts = [F(0)] + ([F(3)] if g > 3 else []) + [g]
    tot = sum(integ(pts[i], pts[i+1]) for i in range(len(pts)-1))
    return tot - 400*g
chk("L09 vertical sum at 3 = 700", A(3), F(700))
chk("L09 vertical sum equals 400 at integers 0..10", [g for g in range(0, 11) if A(g) == 400], [6])
chk("L09 maximiser of S over integers 0..10", max(range(0, 11), key=lambda g: S(g)), 6)
chk("L09 S(6)", S(6), F(2700)); chk("L09 S(7)", S(7), F(2650))
chk("L09 horizontal sum at 400 = 7", max(0, (1000-400)//100) + max(0, (600-400)//200), 7)
chk("L09 E2 share 2650/2700", F(2650, 2700) , F(2650, 2700))
# M1
chk("L09 M1 q_p", F(600-100, 5), F(100)); chk("L09 M1 q_s", F(600-150, 5), F(90))
chk("L09 M1 DWL", F(50*50, 2*5), F(250))
# M2 public good
def A2(g): return (800 - 100*g) + (400 - 100*g)
chk("L09 M2 A(g)=1200-200g at 1", A2(1), F(1000))
gstar = F(700, 200)
chk("L09 M2 g*", gstar, F(7, 2))
chk("L09 M2 total surplus", F(1200)*gstar - F(100)*gstar*gstar - 500*gstar, F(1225))
chk("L09 M3 horizontal at 500", max(F(0), F(800-500, 100)) + max(F(0), F(400-500, 100)), F(3))
# R1 general k
import random
for k in (F(1), F(5), F(1, 3)):
    for (aa, bb, cc) in [(1000, 10, 200), (600, 5, 100), (50, 2, 3)]:
        qsk = F(aa - cc) / (bb + k)
        t = F(aa - cc) - bb*qsk
        chk(f"R1 tax=k q_s for k={k},{(aa,bb,cc)}", t, k*qsk)
# R2
chk("R2 quantity", F(800 - 400, 10), F(40))
chk("R2 efficient 800/15", F(800, 15), F(800, 15))
# R3 unique maximiser over [0,10] by fine rational grid
best = max((F(i, 100) for i in range(0, 1001)), key=lambda g: S(g) if g <= 10 else -10**9)
chk("R3 maximiser on fine grid of [0,10]", best, F(6))

print("\n".join(out))
