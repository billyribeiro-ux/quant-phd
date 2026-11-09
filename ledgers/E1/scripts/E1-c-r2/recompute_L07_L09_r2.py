"""Verifier E1-c round 2: independent recomputation of every L07-L09 closed form and prose number (Fraction only)."""

from fractions import Fraction as F
import itertools
import math


def half_up(x):
    return math.floor(x + F(1, 2))


# ---------- L07: surplus under linear demand, all triples with a > bc > 0 on a finite set ----------
def poly_int(coeffs, lo, hi):
    # coeffs: list of (power, coef); exact definite integral
    return sum(c * (F(hi) ** (p + 1) - F(lo) ** (p + 1)) / (p + 1) for p, c in coeffs)


bad_L07 = []
n_L07 = 0
for b in range(1, 7):
    for c in range(1, 12):
        for a in range(b * c + 1, b * c + 60, 3):
            n_L07 += 1
            d = F(a - b * c)
            Pq = lambda q: F(a - q) / b  # noqa: E731
            # Theorem 1.2 checked by exact integration of P(x) and P(x)-c
            for Q in (d / 2, 2 * d / 3, d, F(a, 1) / 2):
                CS = poly_int([(0, F(a, b)), (1, F(-1, b))], 0, Q) - Pq(Q) * Q
                PS = (Pq(Q) - c) * Q
                W = poly_int([(0, F(a - b * c, b)), (1, F(-1, b))], 0, Q)
                if CS != Q * Q / (2 * b) or PS != (d - Q) * Q / b or W != (2 * d * Q - Q * Q) / (2 * b):
                    bad_L07.append(("thm12", a, b, c, Q))
                if Q <= d and (d - Q) ** 2 / (2 * b) != (d * d / (2 * b)) - (2 * d * Q - Q * Q) / (2 * b):
                    bad_L07.append(("thm15", a, b, c, Q))
            wd = d * d / (2 * b)
            vols = {"M": (d / 2, F(a + b * c, 2 * b)), "C": (2 * d / 3, F(a + 2 * b * c, 3 * b)), "B": (d, F(c))}
            for k, (Q, fee) in vols.items():
                # fee must be the optimum of the structure (argmax of (f-c)*Q(f) for M; closed form check)
                if k == "M":
                    prof = lambda f: (f - c) * (a - b * f)  # noqa: E731
                    if prof(fee) < prof(fee - F(1, 1000)) or prof(fee) < prof(fee + F(1, 1000)):
                        bad_L07.append(("monopoly-fee", a, b, c))
                if Q != F(a - b * fee) and k != "M" and k != "C":
                    bad_L07.append(("bertrand-vol", a, b, c))
            dwl = {k: wd - (2 * d * Q - Q * Q) / (2 * b) for k, (Q, _) in vols.items()}
            if dwl["M"] != d * d / (8 * b) or dwl["C"] != d * d / (18 * b) or dwl["B"] != 0:
                bad_L07.append(("cor21-dwl", a, b, c))
            # Proposition 2.3 ordering
            if not (0 < dwl["C"] < dwl["M"]):
                bad_L07.append(("prop23-order", a, b, c))
            if dwl["M"] / wd != F(1, 4) or dwl["C"] / wd != F(1, 9):
                # wd = d^2/(2b) is the competitive total surplus
                bad_L07.append(("shares", a, b, c))
            if (d / 2 - F(0)) < 0 or not (F(0) <= 2 * d / 3 <= F(a)):
                bad_L07.append(("volume-in-range", a, b, c))
print("L07 triples:", n_L07, "failures:", bad_L07[:5], len(bad_L07))

# Example 2.2 and prose numbers (reference case a=120,b=1,c=20; M1,M2,M3,P1,R1,R2,R3,E1)
a, b, c = 120, 1, 20
d = F(a - b * c)
print("L07 Ex2.2 d:", d, "competitive W:", d * d / (2 * b))
print("L07 Cournot DWL exact:", d * d / (18 * b), "half-up:", half_up(d * d / (18 * b)))
print("L07 Cournot W exact:", F(40000, 9), "half-up:", half_up(F(40000, 9)), "CS half-up", half_up(F(20000, 9)))
print("L07 M1 (90,3,10): d=", F(90 - 30), "CS", F(30 * 30, 6), "PS", F(30 * 30, 3), "loss", F(3600, 6) - F(450), "d2/8b", F(3600, 24))
print("L07 M2 (90,3,10): Cournot loss", F(20 * 20, 6), "=", F(200, 3), "half-up", half_up(F(200, 3)), "d2/18b", F(3600, 54))
print("L07 M3 midpoint two steps:", sum(F(120) - m for m in (F(25, 2), F(75, 2))) * 25, "antiderivative", 120 * 50 - F(50 * 50, 2))
print("L07 R1 Q/d:", 1 - F(1, 2) ** 0 * 0, "sqrt2/4 approx", round(math.sqrt(2) / 4, 5), "1 - sqrt2/4 =", round(1 - math.sqrt(2) / 4, 5))
print("L07 R1 cournot DWL/monopoly DWL", (F(1, 18)) / F(1, 8), "half monopoly:", F(1, 16))
# R3 weighted
for lam in (F(0), F(2, 7), F(1), F(3)):
    W_M = lam * F(1, 8) + F(1, 4)
    W_C = lam * F(2, 9) + F(2, 9)
    print("L07 R3 lambda", lam, "C-M =", W_C - W_M, "=(7lam-2)/72 ?", W_C - W_M == (7 * lam - 2) / 72)
