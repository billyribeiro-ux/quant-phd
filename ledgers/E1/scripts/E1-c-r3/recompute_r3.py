"""Round-3 independent exact recomputation for E1 L07-L09 (no import of the lab twins or the page)."""
from fractions import Fraction as F
from itertools import product

fails = []


def check(name, cond):
    if not cond:
        fails.append(name)
    return cond


def trap_exact(f, lo, hi, n=7):
    """Exact trapezoid over n pieces (exact for linear f)."""
    h = (hi - lo) / n
    s = F(0)
    for i in range(n):
        x0, x1 = lo + i * h, lo + (i + 1) * h
        s += (f(x0) + f(x1)) / 2 * h
    return s


# ---------- L07 ----------
n07 = 0
for b, c in product(range(1, 7), range(1, 12)):
    for a in range(b * c + 1, b * c + 60):
        d = F(a - b * c)
        P = lambda x: (a - x) / F(b)
        W_comp = trap_exact(lambda x: P(x) - c, F(0), d)
        check("L07 W(d)=d^2/2b", W_comp == d * d / (2 * b))
        vols = {"mon": d / 2, "cou": 2 * d / 3, "bert": d}
        out = {}
        for k, Q in vols.items():
            CS = trap_exact(P, F(0), Q) - (P(Q)) * Q  # CS = int P - p Q with p = P(Q)
            fee = P(Q)
            PS = (fee - c) * Q
            W = trap_exact(lambda x: P(x) - c, F(0), Q)
            DWL = W_comp - W
            check(f"L07 CS {k}", CS == Q * Q / (2 * b))
            check(f"L07 PS {k}", PS == (d - Q) * Q / b)
            check(f"L07 W {k}", W == (2 * d * Q - Q * Q) / (2 * b))
            check(f"L07 DWL {k}", DWL == (d - Q) ** 2 / (2 * b))
            out[k] = (CS, PS, W, DWL)
        # Corollary 2.1 values
        check("L07 cor mon", out["mon"] == (d * d / (8 * b), d * d / (4 * b), 3 * d * d / (8 * b), d * d / (8 * b)))
        check("L07 cor cou", out["cou"] == (2 * d * d / (9 * b), 2 * d * d / (9 * b), 4 * d * d / (9 * b), d * d / (18 * b)))
        check("L07 cor bert", out["bert"] == (d * d / (2 * b), F(0), d * d / (2 * b), F(0)))
        # Prop 2.3 orderings and shares
        check("L07 P2.3 DWL order", 0 < out["cou"][3] < out["mon"][3] and out["bert"][3] == 0)
        check("L07 P2.3 CS order", out["mon"][0] < out["cou"][0] < out["bert"][0])
        check("L07 P2.3 PS order", out["mon"][1] > out["cou"][1] > out["bert"][1] == 0)
        check("L07 P2.3 W order", out["mon"][2] < out["cou"][2] < out["bert"][2])
        check("L07 shares", out["mon"][3] / (d * d / (2 * b)) == F(1, 4) and out["cou"][3] / (d * d / (2 * b)) == F(1, 9))
        # monopoly fee maximises (f-c)(a-bf) and Cournot fee maximises profit given rival's output
        fm = F(a + b * c, 2 * b)
        pi = lambda f: (f - c) * max(F(0), a - b * f)
        for dt in (F(1, 7), F(-1, 7), F(1, 3), F(-1, 3)):
            check("L07 monopoly fee optimal", pi(fm) >= pi(fm + dt))
        n07 += 1
print("L07 triples checked:", n07)

# Example 2.2, Lab-printed reference numbers
a, b, c = 120, 1, 20
d = F(a - b * c)
check("L07 ex2.2 d", d == 100)
check("L07 ex2.2 Cournot CS 20000/9", F(200, 3) ** 2 / (2 * b) == F(20000, 9))
check("L07 ex2.2 round half up 5000/9", int(F(5000, 9) + F(1, 2)) == 556)
check("L07 ex2.2 round 40000/9", int(F(40000, 9) + F(1, 2)) == 4444)
check("L07 ex2.2 round 20000/9", int(F(20000, 9) + F(1, 2)) == 2222)
print("L07 Example 2.2 CS/PS/W/DWL mon:", (F(50) ** 2 / 2, (F(70) - c) * 50, F(3750), F(1250)))
# Part C triples
for (a, b, c), (ml, cl, pm, pc) in {(120, 1, 20): (1250, F(5000, 9), 2500, F(20000, 9)),
                                    (90, 3, 10): (150, F(200, 3), 300, F(800, 3)),
                                    (200, 4, 5): (F(2025, 2), 450, 2025, 1800)}.items():
    d = F(a - b * c)
    check(f"L07 partC mon loss {a}", d * d / (8 * b) == ml)
    check(f"L07 partC cou loss {a}", d * d / (18 * b) == cl)
    check(f"L07 partC mon profit {a}", (F(a + b * c, 2 * b) - c) * (d / 2) == pm)
    cou_fee = F(a + 2 * b * c, 3 * b)
    check(f"L07 partC cou two-exchange profit {a}", (cou_fee - c) * (2 * d / 3) == pc)
