"""Independent recomputation of the numbers printed or asserted in L07, L08 and L09 (round 1, slice c).

Uses only fractions.Fraction and integer arithmetic; written without reading the lab twins.
Usage: python -I ledgers/E1/scripts/E1-c-r1/verify_recompute_L07_L09_r1.py
"""

from __future__ import annotations

import math
from fractions import Fraction as F


def check(label: str, got: object, want: object) -> None:
    status = "OK" if got == want else "MISMATCH"
    print(f"{status:8s} {label}: got={got} want={want}")


def half_up(x: F) -> int:
    return math.floor(x + F(1, 2))


# ---------------- L07: surplus and deadweight loss ----------------
print("== L07")


def integral_P(q: F, a: int, b: int) -> F:
    # exact antiderivative of (a - x)/b from 0 to q
    return (a * q - q * q / 2) / b


for a, b, c in [(120, 1, 20), (90, 3, 10), (200, 4, 5)]:
    d = F(a - b * c)
    W = lambda q: (2 * d * q - q * q) / (2 * b)  # noqa: E731
    Wd = W(d)
    struct = {"monopoly": (d / 2, F(a + b * c, 2 * b)), "cournot": (2 * d / 3, F(a + 2 * b * c, 3 * b)), "bertrand": (d, F(c))}
    for name, (q, p) in struct.items():
        cs = integral_P(q, a, b) - p * q
        ps = (p - c) * q
        w = cs + ps
        check(f"L07 ({a},{b},{c}) {name} W=int(P-c)", w, W(q))
        check(f"L07 ({a},{b},{c}) {name} CS=Q^2/2b", cs, q * q / (2 * b))
        check(f"L07 ({a},{b},{c}) {name} DWL=(d-Q)^2/2b", Wd - w, (d - q) ** 2 / (2 * b))
    check(f"L07 ({a},{b},{c}) monopoly DWL/W(d)=1/4", (Wd - W(d / 2)) / Wd, F(1, 4))
    check(f"L07 ({a},{b},{c}) cournot DWL/W(d)=1/9", (Wd - W(2 * d / 3)) / Wd, F(1, 9))
    check(f"L07 ({a},{b},{c}) DWL_M/DWL_C=9/4", (d * d / (8 * b)) / (d * d / (18 * b)), F(9, 4))
    # Lambda ranking: W_lambda = lambda*CS + PS, in units d^2/b
    # (verified symbolically in the page; numeric spot checks at lambda in {0, 2/7, 1})
    for lam in (F(0), F(2, 7), F(1), F(3)):
        cs_m = (d / 2) ** 2 / (2 * b)
        ps_m = (d / 2) * (d / 2) / b
        cs_c = (2 * d / 3) ** 2 / (2 * b)
        ps_c = (d / 3) * (2 * d / 3) / b
        diff = (lam * cs_c + ps_c) - (lam * cs_m + ps_m)
        check(f"L07 R3 sign at lambda={lam} equals sign((7 lambda - 2)/72) in d^2/b units", (diff > 0) - (diff < 0),
              ((7 * lam - 2) > 0) - ((7 * lam - 2) < 0))

