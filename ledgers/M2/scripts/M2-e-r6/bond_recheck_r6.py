"""Independent recomputation of the L23 bond numbers cited by cards c338-c407 (round 6, slice e)."""
import math
from fractions import Fraction
F, C, N, Y0 = 100000, 5000, 10, 0.04
def cf(t): return C + (F if t == N else 0)
def P(y):
    v = 1 + Fraction(y)
    return sum((Fraction(cf(t)) / v**t for t in range(1, N + 1)), Fraction(0))
def P1(y):
    v = 1 + Fraction(y)
    return float(-sum((Fraction(t * cf(t)) / v**(t + 1) for t in range(1, N + 1)), Fraction(0)))
def P2(y):
    v = 1 + Fraction(y)
    return float(sum((Fraction(t * (t + 1) * cf(t)) / v**(t + 2) for t in range(1, N + 1)), Fraction(0)))
p0 = P(Y0)
print('P(0.04) unrounded', float(p0), 'round-half-even', round(p0))
d1 = P1(Y0); d2 = P2(Y0)
print("P'(y0)", d1, "P''(y0)", d2)
fd1 = (float(P(Y0 + 1e-5)) - float(P(Y0 - 1e-5))) / (2e-5)
fd2 = (P1(Y0 + 1e-4) - P1(Y0 - 1e-4)) / (2e-4)
print('central P\'', fd1, 'diff', abs(d1 - fd1), ' central P\'\'', fd2, 'diff', abs(d2 - fd2))
prev1 = prev2 = None
for dy in (0.01, 0.005, 0.0025):
    ex = P(Y0 + dy)
    T1 = p0 + Fraction(d1) * Fraction(dy)
    T2 = T1 + Fraction(1, 2) * Fraction(d2) * Fraction(dy) ** 2
    e1, e2 = ex - T1, ex - T2
    line = f"dy={dy} e1={float(e1):.6e} e2={float(e2):.6e}"
    if prev1 is not None:
        line += f" ratios {float(prev1 / e1):.4f} {float(prev2 / e2):.4f}"
    print(line)
    prev1, prev2 = e1, e2
for dy in (0.01, -0.01):
    ex = round(P(Y0 + dy))
    T2 = P(Y0) + Fraction(d1) * Fraction(dy) + Fraction(1, 2) * Fraction(d2) * Fraction(dy) ** 2
    print('shift', dy, 'exact cents', ex, 'second-order cents', round(T2), 'diff', ex - round(T2), 'unrounded second-order error', float(P(Y0 + dy) - T2))
print('price at float 0.04+0.01 =', float(P(0.04 + 0.01)), 'at 0.05 exact', float(P(0.05)))
print('P1(-y) check: P2 at 0.05 coupon yield price', float(P(0.05)))
print('P1 at 0.05 (closed form)', P1(0.05))
