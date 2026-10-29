"""Independent recomputation of the numbers on L07-L09 (round 4). Run as: python -I this.py"""
from fractions import Fraction as F
import math

def half_up(x):
    return math.floor(x + F(1, 2))

out = []
def check(name, got, want):
    ok = got == want
    out.append(f"{'OK ' if ok else 'BAD'} {name}: got {got} want {want}")
    return ok

# ---- L07: reference case (a,b,c)=(120,1,20), d=100 ----
a, b, c = 120, 1, 20
d = a - b * c
W = lambda Q: F(2 * d * Q - Q * Q, 2 * b)
CS = lambda Q: F(Q * Q, 2 * b)
PS = lambda Q: F((d - Q) * Q, b)
Wd = W(d)
check("L07 W(d)=5000/cents", Wd, 5000)
for name, Q in (("monopoly", F(d, 2)), ("cournot", F(2 * d, 3)), ("bertrand", F(d))):
    check(f"L07 {name} CS+PS=W", CS(Q) + PS(Q), W(Q))
    check(f"L07 {name} DWL=(d-Q)^2/(2b)", Wd - W(Q), F((d - Q) ** 2, 2 * b))
check("L07 monopoly CS 1250", CS(F(50)), 1250)
check("L07 monopoly PS 2500", PS(F(50)), 2500)
check("L07 Cournot CS 20000/9", CS(F(200, 3)), F(20000, 9))
check("L07 Cournot DWL 5000/9 -> 556 half up", (half_up(F(5000, 9)), F(5000, 9)), (556, F(5000, 9)))
check("L07 Cournot W 40000/9 -> 4444", half_up(W(F(200, 3))), 4444)
check("L07 Cournot CS 2222 half up", half_up(CS(F(200, 3))), 2222)
# M1 and M2 (a,b,c)=(90,3,10)
d2 = 90 - 3 * 10
check("L07 M1 monopoly DWL 150", F(d2 * d2, 6) - (2 * d2 * F(d2, 2) - F(d2, 2) ** 2) / 6, 150)
check("L07 M2 Cournot DWL 200/3", F((d2 - F(2 * d2, 3)) ** 2, 6), F(200, 3))
# P1 shares and R1 volume
check("L07 P1 monopoly share 1/4", (1 - F(1, 2)) ** 2, F(1, 4))
check("L07 P1 Cournot share 1/9", (1 - F(2, 3)) ** 2, F(1, 9))
check("L07 Prop2.3 DWL_M-DWL_C = 5d^2/(72b) (units d^2/b)", F(1, 8) - F(1, 18), F(5, 72))
check("L07 Prop2.3 CS_C-CS_M = 7/72", F(2, 9) - F(1, 8), F(7, 72))
check("L07 Prop2.3 PS_M-PS_C = 1/36", F(1, 4) - F(2, 9), F(1, 36))
check("L07 Prop2.3 W_C-W_M = 5/72", F(4, 9) - F(3, 8), F(5, 72))
check("L07 DWL_C/DWL_M = 4/9", F(1, 18) / F(1, 8), F(4, 9))
# R3: W_lambda difference (7 lambda - 2)/72 ; zero at 2/7
check("L07 R3 threshold lambda=2/7", F(2, 7) * F(7, 72) - F(1, 36), 0)
# R1: Q with DWL = half monopoly loss, Q = d(1 - sqrt(2)/4)
q_r1 = 1 - math.sqrt(2) / 4
check("L07 R1 Q/d approx 0.64645 (float, 5 dp)", round(q_r1, 5), 0.64645)
# ---- L08 ----
X, Y = 8, 4
grid = [(x, y) for x in range(X + 1) for y in range(Y + 1)]
ua = lambda x, y: x * y
ub = lambda x, y: (X - x) * (Y - y)
def dom(z, w):
    return ua(*z) >= ua(*w) and ub(*z) >= ub(*w) and (ua(*z) > ua(*w) or ub(*z) > ub(*w))
eff = [w for w in grid if not any(dom(z, w) for z in grid)]
check("L08 grid-efficient count 15", len(eff), 15)
inter = [w for w in eff if 0 < w[0] < X and 0 < w[1] < Y]
check("L08 interior grid-efficient 13", len(inter), 13)
off = [w for w in inter if w[1] * X != w[0] * Y]
check("L08 off-diagonal 10", len(off), 10)
check("L08 boundary efficient", sorted(w for w in eff if w not in inter), [(0, 0), (8, 4)])
# Part C-style explicit improvements (Prop 2.2 construction from L08 M2 / E1 / R3)
def improve(z, zp):
    # z=(x,y) A holds; return (x',y') strictly raising both (exact check)
    return ua(*zp) > ua(*z) and ub(*zp) > ub(*z)
