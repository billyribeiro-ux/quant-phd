"""Independent exact recomputation of the numbers printed on E1 L07, L08 and L09 (round 3 verifier)."""
from fractions import Fraction as F
import math

def half_up(x):
    return math.floor(x + F(1, 2))

out = []
# L07: reference case (a,b,c)=(120,1,20), d=100, b=1
a, b, c = 120, 1, 20
d = F(a - b * c)
W_d = d * d / (2 * b)
for name, Q, fee in [("monopoly", d / 2, F(a + b * c, 2 * b)), ("cournot", 2 * d / 3, F(a + 2 * b * c, 3 * b)), ("bertrand", d, F(c))]:
    CS = Q * Q / (2 * b)
    PS = (fee - c) * Q
    W = CS + PS
    DWL = W_d - W
    assert DWL == (d - Q) ** 2 / (2 * b), name
    out.append((name, str(Q), str(fee), str(CS), half_up(CS), str(PS), str(W), half_up(W), str(DWL), half_up(DWL)))
for row in out:
    print("L07", row)
assert W_d == 5000 and F(5000, 9) > F(5555, 10) and half_up(F(5000, 9)) == 556
# shares and ordering (Proposition 2.3) for three (a,b,c)
for a, b, c in [(120, 1, 20), (90, 3, 10), (200, 4, 5)]:
    d = F(a - b * c)
    Wd = d * d / (2 * b)
    dm = (d - d / 2) ** 2 / (2 * b)
    dc = (d - 2 * d / 3) ** 2 / (2 * b)
    assert dm / Wd == F(1, 4) and dc / Wd == F(1, 9)
    assert dm - dc == F(5, 72) * d * d / b
    assert dc > 0 and dm > dc
    print("L07 shares ok", a, b, c, dm / Wd, dc / Wd)
# monopoly loss ratio 9/4 (P3) and half-loss volume (R1)
assert F(d * d, 8) / F(d * d, 18) == F(9, 4)
q_half = 1 - math.sqrt(2) / 4
print("L07 R1 Q/d", round(q_half, 5), "between 1/2 and 2/3:", 0.5 < q_half < 2 / 3)
# L07 R3: W_lambda difference (units d^2/b)
for lam in [F(2, 7), F(1), F(0)]:
    diff = lam * (F(2, 9) - F(1, 8)) + (F(2, 9) - F(1, 4))
    assert diff == (7 * lam - 2) / 72

# L08: X=8, Y=4
X, Y = 8, 4
def ua(x, y): return x * y
def ub(x, y): return (X - x) * (Y - y)
grid = [(x, y) for x in range(9) for y in range(5)]
def dominates(z, w):
    return ua(*z) >= ua(*w) and ub(*z) >= ub(*w) and (ua(*z) > ua(*w) or ub(*z) > ub(*w))
eff = [p for p in grid if not any(dominates(q, p) for q in grid)]
interior_eff = [p for p in eff if 0 < p[0] < X and 0 < p[1] < Y]
print("L08 grid", len(grid), "grid-efficient", len(eff), "interior", len(interior_eff),
      "off-diagonal", len([p for p in interior_eff if p[1] * X != p[0] * Y]))
assert len(grid) == 45 and len(eff) == 15 and len(interior_eff) == 13
# L08 E1 percentages
gA = F(108, 35) - 3
gB = F(76, 5) - 15
print("L08 E1 gains", gA, float(gA), gB, float(gB), "shares", float(gA / 3 * 100), float(gB / 15 * 100))
assert gA == F(3, 35) and gB == F(1, 5) and gA / 3 == F(1, 35) and gB / 15 == F(1, 75)
# L08 M2 explicit improvement
xA, yA = F(4), F(1)
lam, h = F(11, 24), F(10, 11)
A_new = (xA - h, yA + lam * h)
B_new = (8 - 0 - 0, 0)  # placeholder not used
B_new = (F(10) - A_new[0], F(5) - A_new[1])
assert A_new == (F(34, 11), F(17, 12)) and B_new == (F(76, 11), F(43, 12))
assert A_new[0] * A_new[1] == F(289, 66) > 4 and B_new[0] * B_new[1] == F(817, 33) > 24
# L08 R3 boundary example
assert F(8, 3) * 1 == F(8, 3) and (F(16, 3)) * 3 == 16
# L08 E2 share
print("L08 E2 share", float(F(13, 21)))
assert round(float(F(13, 21)) * 100, 1) == 61.9
# L08 quiz: sqrt(uA)+sqrt(uB) at (4,2) squared equals 32
assert ua(4, 2) == 8 and ub(4, 2) == 8

