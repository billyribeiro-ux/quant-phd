"""Independent re-derivation of every L23 number on the page, from the closed forms (Fraction), not from the twin.

Run: .venv/bin/python -I ledgers/M2/scripts/M2-d2-r8/l23_numbers.py
"""
from fractions import Fraction as Fr
import math

def cf(t, N=10):
    return 5000 + (100000 if t == N else 0)

def P(y, cfs):
    v = 1 + Fr(y)
    return sum((Fr(c) / v**t for t, c in cfs), Fr(0))

def P1(y, cfs):
    return sum((-Fr(t * c) / (1 + Fr(y)) ** (t + 1) for t, c in cfs), Fr(0))

def P2(y, cfs):
    return sum((Fr(t * (t + 1) * c) / (1 + Fr(y)) ** (t + 2) for t, c in cfs), Fr(0))

def P3(y, cfs):
    return sum((-Fr(t * (t + 1) * (t + 2) * c) / (1 + Fr(y)) ** (t + 3) for t, c in cfs), Fr(0))

cfs = [(t, cf(t)) for t in range(1, 11)]
y0 = Fr(0.04)  # the float 0.04 as its exact binary value, as the lab does
p0 = P(0.04, cfs)
print("P(0.04) exact-float-input =", float(p0), "rounded half-even:", round(p0))
print("P'(0.04) =", float(P1(0.04, cfs)), " P''(0.04) =", float(P2(0.04, cfs)))
print("-P'/P =", float(-P1(0.04, cfs) / p0), " P''/P =", float(P2(0.04, cfs) / p0))

# Taylor errors at the three steps, exact minus expansion, with float sensitivities exactly as the lab
d1 = Fr(float(P1(0.04, cfs)))
d2 = Fr(float(P2(0.04, cfs)))
prev = None
for dy in (0.01, 0.005, 0.0025):
    ex = P(0.04 + dy, cfs)
    t1 = p0 + d1 * Fr(dy)
    t2 = t1 + Fr(1, 2) * d2 * Fr(dy) ** 2
    e1 = ex - t1
    e2 = ex - t2
    line = f"dy={dy}: first-order error {float(e1):.6e} second-order error {float(e2):.6e}"
    if prev is not None:
        line += f"  ratios {float(prev[0]/e1):.4f} {float(prev[1]/e2):.4f}"
    print(line)
    prev = (e1, e2)

for dy in (0.01, -0.01):
    ex = P(0.04 + dy, cfs)
    t2 = p0 + d1 * Fr(dy) + Fr(1, 2) * d2 * Fr(dy) ** 2
    print(f"shift {dy:+}: exact unrounded {float(ex):.9f} rounded {round(ex)}; expansion {float(t2):.6f} rounded {round(t2)}; exact-expansion unrounded {float(ex-t2):.6f}")

# Float offset claim (E3): 0.04 + 0.01 versus 1/20
off = Fr(0.04 + 0.01) - Fr(1, 20)
print("0.04+0.01 float =", repr(0.04 + 0.01), " offset from 1/20 =", float(off))
print("P'(0.05) exact-ish float =", float(P1(0.04 + 0.01, cfs)), " P'*offset =", float(P1(0.04 + 0.01, cfs)) * float(off))
pr05 = P(0.04 + 0.01, cfs)
print("unrounded price at float 0.05 =", float(pr05), " minus 100000 =", float(pr05 - 100000))
# price at exact 0.05 = 100000 by Proposition 2.2
print("price at exact 1/20 =", P(Fr(1, 20), cfs))

# why-it-matters: second-order error at +0.01 (Part B)
# M1 check: 2-year bond face 1000 coupon 5% at yield 5%
m1 = [(1, Fr(50)), (2, Fr(1050))]
print("M1 price", float(sum((c / (1 + Fr(1, 20)) ** t for t, c in m1), Fr(0))))
print("M1 terms", float(Fr(50) / Fr(21, 20)), float(Fr(1050) / Fr(21, 20) ** 2))
# Q8 two cash flows c1=-1, c2=1000 at y=0.04
q8 = [(1, -1), (2, 1000)]
print("Q8 P'(0.04) =", float(P1(0.04, q8)), " P'(0.04) two-decimal =", round(float(P1(0.04, q8)), 2))
# M3 zero coupon: P'(0.04) = -200/1.04^3
print("M3 -200/1.04^3 =", -200 / 1.04**3)
# E3 P'(0.05)
print("E3 P'(0.05) =", float(P1(Fr(1, 20), cfs)))
# R2 shift 0.5: first and second order errors magnitude (not printed)
print("y0+0.5 =", 0.54, "> -1:", 0.54 > -1)
print("Sanity: P(0.04) float", float(p0))
