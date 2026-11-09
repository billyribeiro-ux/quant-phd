"""Exact checks of two prose claims in slice a (verifier round 1).

1. L01 Remark 2.4: 'The consumer would give up 4/3 units of y for one more unit of x.' Exact offset for a
   whole unit of x at the bundle (20, 80/3) on utility u = xy.
2. L02 Misconception 1 and card E1-c024: 'Average cost C(q)/q = F/q + c + kq is lowest at q = sqrt(F/k).'
   Exact derivative and second derivative of AC, and the AC values around sqrt(12).
Usage: python -I remark_checks.py
"""

from fractions import Fraction as F

u0 = F(20) * F(80, 3)                 # utility at (20, 80/3)
y_new = u0 / F(21)                    # height y that keeps utility u0 at x = 21
offset = F(80, 3) - y_new             # units of y given up for one whole extra unit of x
print(f"1. utility at (20, 80/3) = {u0}; y at x=21 with same utility = {y_new} = {float(y_new):.6f}")
print(f"   exact offset for one whole unit of x = {offset} = {float(offset):.6f}")
print(f"   claim 4/3 = {float(F(4, 3)):.6f}; equal to exact offset: {offset == F(4, 3)}")
print(f"   small-step offset (MRS) at x=20: {float(F(4, 3)):.6f}; ratio y/x = {F(80,3)/20}")

# AC(q) = F/q + c + k q with F=12, c=2, k=1 (case 1 of L02). Its derivative is -F/q^2 + k.
Fx, c, k = 12.0, 2.0, 1.0
ac = lambda q: Fx / q + c + k * q
dac = lambda q: -Fx / q**2 + k
q0 = (Fx / k) ** 0.5
print(f"2. AC(sqrt(12)) = {ac(q0):.6f}; AC'(sqrt(12)) = {dac(q0):.2e}; AC''(q) = 2F/q^3 = {2*Fx/q0**3:.6f} > 0")
print(f"   AC at q=3,3.4641,4: {ac(3.0):.6f}, {ac(q0):.6f}, {ac(4.0):.6f}")
print("   the page states the minimiser without a derivative; the lab evaluates profit at sqrt(F/k) only")