# R1 and R3
Qr1 = F(1) - F(2) ** F(1, 2) / 4  # times d; use float check for the root
check("L07 R1 monopoly half loss", abs(float((1 - Qr1) ** 2) - 1 / 8) < 1e-12)
check("L07 R1 Cournot/monopoly loss ratio", F(8, 18) == F(4, 9))
for lam in (F(0), F(2, 7), F(1), F(3)):
    dd = F(1)
    W_m = lam * F(1, 8) + F(1, 4)
    W_c = lam * F(2, 9) + F(2, 9)
    check(f"L07 R3 diff lam={lam}", W_c - W_m == (7 * lam - 2) / 72)

# ---------- L08 ----------
def run_L08(X, Y):
    grid = [(x, y) for x in range(X + 1) for y in range(Y + 1)]

    def uA(x, y):
        return F(x) * F(y)

    def uB(x, y):
        return F(X - x) * F(Y - y)

    def dominated(z, w):
        return uA(*z) >= uA(*w) and uB(*z) >= uB(*w) and (uA(*z) > uA(*w) or uB(*z) > uB(*w))

    eff = [w for w in grid if not any(dominated(z, w) for z in grid)]
    interior = [w for w in eff if 0 < w[0] < X and 0 < w[1] < Y]
    boundary = [w for w in eff if w not in interior]
    diag = [w for w in grid if 0 < w[0] < X and 0 < w[1] < Y and w[1] * X == w[0] * Y]
    off = [w for w in interior if w not in diag]
    eq = []
    for x, y in grid:
        A, B = uA(x, y), uB(x, y)
        slack = X * Y - A - B
        assert slack >= 0 and 4 * A * B <= slack * slack, (x, y)
        if 4 * A * B == slack * slack:
            eq.append((x, y))
    return grid, eff, interior, boundary, diag, off, eq, uA, uB