# L09: a=1000, b=10, c=200, e=120 (Lab 1 inputs)
a, b, c, e = 1000, 10, 200, 120
qp = F(a - c, b); qs = F(a - c - e, b)
print("L09 qp", qp, "qs", qs, "gap", qp - qs, "DWL", F(e * e, 2 * b))
assert qp == 80 and qs == 68 and qp - qs == F(e, b) and F(e * e, 2 * b) == 720
taxes = [t for t in range(0, 201) if F(a - c - t, b) == qs]
print("L09 taxes giving 68:", taxes)
assert taxes == [120]
assert F(a - c - 100, b) == 70 and F(b, 2) * (70 - 68) ** 2 == 20
# wedge check: MSC 320 at q; demand price at q = 1000-10q
wedge_area = (F(320 - (1000 - 10 * 68)) + F(320 - (1000 - 10 * 80))) / 2 * (80 - 68)
print("L09 wedge area", wedge_area)
assert wedge_area == 720
# M1: a=600,b=5,c=100,e=50
assert F(600 - 100, 5) == 100 and F(600 - 150, 5) == 90 and F(50 * 50, 2 * 5) == 250
# M2 public good: A(g)=1200-200g, cost 500 -> g=3.5; total surplus 1225
g = F(7, 2)
S = (1200 * g - 100 * g * g) - 500 * g
assert S == 1225
# Lab 1 public good: S(6)=2700, S(7)=2650, vertical sum at 6 equals 400
def A(g):
    w2 = max(F(0), 600 - 200 * g)
    return (1000 - 100 * g) + w2
def integ(lo, hi, f, n=2000):
    # exact piecewise-linear: split at the kink 3
    pts = [lo, hi] if hi <= 3 else [lo, F(3), hi] if lo < 3 else [lo, hi]
    tot = F(0)
    for u, v in zip(pts, pts[1:]):
        tot += (f(u) + f(v)) / 2 * (v - u)
    return tot
def Sfun(g):
    return integ(F(0), g, A) - 400 * g
print("L09 S(6)", Sfun(F(6)), "S(7)", Sfun(F(7)), "A(6)", A(F(6)), "A(3)", A(F(3)))
assert Sfun(F(6)) == 2700 and Sfun(F(7)) == 2650 and A(F(6)) == 400
assert [g for g in range(11) if A(F(g)) == 400] == [6]
assert max(range(11), key=lambda g: Sfun(F(g))) == 6
assert F(2650, 2700) > F(98, 100) and round(float(F(2650, 2700)) * 100, 1) == 98.1
# L09 R2: a=1000,b=10,c=200,k=5
qp2 = F(800, 10); t = 5 * qp2; q_after = (800 - t) / 10; qs2 = F(800, 15)
print("L09 R2 qp", qp2, "t", t, "after", q_after, "qs", float(qs2), "miss", float(qs2 - q_after))
assert q_after == 40 and abs(float(qs2 - q_after) - 13.3) < 0.05
# L09 R1 identity: t = k*qs for general a,b,c,k (spot check)
for (aa, bb, cc, kk) in [(1000, 10, 200, 5), (600, 5, 100, 3), (90, 3, 10, 2)]:
    qsx = F(aa - cc, bb + kk); tx = F(aa - cc) - bb * qsx
    assert tx == kk * qsx, (aa, bb, cc, kk)
print("ALL ASSERTIONS PASSED")
