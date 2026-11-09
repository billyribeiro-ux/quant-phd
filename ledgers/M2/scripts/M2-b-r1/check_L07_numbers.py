# Independent recomputation of L07 prose numbers (run with python -I).
from fractions import Fraction as F
from math import factorial
import re, html, sys
# E1 ratio from printed decimals
e5 = 0.0010414286; e4 = 0.0034714286
r = e5 / e4
print("E1 printed ratio", repr(r), "rel diff vs 0.3", abs(r - 0.3) / 0.3)
# exact errors
x = F(3, 10)
for n in (4, 5, 9, 10):
    exact_err = x ** (n + 1) / (1 - x)
    print("n", n, "exact err", float(exact_err))
print("ratio exact", float(x ** 6 / (1 - x) / (x ** 5 / (1 - x))))
# Example 2.4 sig figs of degree-10 error
print("deg10 err", float(x ** 11 / (1 - x)), "%.5e" % float(x ** 11 / (1 - x)))
# E2
for n in range(7, 11):
    v = (F(1, 2)) ** (n + 1) / F(3, 2)
    print("E2 n", n, float(v), v <= F(1, 1000))
# R2
print("2^19", 2**19, "2^20", 2**20, 2**19 < 10**6 <= 2**20)
# R1 remainder check: f(x)-P_n(x) at x=0.3 with center 1/2
def f(t): return F(1) / (1 - t)
def Pc(t, n):
    u = 2 * t - 1
    return sum(F(2) ** (k + 1) * (t - F(1, 2)) ** k for k in range(n + 1))
t = F(3, 10)
for n in range(0, 6):
    lhs = f(t) - Pc(t, n)
    rhs = (2 * t - 1) ** (n + 1) / (1 - t)
    print("R1 n", n, lhs == rhs)
# Example 1.5 / problem values
print("f''(1/2)", 2 / F(1, 2) ** 3, "f'''(1/2)", 6 / F(1, 2) ** 4)
print("P2(1/2)", 1 + F(1, 2) + F(1, 4), "err", 2 - (1 + F(1, 2) + F(1, 4)))
print("P3(1/2) err", 2 - (1 + F(1, 2) + F(1, 4) + F(1, 8)))
# M2 cubic
g = lambda t: t**3 - 2*t + 1
print("cubic P3 equals g at sample pts", all(g(F(k, 7)) == 1 - 2*F(k, 7) + F(k, 7)**3 for k in range(-20, 21)))
# Section 5 claim: at x=2, deg 10 error
print("x=2 deg10 err", (F(2) ** 11) / (1 - F(2)))