print("L07 E2 shares d-independent; P3 ratio", (F(1, 8)) / (F(1, 18)))
print("L07 Q-items: 5000/9 =", F(5000, 9), float(F(5000, 9)))

# ---------- L08 ----------
X, Y = 8, 4
def uA(x, y): return x * y
def uB(x, y): return (X - x) * (Y - y)
grid = [(x, y) for x in range(X + 1) for y in range(Y + 1)]
def dom(z, w):
    return uA(*z) >= uA(*w) and uB(*z) >= uB(*w) and (uA(*z) > uA(*w) or uB(*z) > uB(*w))
eff = [w for w in grid if not any(dom(z, w) for z in grid)]
print("L08 grid", len(grid), "grid-efficient", len(eff), eff)
interior_eff = [w for w in eff if 0 < w[0] < X and 0 < w[1] < Y]
diag = [w for w in interior_eff if w[1] * X == w[0] * Y]
off = [w for w in interior_eff if w not in diag]
print("L08 interior eff", len(interior_eff), "diag", diag, "off", len(off))
# recompute P2.3 bound over the whole grid with exact arithmetic and a finer rational lattice
bound_fail = []
for xn in range(0, 8 * 12 + 1):
    for yn in range(0, 4 * 12 + 1):
        x, y = F(xn, 12), F(yn, 12)
        p, q = x * (Y - y), y * (X - x)
        ua, ub = uA(x, y), uB(x, y)
        if p + q != X * Y - ua - ub or p * q != ua * ub:
            bound_fail.append(("identity", x, y))
        # (sqrt ua + sqrt ub)^2 <= XY  <=>  2 sqrt(ua ub) <= XY - ua - ub
        s = X * Y - ua - ub
        if s < 0 or 4 * ua * ub > s * s:
            bound_fail.append(("bound", x, y))
        if (4 * ua * ub == s * s) != (y * X == x * Y):
            bound_fail.append(("equality-diagonal", x, y))
print("L08 finer-lattice (1/12 steps) bound/equality failures:", bound_fail[:5], len(bound_fail))
# improvements for each off-diagonal point: recompute strict improvement with the lab's lambda and check non-integer
for (x, y) in off:
    ra = F(y, x); rb = F(Y - y, X - x)
    if rb < ra:
        lam = (ra + rb) / 2
        # take a generic trade and check both strictly improve; search h on a fine rational grid
        ok = None
        for k in range(1, 400):
            h = F(k, 400) * min((F(y) - lam * x) / lam, (lam * (X - x) - (Y - y)) / lam)
            na = (F(x) + h, F(y) - lam * h)
            if uA(*na) > uA(x, y) and uB(*na) > uB(x, y):
                ok = (na, h)
                break
    else:
        ok = None
        lam = (ra + rb) / 2
        for k in range(1, 400):
            h = F(k, 400) * min((lam * x - y) / lam, (Y - y - lam * (X - x)) / lam)
            na = (F(x) - h, F(y) + lam * h)
            if uA(*na) > uA(x, y) and uB(*na) > uB(x, y):
                ok = (na, h)
                break
    if ok is None or all(v.denominator == 1 for v in ok[0]):
        print("L08 improvement check FAILED or integer at", (x, y), ok)
    else:
        pass