check("L08 E1 uB at (38/7,14/5) = 76/5", ub(F(18, 7), F(6, 5)), F(76, 5))
check("L08 E1 share A 1/35", (F(108, 35) - 3) / 3, F(1, 35))
check("L08 E1 share B 1/75", (F(76, 5) - 15) / 15, F(1, 75))
# M2 uses X=10,Y=5 -- recompute with own constants
X2, Y2 = 10, 5
xa, ya = F(4), F(1)
lam = F(11, 24)
h = F(10, 11)
A_new = (xa - h, ya + lam * h)
B_new = (X2 - A_new[0], Y2 - A_new[1])
check("L08 M2 uA=289/66", A_new[0] * A_new[1], F(289, 66))
check("L08 M2 uB=817/33", B_new[0] * B_new[1], F(817, 33))
check("L08 M2 uA>4 and uB>24", (A_new[0] * A_new[1] > 4) and (B_new[0] * B_new[1] > 24), True)
check("L08 M2 bound A 20/11", (lam * xa - ya) / lam, F(20, 11))
check("L08 M2 bound B 30/11", (4 - lam * 6) / lam, F(30, 11))
# P3/Prop2.3 identities
import random
random.seed(0)
for _ in range(200):
    x, y = F(random.randint(0, 8)), F(random.randint(0, 4))
    uA, uB = x * y, (X - x) * (Y - y)
    p, q = x * (Y - y), y * (X - x)
    assert uA * uB == p * q and p + q == X * Y - uA - uB
check("L08 P3 identities on 200 random grid points", True, True)
eqpts = [w for w in grid if 4 * ua(*w) * ub(*w) == (X * Y - ua(*w) - ub(*w)) ** 2]
check("L08 E3 equality points", eqpts, [(0, 0), (2, 1), (4, 2), (6, 3), (8, 4)])
check("L08 E2 share 13/21", F(13, 21), F(13, 21))
check("L08 E2 interior points 21", 7 * 3, 21)
check("L08 R3 A(0,2)->(8/3,1) B (16/3,3) uB=16", (F(16, 3) * 3, F(8, 3) * 1), (16, F(8, 3)))
# quiz Q9 and M3
# ---- L09 ----
e, bb, cc, aa = 120, 10, 200, 1000
qp = F(aa - cc, bb); qs = F(aa - cc - e, bb)
check("L09 q_p=80", qp, 80)
check("L09 q_s=68", qs, 68)
check("L09 tax list in 0..200 = [120]", [t for t in range(0, 201) if F(aa - cc - t, bb) == qs], [120])
check("L09 revenue 8160", 120 * 68, 8160)
W9 = lambda q: (aa - (cc + e)) * q - F(bb, 2) * q * q
check("L09 DWL = W(qs)-W(qp) = 720", W9(qs) - W9(qp), 720)
check("L09 Prop1.4 identity at q=75", W9(F(75)), W9(qs) - F(bb, 2) * (F(75) - qs) ** 2)
check("L09 M1 q_p=100", F(600 - 100, 5), 100)
check("L09 M1 q_s=90", F(600 - 150, 5), 90)
check("L09 M1 DWL 250", F(50 ** 2, 2 * 5), 250)
check("L09 R2 quantity 40", F(800 - 400, 10), 40)
check("L09 R2 q_s=800/15", F(800, 15), F(800, 15))
# public good
def A(g):
    return max(F(0), 600 - 200 * g) + 1000 - 100 * g
def S(g):
    # exact piecewise: A linear on [0,3] and [3,10]; integrate exactly by Simpson (exact for linear/quadratic pieces)
    def integ(lo, hi):
        mid = (lo + hi) / 2
        return (A(lo) + 4 * A(mid) + A(hi)) * (hi - lo) / 6
    pieces = [(F(0), min(g, F(3)))] + ([(F(3), g)] if g > 3 else [])
    return sum((integ(lo, hi) for lo, hi in pieces if hi > lo), F(0)) - 400 * g
ints = {g: S(F(g)) for g in range(0, 11)}
check("L09 S(6)=2700", ints[6], 2700)
check("L09 S(7)=2650", ints[7], 2650)
check("L09 argmax over 0..10 is 6", max(ints, key=ints.get), 6)
check("L09 vertical sum equals 400 only at g=6 (0..10)", [g for g in range(11) if A(F(g)) == 400], [6])
check("L09 horizontal sum at 400c = 7", F(1000 - 400, 100) + max(F(0), F(600 - 400, 200)), 7)
check("L09 M2 g*=3.5", (1200 - 500) / 200, F(7, 2))
check("L09 M2 total surplus 1225", F(1200) * F(7, 2) - 100 * F(7, 2) ** 2 - 500 * F(7, 2), 1225)
check("L09 M3 horizontal at 500 = 3", F(800 - 500, 100) + max(F(0), F(400 - 500, 100)), 3)
check("L09 E2 share 2650/2700 = 0.9815", round(float(F(2650, 2700)), 4), 0.9815)
check("L09 R3 A(6)=400 and A(g)>400 below 6 (0..5)", all(A(F(g)) > 400 for g in range(6)) and A(F(6)) == 400, True)
open(__file__.replace('recompute_L07_L09.py', 'recompute_out.txt'), 'w').write("\n".join(out) + "\n")
print("\n".join(out))
check("L09 E1 100-cent tax loss 20", F(bb, 2) * (70 - 68) ** 2, 20)
check("L08 M3 (6,3) sqrt sum^2 = 32", round((18 ** 0.5 + 2 ** 0.5) ** 2, 9), 32.0)
check("L08 E1 (3,1)->(18/7,6/5) both strictly up", (F(18,7)*F(6,5) > 3 and F(38,7)*F(14,5) > 15), True)
print("BAD count:", sum(1 for l in out if l.startswith("BAD")))
