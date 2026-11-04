"""Round-6 checks of the float-offset claims on L23 (E3) and the unrounded central errors on L24 (E3). Standard library only."""
import math
from fractions import Fraction

s = 0.04 + 0.01                      # the float the lab's y0 + dy evaluates to
print("repr(0.04+0.01) =", repr(s), " equals float 0.05:", s == 0.05)
off = Fraction(s) - Fraction(1, 20)  # exact rational value of the stored float minus the decimal 1/20
print("exact offset of stored float from 1/20 =", float(off), " (", off, ")")
PPRIME = None
FACE = 100000; COUP = 5000; N = 10
def c(t): return COUP + (FACE if t == N else 0)
def P1(y):
    v = 1 + Fraction(y)
    return -sum((Fraction(t * c(t)) / v ** (t + 1) for t in range(1, N + 1)), Fraction(0))
pp = float(P1(0.05))
print("P'(0.05) =", pp, " effect on unrounded price = P' * offset =", pp * float(off), "cents")
# exact price at the stored float, minus exact price at 1/20 (= 100000 exactly by Proposition 2.2)
def P(y):
    v = 1 + Fraction(y)
    return sum((Fraction(c(t)) / v ** t for t in range(1, N + 1)), Fraction(0))
print("P(stored 0.05) - 100000 =", float(P(s) - 100000), "cents; P(1/20 exact) - 100000 =", float(P(Fraction(1, 20)) - 100000) if False else "n/a (Fraction input)")
print("exact P(1/20) check via Fraction:", P(Fraction(1, 20)) == 100000)
# L24 E3: unrounded central errors at h = 1e-5 and 1e-7 for exp at 1, computed from the same float expressions as the lab
e = math.e
def central(h):
    return (math.exp(1 + h) - math.exp(1 - h)) / (2.0 * h)
ec5 = abs(central(1e-5) - e)
ec7 = abs(central(1e-7) - e)
print("central error h=1e-5 (float) =", repr(ec5), " ->", f"{ec5:.6e}")
print("central error h=1e-7 (float) =", repr(ec7), " ->", f"{ec7:.6e}")
print("difference =", f"{abs(ec5 - ec7):.6e}", " ulp(e) =", math.ulp(e))
# exact-rational variant for the same float inputs (exp values as floats, subtraction exact)
for h in (1e-5, 1e-7):
    num = Fraction(math.exp(1 + h)) - Fraction(math.exp(1 - h))
    cen = num / (2 * Fraction(h))
    print(f"exact-rational quotient of float exp values at h={h}: error vs e (float) =", f"{abs(float(cen) - e):.6e}")
print("target e as float:", repr(e), " 10-digit:", f"{e:.10f}")