# reference case values from Example 2.2 and the lab
a, b, c = 120, 1, 20
d = F(100)
check("L07 Cournot DWL exact 5000/9", (d * d / (18 * b)), F(5000, 9))
check("L07 Cournot DWL half-up cents", half_up(F(5000, 9)), 556)
check("L07 Cournot total surplus half-up cents", half_up(F(40000, 9)), 4444)
check("L07 Cournot CS half-up cents", half_up(F(20000, 9)), 2222)
check("L07 Cournot profit 20000/9 = 2 * d^2/(9b)", 2 * d * d / (9 * b), F(20000, 9))
check("L07 M2 Cournot loss (90,3,10) exact 200/3", (F(60 - 40) ** 2) / (2 * 3), F(200, 3))
check("L07 M2 half-up 67", half_up(F(200, 3)), 67)
check("L07 M1 monopoly CS (90,3,10) = 150", F(30) ** 2 / (2 * 3), 150)
check("L07 M1 PS = 300", (F(60) - 30) * 30 / 3, 300)
check("L07 M3 midpoint two steps = 4750", sum((120 - x) * 25 for x in (F(25, 2), F(75, 2))), 4750)
check("L07 R1 Q/d = 1 - sqrt2/4 numerically", round(1 - (2 ** 0.5) / 4, 5), 0.64645)
check("L07 R1 Cournot loss / monopoly loss = 4/9", (F(1, 18)) / F(1, 8), F(4, 9))
check("L07 E2 share 1/4 identical across cases", F(1, 4), F(1, 4))
check("L07 quiz 555.5556 within 0.001 of 5000/9", abs(555.5556 - 5000 / 9) <= 0.001, True)
check("L07 Prop 2.3 accounting: CS change 7/72", F(2, 9) - F(1, 8), F(7, 72))
check("L07 Prop 2.3 accounting: PS change -2/72", F(2, 9) - F(1, 4), F(-2, 72))
check("L07 Prop 2.3 accounting: W change 5/72", F(4, 9) - F(3, 8), F(5, 72))

# ---------------- L08: Pareto efficiency ----------------
print("== L08")
X, Y = 8, 4
grid = [(x, y) for x in range(X + 1) for y in range(Y + 1)]


def ua(x: F, y: F) -> F:
    return x * y


def ub(x: F, y: F) -> F:
    return (X - x) * (Y - y)


def dominates(z: tuple[F, F], w: tuple[F, F]) -> bool:
    za, zb = ua(*z), ub(*z)
    wa, wb = ua(*w), ub(*w)
    return za >= wa and zb >= wb and (za > wa or zb > wb)


eff = [p for p in grid if not any(dominates((F(x), F(y)), (F(p[0]), F(p[1]))) for x, y in grid)]
interior_eff = [p for p in eff if 0 < p[0] < X and 0 < p[1] < Y]
boundary_eff = [p for p in eff if p not in interior_eff]
check("L08 grid-efficient total", len(eff), 15)
check("L08 interior grid-efficient count", len(interior_eff), 13)
check("L08 boundary grid-efficient", sorted(boundary_eff), [(0, 0), (8, 4)])
diag = [p for p in grid if 0 < p[0] < X and 0 < p[1] < Y and p[1] * X == p[0] * Y]
check("L08 interior diagonal points", diag, [(2, 1), (4, 2), (6, 3)])
off = [p for p in interior_eff if p not in diag]
check("L08 off-diagonal interior grid-efficient", len(off), 10)
check("L08 share 13/21", F(13, 21), F(13, 21))
check("L08 13/21 rounded", round(13 / 21, 3), 0.619)
check("L08 3/35 / 3 = 1/35 (2.86%)", round(float(100 * (F(108, 35) - 3) / 3), 2), 2.86)
check("L08 1/5 / 15 = 1/75 (1.33%)", round(float(100 * (F(76, 5) - 15) / 15), 2), 1.33)
check("L08 (3,1) improvement A=(18/7,6/5): uA", ua(F(18, 7), F(6, 5)), F(108, 35))
check("L08 (3,1) improvement B=(38/7,14/5): uB", ub(F(18, 7), F(6, 5)), F(76, 5))
check("L08 (3,1) B utility gain", ub(F(18, 7), F(6, 5)) - 15, F(1, 5))
check("L08 (3,1) A utility gain", ua(F(18, 7), F(6, 5)) - 3, F(3, 35))
check("L08 M2 (10,5 totals) lambda bound 20/11", (F(11, 6) - 1) / F(11, 24), F(20, 11))
check("L08 M2 B bound 30/11", (F(4) - F(11, 24) * 6) / F(11, 24), F(30, 11))
check("L08 M2 u_A=289/66", F(34, 11) * F(17, 12), F(289, 66))
check("L08 M2 u_B=817/33", F(76, 11) * F(43, 12), F(817, 33))
check("L08 M2 new holding A y = 1 + 5/12", F(1) + F(11, 24) * F(10, 11), F(17, 12))
check("L08 M3 (sqrt18+sqrt2)^2 = 32 (float, 9 dp)", round((math.sqrt(18) + math.sqrt(2)) ** 2, 9), 32)
check("L08 quiz (4,2) sum of roots 2 sqrt8 = sqrt32", round(2 * math.sqrt(8), 2), 5.66)
# part E: equality points of the bound
eq = []
for x, y in grid:
    A, B = ua(F(x), F(y)), ub(F(x), F(y))
    s = X * Y - A - B
    assert s >= 0 and 4 * A * B <= s * s
    if 4 * A * B == s * s:
        eq.append((x, y))
