"""Verifier round 5: check every printed Part C improvement of L08 and the L09 numbers, exact Fractions."""
from fractions import Fraction as F
import re
X, Y = 8, 4
ua = lambda x, y: x * y
ub = lambda x, y: (X - x) * (Y - y)
out = open("/tmp/e1c-v/r5/lab-E1-L08-1.out", encoding="utf-8").read()
pat = re.compile(r"from \((\d+), (\d+)\) \(utilities (\S+) and (\S+)\), A and B can move to A = \(([^)]*)\) and B = \(([^)]*)\), with utilities (\S+) and (\S+)")
def fr(s):
    return F(s) if "/" in s else F(int(s))
n = 0
for m in pat.finditer(out):
    x, y = int(m.group(1)), int(m.group(2))
    a1, a2 = (fr(t.strip()) for t in m.group(5).split(","))
    b1, b2 = (fr(t.strip()) for t in m.group(6).split(","))
    assert a1 + b1 == X and a2 + b2 == Y, "not a reallocation of the totals"
    assert a1 >= 0 and a2 >= 0 and b1 >= 0 and b2 >= 0
    assert ua(a1, a2) == fr(m.group(7)) and ub(a1, a2) == fr(m.group(8)) or True
    assert ua(a1, a2) == fr(m.group(7)) and ub(a1, a2) == fr(m.group(8)), "printed utilities differ"
    assert ua(a1, a2) > ua(x, y) and ub(a1, a2) > ub(x, y), "not strict for both"
    n += 1
print("printed Part C improvements verified exact and strict for both:", n)

# L09 numbers
a, b, c, e = 1000, 10, 200, 120
qp = F(a - c, b); qs = F(a - c - e, b)
print("q_p", qp, "q_s", qs, "gap", qp - qs, "e/b", F(e, b))
print("DWL e^2/(2b)", F(e * e, 2 * b))
W = lambda q: a * q - F(b, 2) * q * q - (c + e) * q
print("W(qp)-W(qs)", W(qp) - W(qs), "check Prop1.4 at qp", W(qs) - F(b, 2) * (qp - qs) ** 2 == W(qp))
print("wedge at 80:", (c + e) - (a - b * 80), " at 68:", (c + e) - (a - b * 68))
print("units 69..80 demand price < 320:", all(a - b * q < c + e for q in range(69, 81)), [a - b * q for q in (69, 80)])
print("revenue 120*68", 120 * 68, "CU", F(120 * 68, 100))
print("tax 100 quantity", F(a - c - 100, b), "loss", F(b, 2) * (F(a - c - 100, b) - qs) ** 2)
print("tax values giving 68:", [t for t in range(0, 201) if F(a - c - t, b) == qs])
print("surplus at 0..100 max at", max(range(0, 101), key=lambda q: W(F(q))))
# public good
def A(g):
    return (1000 - 100 * g) + max(F(0), 600 - 200 * g)
def S(g):
    # exact integral of piecewise linear A on [0,g], split at 3
    g = F(g)
    total = F(0)
    pts = [F(0)] + ([F(3)] if g > 3 else []) + [g]
    for u, v in zip(pts, pts[1:]):
        total += (A(u) + A(v)) / 2 * (v - u)
    return total - 400 * g
print("A(6)", A(6), "A(3)", A(3), "vertical=400 integers:", [g for g in range(11) if A(g) == 400])
print("S(6)", S(6), "S(7)", S(7), "argmax over 0..10", max(range(11), key=lambda g: S(g)), [S(g) for g in range(11)])
print("horizontal at 400:", F(1000 - 400, 100) + max(F(0), F(600 - 400, 200)))
print("M1 l09:", F(600 - 100, 5), F(600 - 150, 5), F(50 * 50, 2 * 5))
print("M2 l09 g*:", F(700, 200), "S:", F(1200) * F(7, 2) - 100 * F(49, 4) - 500 * F(7, 2))
print("R2 l09 k=5:", F(800, 10), F(800 - 400, 10), F(800, 15), float(F(800, 15)) - 40)
print("R1 general check k=5 b=10 a=1000 c=200: t = k*q_s:", F(5 * 800, 15))
print("E1 p2 share", float(F(2650, 2700)), "%", float(F(2650, 2700)) * 100)
