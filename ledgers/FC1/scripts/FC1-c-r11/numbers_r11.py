"""Re-derive every number on FC1 project page and the new r11 test docstrings with Fraction (verifier, r11)."""
from fractions import Fraction as F
import math


def half_away(x):
    m = abs(x)
    w = (2 * m.numerator + m.denominator) // (2 * m.denominator)
    return w if x >= 0 else -w


def events(face, cbps, n):
    c = half_away(F(face * cbps, 10000))
    ev = [(t, c) for t in range(1, n + 1)]
    ev[-1] = (n, ev[-1][1] + face)
    return ev


def pv_exact(ev, ybps):
    y = F(ybps, 10000)
    return sum((F(a) / (1 + y) ** t for t, a in ev), F(0))


def price(ev, ybps):
    return half_away(pv_exact(ev, ybps))


def term_price(ev, ybps):
    y = F(ybps, 10000)
    return sum(half_away(F(a) / (1 + y) ** t) for t, a in ev)


# Lab 1
ev1 = events(100000, 500, 3)
print("lab1 events", ev1)
ex1 = pv_exact(ev1, 400)
print("lab1 exact float %.6f" % float(ex1), "price", price(ev1, 400), "term-by-term", term_price(ev1, 400))
print("lab1 exact float repr", repr(float(ex1)))
print("lab1 trade", (2, -1 * 10 * 9850))
# Fixture A
A = events(10000, 500, 1); print("A", A, "price@500", price(A, 500), "exact", pv_exact(A, 500))
# B
B = events(10000, 500, 1); print("B price@-500", price(B, -500), "exact", float(pv_exact(B, -500)), "=210000/19?", pv_exact(B, -500) == F(210000, 19))
print("B exact 4dp", "%.4f" % float(F(10500) / F(95, 100)))
# C
C = events(10001, 5000, 2); print("C", C)
# D
D = events(1, 5000, 1); print("D", D)
# E
print("E", (2, -10 * 9850), "seller", (2, 10 * 9850))
# F
Fv = events(1, 0, 1); print("F", Fv, "exact", pv_exact(Fv, 10000), "price", price(Fv, 10000), "python round", round(pv_exact(Fv, 10000)), round(float(pv_exact(Fv, 10000))))
# G
G = events(10001, 0, 1); print("G", G, "exact", pv_exact(G, 10000), "price", price(G, 10000))
# Rounding fixture
R = events(10000, 500, 3); print("R", R, "exact", float(pv_exact(R, 400)), "%.6f" % float(pv_exact(R, 400)), "price", price(R, 400), "termwise", term_price(R, 400))
print("R termwise parts", [float(F(a) / (F(10001, 10000)) ** t) for t, a in R])
print("R rounded parts", [half_away(F(a) / F(104, 100) ** t) for t, a in R])
# r11 new tests
T1 = events(10000, 500, 1)
print("yield 1e7 bps: exact", pv_exact(T1, 10_000_000), "10500/1001 =", float(F(10500, 1001)), "price", price(T1, 10_000_000))
print("settlement 10**7 trade event", (10**7, -98500))
Z = events(10000, 0, 1001); print("1001 periods zero coupon events tail", Z[-1], "price@0", price(Z, 0), "sum", sum(a for _, a in Z))
# Rounding claim 10277.509103
print("rounded exact 10277.509103 ->", half_away(pv_exact(R, 400)))
# Half-cent claim
h = F(10**40 + 1, 2); print("half cent case exact", h, "price", half_away(h), "frac", h - int(h))
# Hair under half cent claim
print("hair-under-half case: find in test file later")
# Lab 3 fixtures
print("B 210000/19 float", 210000 / 19)
# Bond 13..15 etc not needed here
# 1001-period bond at 400bps: last-event size
Q = events(10000, 500, 1001); e = pv_exact(Q, 400)
print("1001p at 400bps exact", float(e), "price", price(Q, 400))
print("1001p dropping period 1001 at 400bps exact", float(e - F(Q[-1][1], (1 + F(400, 10000)) ** 1001)), "price", half_away(e - F(Q[-1][1], (1 + F(400, 10000)) ** 1001)))