print("L08 improvement search: done for", len(off), "points")
# Remark 2.6 / R3: A holds (0,2): u_A=0, B holds (8,2): u_B=16; trade 8/3 of x for 1 of y
na = (F(8, 3), F(1))
print("L08 R3:", uA(*na), uB(F(8) - 0, F(4)) if False else (X - na[0]) * (Y - na[1]), "old u_B", (X - 0) * (Y - 2))
# M2 (X=10,Y=5) explicit improvement
Xm, Ym = 10, 5
xm, ym, lam = F(4), F(1), F(11, 24)
h = F(10, 11)
A_new = (xm - h, ym + lam * h)
B_new = (Xm - A_new[0], Ym - A_new[1])
print("L08 M2 A_new", A_new, "uA", A_new[0] * A_new[1], ">4?", A_new[0] * A_new[1] > 4, "uB", B_new[0] * B_new[1], ">24?", B_new[0] * B_new[1] > 24)
print("L08 M2 bounds 20/11, 30/11:", (lam * xm - ym) / lam, (F(Ym - 0) - lam * 0) and ((Ym - lam * 0) - (Ym - ym) + 0), (F(6) * 0 + F(4) - lam * 6) / lam)
# M1
print("L08 M1 y:", F(4 * 5, 10), "uB at (6,3)", (10 - 4) * (5 - 2))
# M3 and quiz
print("L08 M3:", math.sqrt(18) + math.sqrt(2), math.sqrt(32), (math.sqrt(18) + math.sqrt(2)) ** 2)
# E1 (3,1) improvement gains
print("L08 E1 gains:", F(18, 7) * F(6, 5) - 3, F(38, 7) * F(14, 5) - 15, float(F(1, 35) / 3 * 100), float(F(1, 5) / 15 * 100))
print("L08 E2 share 13/21 =", float(F(13, 21)), "7*3=", 7 * 3)
print("L08 E3:", [(x, y) for (x, y) in grid if x * (Y - y) == y * (X - x)])
print("L08 quiz (4,2) sum", 2 * math.sqrt(8), math.sqrt(32))
print("L08 quiz Q5: (2,1) yX", 1 * 8, "xY", 2 * 4, " (1,2):", 2 * 8, 1 * 4, " (3,2):", 2 * 8, 3 * 4, " (4,1):", 1 * 8, 4 * 4)
# P1-prime lemma 2.1 by direct check on interior grid
print("L08 Lemma 2.1 holds on interior grid:", all(((y * (X - x) == x * (Y - y)) == (F(y, x) == F(Y - y, X - x))) and ((y * X == x * Y) == (F(y, x) == F(Y, X))) for x in range(1, X) for y in range(1, Y)))
# Example 2.5 utilities
print("L08 Ex2.5", uA(6, 3), uB(6, 3), uA(2, 1), uB(2, 1))
print("L08 R2/Remark: LHS of R3 boundary off-diagonal", 0 * Y - 2 * X)

# ---------- L09 ----------
bad9 = []
n9 = 0
for a in range(1, 40, 3):
    for b in range(1, 8):
        for c in range(0, a, 2):
            for e in range(0, 12):
                if c + e >= a:
                    continue
                n9 += 1
                qp = F(a - c, b); qs = F(a - c - e, b)
                if qp - qs != F(e, b):
                    bad9.append(("prop13", a, b, c, e))
                W = lambda q: F(a) * q - F(b, 2) * q * q - (c + e) * q  # noqa: E731
                for q in (F(0), qs, qp, F(3, 7)):
                    if W(q) != W(qs) - F(b, 2) * (q - qs) ** 2:
                        bad9.append(("prop14", a, b, c, e, q))
                if W(qs) - W(qp) != F(e * e, 2 * b):
                    bad9.append(("cor15", a, b, c, e))
                # Prop 1.6: q(t) = qs iff t = e (t in 0..200)
                ts = [t for t in range(0, 201) if F(a - c - t, b) == qs]
                if (e in range(0, 201) and ts != [e]) and not (e > 200):
                    bad9.append(("prop16", a, b, c, e, ts))
                # wedge triangle: gap at qs is 0, at qp is e
                gap_qp = (c + e) - (a - b * qp)
                if gap_qp != e or (c + e) - (a - b * qs) != 0:
                    bad9.append(("wedge", a, b, c, e))
print("L09 triples:", n9, "failures:", bad9[:5], len(bad9))

# Lab 1 Part A numbers
a, b, c, e = 1000, 10, 200, 120
qp = F(a - c, b); qs = F(a - c - e, b)
print("L09 lab qp", qp, "qs", qs, "taxes:", [t for t in range(0, 201) if F(a - c - t, b) == qs])
print("L09 revenue", 120 * 68, "wedge DWL", F(120 + 0, 2) * (qp - qs), "e2/2b", F(e * e, 2 * b))
def Wlab(q):
    return F(1000) * q - F(10, 2) * q * q - 320 * q