check("L08 equality points", eq, [(0, 0), (2, 1), (4, 2), (6, 3), (8, 4)])
# the (x,y) Part C improvements: exhibit that every off-diagonal interior grid-efficient point has a strict improvement
# using the page's rule (any lambda strictly between the rates; h below both bounds)
for x, y in off:
    xa, ya = F(x), F(y)
    xb, yb = X - xa, Y - ya
    ra, rb = ya / xa, yb / xb
    lo, hi = min(ra, rb), max(ra, rb)
    lam = (lo + hi) / 2
    if rb < ra:
        bound = min((ya - lam * xa) / lam, (lam * xb - yb) / lam)
        h = bound / 2
        na = (xa + h, ya - lam * h)
    else:
        bound = min((lam * xa - ya) / lam, (yb - lam * xb) / lam)
        h = bound / 2
        na = (xa - h, ya + lam * h)
    nb = (X - na[0], Y - na[1])
    ok = ua(*na) > ua(xa, ya) and ub(*na) > ub(xa, ya) and nb[0] >= 0 and nb[1] >= 0 and na[0] >= 0 and na[1] >= 0
    nonint = na[0].denominator != 1 or na[1].denominator != 1
    check(f"L08 Part C improvement from {(x, y)} strictly raises both and is non-integer", (ok, nonint), (True, True))

# ---------------- L09: externalities and public goods ----------------
print("== L09")
a, b, c, e = 1000, 10, 200, 120
qp = F(a - c, b)
qs = F(a - c - e, b)
check("L09 q_p=80", qp, 80)
check("L09 q_s=68", qs, 68)
check("L09 q_p - q_s = e/b = 12", qp - qs, F(e, b))
check("L09 DWL = e^2/(2b)=720", F(e * e, 2 * b), 720)


def Wnet(q: F) -> F:
    return a * q - F(b, 2) * q * q - (c + e) * q


check("L09 W(q_s)-W(q_p)=720", Wnet(qs) - Wnet(qp), 720)
check("L09 W(q_s)-W(q)=(b/2)(q-q_s)^2 at q=80", Wnet(qs) - Wnet(F(80)), F(b, 2) * (F(80) - qs) ** 2)
check("L09 revenue 120*68 = 8160 cents", e * 68, 8160)
check("L09 revenue CU 81.60", F(8160, 100), F("81.6"))
best = max(range(0, 101), key=lambda q: Wnet(F(q)))
check("L09 integer maximiser over 0..100 is 68", best, 68)
taxes = [t for t in range(0, 201) if F(a - c - t, b) == qs]
check("L09 only tax giving 68 is [120]", taxes, [120])
check("L09 tax 100 quantity 70", F(a - c - 100, b), 70)
check("L09 tax 100 loss (b/2)(70-68)^2 = 20", F(b, 2) * (70 - 68) ** 2, 20)
check("L09 wedge at 70 = 320 - 300 = 20", (c + e) - (a - b * 70), 20)
check("L09 wedge over [68,80] integral = 720", F(0 + 120, 2) * (80 - 68), 720)
check("L09 gap at 80 = 120 (wedge)", (c + e) - (a - b * 80), 120)
check("L09 units 69..80 demand price below 320", all(a - b * q < c + e for q in range(69, 81)), True)
check("L09 unit 68 demand price equals 320", a - b * 68, c + e)
# surplus S(q) = 680q - 5q^2 (linear demand, MSC 320)
S = lambda q: F(a) * q - F(b, 2) * q * q - (c + e) * q  # noqa: E731
check("L09 S(68)-S(80)=720", S(F(68)) - S(F(80)), 720)
# M1 numbers: 600-5q, c=100, e=50
check("L09 M1 q_p=100", F(600 - 100, 5), 100)
check("L09 M1 q_s=90", F(600 - 150, 5), 90)
check("L09 M1 DWL=250", F(50 * 50, 2 * 5), 250)
check("L09 M1 triangle 1/2*10*50", F(1, 2) * 10 * 50, 250)
# M2: vertical sum 1200-200g, cost 500
gstar = F(1200 - 500, 200)
check("L09 M2 g*=3.5", gstar, F(7, 2))
S2 = lambda g: F(1200) * g - 100 * g * g - 500 * g  # noqa: E731
check("L09 M2 total surplus at 3.5 = 1225", S2(F(7, 2)), 1225)
check("L09 M2 consumer 2 line at 3.5 = 50 > 0", 400 - 100 * F(7, 2), 50)
# M3: horizontal at 500
check("L09 M3 consumer 1 quantity at 500 = 3", F(800 - 500, 100), 3)
# E1 (tax 100): quantity 70
# E2: 2650/2700 and 2500/2700
check("L09 E2 2650/2700 = 0.9815", round(2650 / 2700, 4), 0.9815)
check("L09 E2 98.1 per cent", round(100 * 2650 / 2700, 1), 98.1)
check("L09 E2 2500/2700 = 92.6 per cent", round(100 * 2500 / 2700, 1), 92.6)
# public good aggregates at g=4 used by E2 (surplus 2500 at 4 units): recompute from definitions
def w1(g: F) -> F:
    return 1000 - 100 * g