grid, eff, interior, boundary, diag, off, eq, uA, uB = run_L08(8, 4)
print("L08 grid", len(grid), "eff", len(eff), "interior", len(interior), sorted(interior))
print("L08 boundary", boundary, "diag interior", diag, "off", len(off), "equality", eq)
check("L08 counts", len(grid) == 45 and len(eff) == 15 and len(interior) == 13 and len(off) == 10 and len(diag) == 3)
check("L08 boundary is (0,0),(8,4)", sorted(boundary) == [(0, 0), (8, 4)])
check("L08 equality points", sorted(eq) == [(0, 0), (2, 1), (4, 2), (6, 3), (8, 4)])
check("L08 interior list", sorted(interior) == sorted([(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (4, 1), (4, 2), (4, 3), (5, 2), (5, 3), (6, 2), (6, 3), (7, 3)]))
check("L08 21 interior points", (8 - 1) * (4 - 1) == 21 and F(13, 21) > F(619, 1000) - F(1, 1000))
print("L08 13/21 =", float(F(13, 21)))


def improvement(X, Y, x, y):
    """Independent improvement: rational lambda midpoint of the two rates, h = half of admissible bound."""
    xa, ya = F(x), F(y)
    xb, yb = F(X) - xa, F(Y) - ya
    ra, rb = ya / xa, yb / xb
    lam = (ra + rb) / 2
    if rb < ra:
        h = min((ya - lam * xa) / lam, (lam * xb - yb) / lam) / 2
        new = (xa + h, ya - lam * h)
    else:
        h = min((lam * xa - ya) / lam, (yb - lam * xb) / lam) / 2
        new = (xa - h, ya + lam * h)
    nA = new[0] * new[1]
    nB = (X - new[0]) * (Y - new[1])
    return new, nA, nB


for (x, y) in off:
    new, nA, nB = improvement(8, 4, x, y)
    ok = nA > uA(x, y) and nB > uB(x, y)
    check(f"L08 improvement {(x, y)}", ok)
    check(f"L08 improvement noninteger {(x, y)}", any(v.denominator != 1 for v in new))
print("L08 improvements: checked", len(off))
# Lab printed numbers (lines 311-320) recomputed
printed = {(1, 1): ((F(6, 5), F(6, 7)), F(36, 35), F(748, 35)), (3, 1): ((F(18, 7), F(6, 5)), F(108, 35), F(76, 5)),
           (4, 1): ((F(3), F(3, 2)), F(9, 2), F(25, 2)), (7, 3): ((F(34, 5), F(22, 7)), F(748, 35), F(36, 35))}
for (x, y), (newA, eA, eB) in printed.items():
    check(f"L08 printed amount {(x, y)} utA", newA[0] * newA[1] == eA)
    check(f"L08 printed amount {(x, y)} utB", (8 - newA[0]) * (4 - newA[1]) == eB)
# M1 / M2 / M3 / P3 / E1 / R3 / R1 / q9 numbers
check("L08 M1 y=2", F(10 * 2) == F(4 * 5) and F(4) * F(2) == 8 and F(6) * F(3) == 18)
lam = F(11, 24)
check("L08 M2 bounds", (F(1, 4) < lam < F(2, 3)) and (lam * 4 - 1) / lam == F(20, 11) and (4 - lam * 6) / lam == F(30, 11))
hh = F(10, 11)
nA = (F(4) - hh) * (F(1) + lam * hh)
nB = (F(6) + hh) * (F(4) - lam * hh)
check("L08 M2 utilities", nA == F(289, 66) and nB == F(817, 33) and nA > 4 and nB > 24)
check("L08 M3 sqrt sum", abs((18 ** 0.5 + 2 ** 0.5) ** 2 - 32) < 1e-9)
check("L08 E1 gains", F(108, 35) - 3 == F(3, 35) and F(76, 5) - 15 == F(1, 5))
check("L08 E1 share A 2.86%", round(float(F(3, 35) / 3) * 100, 2) == 2.86 and round(float(F(3, 35) / 3) * 100, 1) == 2.9)
check("L08 E1 share B 1.33%", round(float(F(1, 5) / 15) * 100, 2) == 1.33)
check("L08 q9 sqrt(32) two decimals", round((2 * 8 ** 0.5), 2) == 5.66)
# R1 image: s + t constant on the diagonal
for X, Y in ((8, 4), (10, 5), (3, 7)):
    for x in range(0, X + 1):
        s = x * ((F(Y, X)) ** 0.5)  # sqrt(uA) = x sqrt(Y/X) on the diagonal, since uA = x * (Y/X) x
        t = (X - x) * ((F(Y, X)) ** 0.5)  # sqrt(uB) = (X - x) sqrt(Y/X)
        check(f"L08 R1 s+t const {X},{Y},{x}", abs((s + t) - (X * Y) ** 0.5) < 1e-9)
# R3 boundary example
check("L08 R3 uA 0 uB 16", F(0) * F(2) == 0 and (8 - 0) * (4 - 2) == 16)
check("L08 R3 new", F(8, 3) * 1 == F(8, 3) and (F(8) - F(8, 3)) * (F(4) - F(1)) == 16)
# Check Proposition 2.3 identities on a finite box with random rational points
import random
random.seed(3)
for _ in range(2000):
    X = random.randint(1, 9)
    Y = random.randint(1, 9)
    x = F(random.randint(0, 4 * X), 4)
    y = F(random.randint(0, 4 * Y), 4)
    if x > X or y > Y:
        continue
    uA_ = x * y
    uB_ = (X - x) * (Y - y)
    p = x * (Y - y)
    q = y * (X - x)
    check("P2.3 identity p+q", p + q == X * Y - uA_ - uB_)
    check("P2.3 identity product", uA_ * uB_ == p * q)
    check("P2.3 equality iff diagonal", (p == q) == (y * X == x * Y))

# ---------- L09 ----------
n09 = 0
for b in range(1, 6):
    for a in range(1, 40):
        for c in range(0, a):
            for e in range(0, a - c):
                if c + e >= a:
                    continue
                qp = F(a - c, b)
                qs = F(a - c - e, b)
                check("L09 P1.3", qp - qs == F(e, b))
                V = lambda q: a * q - F(b, 2) * q * q - (c + e) * q
                check("L09 P1.4 completed square", all(V(q) == V(qs) - F(b, 2) * (q - qs) ** 2 for q in (F(0), qp, F(3, 2), F(qs))))
                check("L09 C1.5 loss", V(qs) - V(qp) == F(e * e, 2 * b))
                wedge = lambda q: (c + e) - (a - b * q)
                check("L09 wedge area", trap_exact(wedge, qs, qp) == F(e * e, 2 * b))
                # tax t: market quantity (a-c-t)/b, equals qs only at t=e among integer taxes in [0, a-c)
                taxes = [t for t in range(0, a - c) if F(a - c - t, b) == qs]
                check("L09 P1.6 unique tax", taxes == ([e] if e >= 0 else []) or (e == 0 and taxes == [0]) or taxes == [e])
                n09 += 1
print("L09 tuples checked:", n09)
# Lab 1 Part A numbers
a, b, c, e = 1000, 10, 200, 120
qp = F(1000 - 200, 10)
qs = F(1000 - 200 - 120, 10)
check("L09 80/68", qp == 80 and qs == 68)
check("L09 taxes list [120]", [t for t in range(0, 201) if F(1000 - 200 - t, 10) == qs] == [120])
check("L09 revenue 8160", 120 * 68 == 8160 and F(8160, 100) == F(408, 5))
check("L09 loss 720", F(120 * 120, 2 * 10) == 720 and (F(320 - 320) + F(320 - 200)) / 2 * 12 == 720)
check("L09 wedge at 80 is 120", (200 + 120) - (1000 - 10 * 80) == 120)
check("L09 units 69..80 below 320 under P(n)", all(1000 - 10 * n < 320 for n in range(69, 81)) and 1000 - 10 * 68 == 320)
check("L09 continuous reading: price at quantity 68 equals 320 (unit 69 starts at 320)", 1000 - 10 * 68 == 320)


def S(g):
    def A(s):
        w1 = 1000 - 100 * s
        w2 = max(F(0), 600 - 200 * s)
        return w1 + w2
    pieces = [(F(0), min(g, F(3)))]
    if g > 3:
        pieces.append((F(3), g))
    area = sum(((A(lo) + A(hi)) / 2 * (hi - lo) for lo, hi in pieces), F(0))
    return area - 400 * g


check("L09 S(6)=2700", S(F(6)) == 2700)
check("L09 S(7)=2650", S(F(7)) == 2650)
check("L09 S(4)=2500", S(F(4)) == 2500)
grid_best = max((F(k, 100) for k in range(0, 1001)), key=S)
check("L09 public-good maximiser on 0..10 grid is 6", grid_best == 6)
check("L09 integer maximiser 6", max(range(0, 11), key=lambda g: S(F(g))) == 6)
check("L09 E2 shares", F(2650, 2700) == F(53, 54) and round(float(F(2650, 2700)) * 100, 1) == 98.1)
check("L09 E2 4-unit share", round(float(F(2500, 2700)) * 100, 1) == 92.6)
check("L09 E2 3450", trap_exact(lambda s: 1600 - 300 * s, F(0), F(3)) == 3450 and trap_exact(lambda s: 1000 - 100 * s, F(3), F(4)) == 650)
# M2 separately
Aem2 = lambda s: (800 - 100 * s) + (400 - 100 * s)
check("L09 M2 vertical sum", Aem2(F(0)) == 1200 and Aem2(F(7, 2)) == 500)
check("L09 M2 total surplus 1225", trap_exact(Aem2, F(0), F(7, 2)) - 500 * F(7, 2) == 1225)
check("L09 M3 horizontal 3", (800 - 500) / 100 == 3 and max(F(0), (400 - 500) / 100) == 0)
check("L09 E1 100-tax loss 20", (F(5) * (70 - 68) ** 2) == 20 and F(320 - 300) == 20)
check("L09 E1 wedge area 20", trap_exact(lambda q: 320 - (1000 - 10 * q), F(68), F(70)) == 20)
for a0, b0, c0, k0 in product((50, 60, 90), (1, 2, 5), (0, 3, 10), (1, 2, 4)):
    qs0 = F(a0 - c0, b0 + k0)  # efficient quantity with marginal damage k q
    t0 = (a0 - c0) - b0 * qs0  # tax that gives q(t) = qs0, from (a - c - t)/b = qs0
    check("L09 R1 eff qty solves", a0 - b0 * qs0 == c0 + k0 * qs0)
    check("L09 R1 t = k q_s", t0 == k0 * qs0)
check("L09 R2 numbers", F(800 - 400, 10) == 40 and abs(float(F(800, 15)) - 53.33) < 0.01)
check("L09 R2 ratio distinct", all(((b0 - k0) * (b0 + k0) != b0 * b0) for b0 in range(1, 9) for k0 in range(1, 9)))
check("L09 R3 A(6)=400 on [3,10] branch", 1000 - 100 * 6 == 400 and 1600 - 300 * 3 == 700 == 1000 - 100 * 3)
print("FAILS:", fails)
print("TOTAL FAILS:", len(fails))
