"""Independent re-derivation of the numbers printed or quoted in L23 and L24 (verifier round 3, slice d2)."""
import math
from fractions import Fraction as Fr

# ---- L23: bond, independent of the lab code (own cash flows, own sums)
N, F, C = 10, 100000, 5000
cf = {t: C + (F if t == N else 0) for t in range(1, N + 1)}
def P(y):  # exact rational price at float yield y
    v = 1 + Fr(y)
    return sum(Fr(cf[t]) / v**t for t in range(1, N + 1))
def P1(y):
    v = 1 + Fr(y)
    return -sum(Fr(t * cf[t]) / v**(t + 1) for t in range(1, N + 1))
def P2(y):
    v = 1 + Fr(y)
    return sum(Fr(t * (t + 1) * cf[t]) / v**(t + 2) for t in range(1, N + 1))
def P3(y):
    v = 1 + Fr(y)
    return -sum(Fr(t * (t + 1) * (t + 2) * cf[t]) / v**(t + 3) for t in range(1, N + 1))

y0 = 0.04
p0 = P(y0); d1 = float(P1(y0)); d2 = float(P2(y0))
print("L23 P(0.04) unrounded", float(p0), "round", round(p0))
print("L23 P'(0.04)", d1, "P''(0.04)", d2)
print("L23 -P'/P", -d1 / float(p0), "P''/P", d2 / float(p0))
# central difference checks (float, as in the lab)
def pf(y): return float(P(y))
print("L23 central P' step 1e-5 diff", abs(d1 - (pf(y0 + 1e-5) - pf(y0 - 1e-5)) / 2e-5))
print("L23 central P'' step 1e-4 diff", abs(d2 - (float(P1(y0 + 1e-4)) - float(P1(y0 - 1e-4))) / 2e-4))
# Taylor errors, exact
def t1(dy): return P(y0) + Fr(d1) * Fr(dy)
def t2(dy): return t1(dy) + Fr(1, 2) * Fr(d2) * Fr(dy) ** 2
prev1 = prev2 = None
for dy in (0.01, 0.005, 0.0025):
    e1 = float(P(y0 + dy) - t1(dy)); e2 = float(P(y0 + dy) - t2(dy))
    line = f"shift {dy}: e1 {e1:.6e} e2 {e2:.6e}"
    if prev1 is not None: line += f" ratios {prev1/e1:.4f} {prev2/e2:.4f}"
    print("L23", line)
    prev1, prev2 = e1, e2
for dy in (0.01, -0.01):
    ex = round(P(y0 + dy)); ap = round(t2(dy))
    print("L23 shift", dy, "exact", ex, "second-order", ap, "diff", ex - ap)
# float yield 0.04 + 0.01 and its distance from 0.05
yf = 0.04 + 0.01
print("L23 float 0.04+0.01 =", repr(yf), "minus exact 0.05 (Fraction):", float(Fr(yf) - Fr(1, 20)))
print("L23 unrounded price at float yield 0.05 minus 100000:", float(P(yf) - 100000), "cents")
print("L23 P'(0.05) approx", float(P1(yf)), " product with offset:", float(P1(yf)) * float(Fr(yf) - Fr(1, 20)))
# quiz 8 counterexample: c1=-1, c2=1000, N=2 at y=0.04
c = {1: -1, 2: 1000}
v = 1 + Fr(0.04)
q = -sum(Fr(t * c[t]) / v**(t + 1) for t in (1, 2))
print("L23 quiz8 P'(0.04) with c1=-1,c2=1000:", float(q))
# M1 two-year bond at 0.05: 50/1.05 + 1050/1.05^2
print("L23 M1 check:", 50 / 1.05 + 1050 / 1.05**2, "rounded terms", 47.619 + 952.381)
print("L23 M3 zero coupon P'(0.04)=-200/1.04^3:", -200 / 1.04**3)

# ---- L24: |x| and exp
for k in range(1, 7):
    h = 10.0 ** -k
    fw = (abs(0 + h) - abs(0.0)) / h; bw = (abs(0.0) - abs(0 - h)) / h; ce = (abs(0 + h) - abs(0 - h)) / (2 * h)
    assert (fw, bw, ce) == (1.0, -1.0, 0.0), (k, fw, bw, ce)
print("L24 Part A exact for six steps: (1,-1,0) confirmed")
e = math.e
def fwd(h): return (math.exp(1 + h) - math.exp(1.0)) / h
def cen(h): return (math.exp(1 + h) - math.exp(1 - h)) / (2 * h)
for k in (5, 7):
    h = 10.0 ** -k
    print(f"L24 central unrounded error at 1e-{k}: {abs(cen(h) - e):.9e}  forward {abs(fwd(h)-e):.9e}")
print("L24 difference of central errors 1e-5 vs 1e-7:", abs(cen(1e-5) - e) - abs(cen(1e-7) - e))
print("L24 ulp of e:", math.ulp(math.e), "half ulp:", math.ulp(math.e) / 2)
print("L24 delta/e etc: 2*sqrt(delta/e)=", 2 * math.sqrt(2.22e-16 / math.e), " (3delta/e)^(1/3)=", (3 * 2.22e-16 / math.e) ** (1 / 3))
print("L24 half e h at 1e-5:", math.e / 2 * 1e-5, " 2delta/h at 1e-15:", 2 * 2.22e-16 / 1e-15)
print("L24 E3 check: exact e via Fraction-free:", math.e)
print("L24 ratio 4.531e-9/5.859e-11 =", 4.531e-9 / 5.859e-11)