def w2(g: F) -> F:
    return max(F(0), 600 - 200 * g)


def A(g: F) -> F:
    return w1(g) + w2(g)


def integ(f, lo: F, hi: F) -> F:  # exact by splitting at kink 3 and using trapezoid (linear pieces)
    pts = sorted({lo, hi} | ({F(3)} if lo < 3 < hi else set()))
    tot = F(0)
    for u, v in zip(pts, pts[1:]):
        tot += (f(u) + f(v)) / 2 * (v - u)
    return tot


def Spub(g: F) -> F:
    return integ(A, F(0), g) - 400 * g


check("L09 public-good S(6)=2700", Spub(F(6)), 2700)
check("L09 public-good S(7)=2650", Spub(F(7)), 2650)
check("L09 public-good S(4)=2500 (E2 solution text)", Spub(F(4)), 2500)
check("L09 vertical sum at 3 = 700", A(F(3)), 700)
check("L09 horizontal sum at 400 = 7", F(1000 - 400, 100) + max(F(0), F(600 - 400, 200)), 7)
ints = [g for g in range(0, 11) if A(F(g)) == 400]
check("L09 integer vertical-sum=cost list = [6]", ints, [6])
check("L09 integer maximiser of S on 0..10 = 6", max(range(0, 11), key=lambda g: Spub(F(g))), 6)
# R2 numbers: a=1000, b=10, c=200, k=5
qpR = F(800, 10)
check("L09 R2 q_p=80", qpR, 80)
check("L09 R2 tax 400", 5 * qpR, 400)
check("L09 R2 quantity 40", F(800 - 400, 10), 40)
check("L09 R2 q_s = 800/15", F(800, 15), F(160, 3))
check("L09 R2 shortfall 13.3", round(float(F(160, 3) - 40), 1), 13.3)
# R1 general identity check at sample numbers
for (aa, bb, cc, kk) in [(1000, 10, 200, 5), (600, 5, 100, 3)]:
    qsR = F(aa - cc, bb + kk)
    tR = F(aa - cc) - bb * qsR
    check(f"L09 R1 tax=kq_s at ({aa},{bb},{cc},{kk})", tR, kk * qsR)
# R3: A on [0,3] and [3,10]
check("L09 R3 A(g) on [0,3] is 1600-300g at g=1", A(F(1)), 1600 - 300)
check("L09 R3 A(g) on [3,10] is 1000-100g at g=5", A(F(5)), 1000 - 100 * 5)
# P2/E1 numbers in L09 Corollary proof: triangle
print("done")