print("L09 W(68)-W(80)", Wlab(F(68)) - Wlab(F(80)), "max integer", max(range(0, 101), key=lambda q: Wlab(F(q))))
# public good
def w1(g): return 1000 - 100 * g
def w2(g): return max(F(0), 600 - 200 * g)
def A(g): return w1(g) + w2(g)
def Sg(g):
    # exact integral of A over [0,g] with breakpoint 3
    pts = [F(0)]
    if g > 3:
        pts += [F(3), g]
    else:
        pts += [g]
    area = F(0)
    for lo, hi in zip(pts, pts[1:]):
        area += (A(lo) + A(hi)) / 2 * (hi - lo)
    return area - 400 * g
print("L09 PG vertical at 6:", A(F(6)), " W2(6)", w2(F(6)), "W1(6)", w1(F(6)))
print("L09 PG S(6), S(7), S(4):", Sg(F(6)), Sg(F(7)), Sg(F(4)), " share 2650/2700", F(2650, 2700), float(F(2650, 2700)))
print("L09 PG maximiser over integers 0..10:", max(range(11), key=lambda g: Sg(F(g))))
print("L09 PG maximiser over 1/100 grid 0..10:", max((F(k, 100) for k in range(0, 1001)), key=Sg))
print("L09 E2 at 4 units:", F(3450) + 650 - 1600, "int 0..3 of 1600-300s:", 1600 * 3 - F(300, 2) * 9, "int 3..4 of 1000-100s:", 1000 - F(100, 2) * (16 - 9), "S(4)", Sg(F(4)), "2500/2700", float(F(2500, 2700)))
print("L09 E2 check 2650/2700", float(F(2650, 2700)), "2500/2700", float(F(2500, 2700)))
print("L09 M1: qp", F(600 - 100, 5), "qs", F(600 - 150, 5), "DWL e2/2b", F(2500, 10), "triangle", F(1, 2) * 10 * 50)
# M2: A(g)=1200-200g ; A(g*)=500
gstar = F(1200 - 500, 200)
print("L09 M2 g*", gstar, "cons2 at g*", 400 - 100 * gstar, "S", F(1200) * gstar - 100 * gstar * gstar - 500 * gstar)
print("L09 M2 check w2 on [0,3.5] non-neg?", all(400 - 100 * F(k, 10) >= 0 for k in range(0, 36)))
# M3 horizontal price 500
print("L09 M3 horizontal:", F(800 - 500, 100), "+", max(F(0), F(400 - 500, 100)), "eff 3.5")
# E1 tax 100
print("L09 E1 q(100)", F(1000 - 200 - 100, 10), "loss b/2 (70-68)^2", F(10, 2) * (70 - 68) ** 2, "gap at 70", 320 - (1000 - 700), "area", F(1, 2) * (0 + 20) * 2)
# E3: consumer 2 line at 6, consumer 1 line at 6; crossing beyond 3
print("L09 E3 w2(6) raw", 600 - 200 * 6, " w1(6)", 1000 - 100 * 6, " A on [0,3] min", 1600 - 300 * 3)
# R1 tax equals damage at efficient quantity: random check
bad_R1 = []
for a_ in range(10, 60, 7):
    for b_ in range(1, 6):
        for c_ in range(0, 5):
            for k in range(1, 5):
                qs_ = F(a_ - c_, b_ + k)
                t = a_ - c_ - b_ * qs_
                if t != k * qs_ or F(a_ - c_ - t, b_) != qs_:
                    bad_R1.append((a_, b_, c_, k))
print("L09 R1 failures:", bad_R1[:3], len(bad_R1))
# R2 numbers
qp2 = F(1000 - 200, 10); t2 = 5 * qp2; q2 = (F(1000 - 200) - t2) / 10; qs2 = F(1000 - 200, 15)
print("L09 R2 qp", qp2, "t", t2, "q", q2, "qs", qs2, float(qs2), "short", float(qs2 - q2))
print("L09 R2 k^2 = 0 claim: (b-k)(b+k)=b^2 iff k=0 ->", [k for k in range(1, 6) if (10 - k) * (10 + k) == 100])
# R3 vertical sum check
print("L09 R3 A(6)=400?", A(F(6)) == 400, " A on [0,3] =1600-300g", all(A(F(k, 4)) == 1600 - 300 * F(k, 4) for k in range(0, 13)))
print("L09 quiz: 120^2/20 =", F(120 ** 2, 20), " 80 and 68:", F(800, 10), F(680, 10))
print("L09 quiz Q10: 5*80=", 5 * 80, "(800-400)/10 =", (800 - 400) / 10)
print("L09 intro line:", "e/b=12", F(120, 10), "ops:", F(120, 10))
