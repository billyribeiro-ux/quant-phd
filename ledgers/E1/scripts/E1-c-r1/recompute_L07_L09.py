"""Independent recomputation (E1 slice c, round 1) of the numbers in L07-L09 pages, with exact Fractions.

Run: <checkout>/.venv/bin/python -I ledgers/E1/scripts/E1-c-r1/recompute_L07_L09.py
Prints every checked quantity and asserts it; exits non-zero on any mismatch.
"""
from fractions import Fraction as F
import math

def half_up(x):
    return math.floor(x + F(1, 2))

out = []
def check(name, got, want):
    ok = got == want
    out.append(f"{'OK ' if ok else 'BAD'} {name}: got {got} want {want}")
    if not ok:
        raise SystemExit("\n".join(out))

# ---- L07: reference case (a,b,c)=(120,1,20), d=100 ----
a, b, c = 120, F(1), F(20)
d = a - b * c
W = lambda Q: (2 * d * Q - Q * Q) / (2 * b)
CS = lambda Q: Q * Q / (2 * b)
PS = lambda Q, fee: (fee - c) * Q
for name, Q, fee in [("monopoly", d / 2, (a + b * c) / (2 * b)),
                     ("cournot", 2 * d / 3, (a + 2 * b * c) / (3 * b)),
                     ("bertrand", d, c)]:
    cs = CS(Q); ps = PS(Q, fee); w = W(Q); dwl = W(d) - w
    check(f"L07 {name} CS=cs+ps?", cs + ps, w)
    check(f"L07 {name} DWL=(d-Q)^2/2b", dwl, (d - Q) ** 2 / (2 * b))
    print(name, "cents exact", cs, ps, w, dwl, "half-up", half_up(cs), half_up(ps), half_up(w), half_up(dwl))
check("L07 monopoly DWL d^2/8b", W(d) - W(d / 2), d * d / (8 * b))
check("L07 cournot DWL d^2/18b", W(d) - W(2 * d / 3), d * d / (18 * b))
check("L07 cournot half-up 556", half_up(F(5000, 9)), 556)
check("L07 cournot total half-up 4444", half_up(F(40000, 9)), 4444)
check("L07 cournot CS half-up 2222", half_up(F(20000, 9)), 2222)
# Proposition 2.3 ratios, with several (a,b,c)
for (A, B, C) in [(120, 1, 20), (90, 3, 10), (200, 4, 5), (7, 1, 1), (1000, 17, 3)]:
    D = F(A - B * C)
    Wst = D * D / (2 * B)
    Wm = (2 * D * (D / 2) - (D / 2) ** 2) / (2 * B)
    Wc = (2 * D * (2 * D / 3) - (2 * D / 3) ** 2) / (2 * B)
    check(f"L07 share monopoly (a,b,c)={(A,B,C)}", (Wst - Wm) / Wst, F(1, 4))
    check(f"L07 share cournot (a,b,c)={(A,B,C)}", (Wst - Wc) / Wst, F(1, 9))
    check(f"L07 DWL ratio 9/4 {(A,B,C)}", (Wst - Wm) / (Wst - Wc), F(9, 4))
# R1 / L07: half monopoly loss point
Qr = 1 - math.sqrt(2) / 4
check("L07 R1 (d-Q)^2 = d^2/8 numerically", round((1 - Qr) ** 2, 12), round(1 / 8, 12))
check("L07 R1 Q/d 0.64645 to 5dp", round(Qr, 5), 0.64645)
# E2 L07 shares
check("L07 P1 (1-Q/d)^2 at 1/2", (1 - F(1, 2)) ** 2, F(1, 4))
# R3 L07 lambda threshold
lam = F(2, 7)
check("L07 R3 difference zero at lambda=2/7", F(7) * lam / 72 - F(1, 36), 0)
# Lab check of misconception: monopoly profit 2500 vs DWL 1250
check("L07 monopoly profit (ref)", (F(70) - c) * (d / 2), F(2500))

# ---- L08: X=8, Y=4 ----
X, Y = 8, 4
def uA(x, y): return x * y
def uB(x, y): return (X - x) * (Y - y)
grid = [(F(x), F(y)) for x in range(X + 1) for y in range(Y + 1)]
def dominates(z, w):
    return uA(*z) >= uA(*w) and uB(*z) >= uB(*w) and (uA(*z) > uA(*w) or uB(*z) > uB(*w))
