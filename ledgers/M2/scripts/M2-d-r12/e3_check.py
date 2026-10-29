import sys, re, html
from fractions import Fraction
sys.path.insert(0, "tests/labs/M2")
y = 0.04 + 0.01
print("0.04+0.01 == 0.05:", y == 0.05, repr(y))
d = Fraction(y) - Fraction(1, 20)
print("float - 1/20 =", float(d), "=", d)
FACE=100000; C=5000; N=10
def cf(t): return C + (FACE if t==N else 0)
def price(yv):
    v = 1 + Fraction(yv)
    return sum((Fraction(cf(t))/v**t for t in range(1,N+1)), Fraction(0))
p_exact_float = price(y)
print("unrounded price at float yield - 100000 =", float(p_exact_float - FACE), "cents")
print("rounded:", round(p_exact_float))
# derivative at par
v = Fraction(21,20)
Pp = -sum((Fraction(t*cf(t))/v**(t+1) for t in range(1,N+1)), Fraction(0))
print("P'(0.05) =", float(Pp))
print("P'(0.05)*d =", float(Pp*d), "cents")