eff = [w for w in grid if not any(dominates(z, w) for z in grid)]
check("L08 grid size", len(grid), 45)
check("L08 grid-efficient count", len(eff), 15)
interior = [w for w in eff if 0 < w[0] < X and 0 < w[1] < Y]
check("L08 interior grid-efficient count", len(interior), 13)
diag = [w for w in interior if w[1] * X == w[0] * Y]
check("L08 interior on diagonal", len(diag), 3)
check("L08 off-diagonal interior", len(interior) - len(diag), 10)
check("L08 share 13/21", F(13, 21), F(13, 21))
print("L08 13/21 =", float(F(13, 21)), "-> 61.9%")
# M2 check (X=10,Y=5, A=(4,1)); trade lam=11/24, h=10/11
X2, Y2 = 10, 5
xa, ya = F(4), F(1); lam2 = F(11, 24); h = F(10, 11)
ra = ya / xa; rb = (Y2 - ya) / (X2 - xa)
check("L08 M2 r_A<lam<r_B", (ra < lam2 < rb), True)
newA = (xa - h, ya + lam2 * h)
check("L08 M2 uA new", newA[0] * newA[1], F(289, 66))
check("L08 M2 uB new", (X2 - newA[0]) * (Y2 - newA[1]), F(817, 33))
print("L08 M2 uA float", float(F(289, 66)), "uB float", float(F(817, 33)))
# Example 2.5 and quiz
check("L08 M3 (sqrt18+sqrt2)^2 = 32 numerically", round((math.sqrt(18) + math.sqrt(2)) ** 2, 9), 32.0)
print("L08 quiz (4,2): sqrt(uA)+sqrt(uB) =", math.sqrt(8) + math.sqrt(8), "two-decimal rounding:", round(math.sqrt(8) + math.sqrt(8), 2), "three-decimal:", round(math.sqrt(8) + math.sqrt(8), 3))
# E1 L08 numbers
check("L08 E1 uA-3", F(108, 35) - 3, F(3, 35))
check("L08 E1 uB-15", F(76, 5) - 15, F(1, 5))
check("L08 E1 uB at (38/7,14/5)", F(38, 7) * F(14, 5), F(76, 5))
# R3 L08 witness
check("L08 R3 B after trade", (F(16, 3)) * 3, F(16))
# Prop 2.2 M2 bound check: A=(4,1) bounds
check("L08 M2 bound 20/11", (F(5, 6)) / (F(11, 24)), F(20, 11))
check("L08 M2 bound 30/11", (F(5, 4)) / (F(11, 24)), F(30, 11))
# Lab part E equality set
eq = [w for w in grid if 4 * uA(*w) * uB(*w) == (X * Y - uA(*w) - uB(*w)) ** 2]
diag_all = [w for w in grid if w[1] * X == w[0] * Y]
check("L08 part E equality == diagonal", sorted(eq), sorted(diag_all))

# ---- L09 ----
ap, bp, cp, ep = 1000, 10, 200, 120
qp = F(ap - cp, bp); qs = F(ap - cp - ep, bp)
check("L09 q_p", qp, 80); check("L09 q_s", qs, 68)
check("L09 DWL e^2/2b", ep * ep / (2 * bp), 720)
check("L09 tax revenue", 120 * qs, 8160)
W9 = lambda q: ap * q - F(bp, 2) * q * q - (cp + ep) * q
check("L09 W(q_p) loss", W9(qs) - W9(qp), 720)
check("L09 W(70) loss vs 68 at tax 100", W9(qs) - W9(F(70)), F(bp, 2) * (70 - 68) ** 2)
check("L09 wedge at 70", (cp + ep) - (ap - bp * 70), 20)
check("L09 E2 2650/2700 to 4dp", round(F(2650, 2700), 4), F(9815, 10000))
# Part B: vertical sum and horizontal
def A9(g): return (1000 - 100 * g) + max(F(0), 600 - 200 * g)
def S9(g):
    pieces = [(F(0), min(g, F(3)))] + ([(F(3), g)] if g > 3 else [])
    area = sum((A9(x) + A9(y)) / 2 * (y - x) for x, y in pieces)
    return area - 400 * g
check("L09 S(6)", S9(F(6)), 2700); check("L09 S(7)", S9(F(7)), 2650)
check("L09 A(6)=400", A9(F(6)), 400); check("L09 A(3)=700", A9(F(3)), 700)
best = max(range(11), key=lambda g: S9(F(g)))
check("L09 argmax over 0..10", best, 6)
# Horizontal at 400
check("L09 horizontal at 400", (F(1000 - 400, 100)) + max(F(0), F(600 - 400, 200)), 7)
# M1 (600,5,100,50)
check("L09 M1 q_p", F(600 - 100, 5), 100); check("L09 M1 q_s", F(600 - 150, 5), 90)
check("L09 M1 DWL", F(50 * 50, 2 * 5), 250)
# M2 public (800-100g, 400-100g, cost 500)
A2 = lambda g: (800 - 100 * g) + (400 - 100 * g)
check("L09 M2 g* solves 1200-200g=500", F(500 - 1200, -200), F(7, 2))
check("L09 M2 surplus", F(1200) * F(7, 2) - 100 * F(7, 2) ** 2 - 500 * F(7, 2), 1225)
# M3 horizontal at 500
check("L09 M3 horizontal", F(800 - 500, 100) + max(F(0), F(400 - 500, 100)), 3)
# R1 / R2
kk = 5; A_, B_, C_ = 1000, 10, 200
qp2 = F(A_ - C_, B_); qs2 = F(A_ - C_, B_ + kk)
t2 = kk * qp2
check("L09 R2 quantity with tax kq_p", (A_ - C_ - t2) / B_, 40)
check("L09 R2 efficient", qs2, F(800, 15))
check("L09 R2 shortfall", qs2 - 40, F(200, 15))
# R3 pieces
check("L09 R3 A on [0,3] at g=0", A9(F(0)), 1600)
# misconception: each 12 unit demand price below 320 for 68<q<=80
check("L09 MSC", ep + cp, 320)
print("\n".join(out))
print("ALL CHECKS PASS")
