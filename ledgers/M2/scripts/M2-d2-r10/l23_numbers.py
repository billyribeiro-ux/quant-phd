"""M2-d2 r10: independent recomputation of the L23 numbers (exact rationals, no lab code reused).

Checks the lesson figures: unrounded price, integer price, P', P'', central differences, preview
ratios, first/second-order errors at +-0.01, 0.005, 0.0025, the error ratios, the -15/+16 cent
differences, the float offset 0.04+0.01 vs 1/20, the quiz two-cash-flow P', and M1 price.
"""
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_EVEN

N = 10
c = {t: F(5000) + (F(100000) if t == N else F(0)) for t in range(1, N + 1)}

def P(y):  # exact rational price in cents, y a Fraction
    return sum(c[t] / (1 + y) ** t for t in range(1, N + 1))

def P1(y):
    return -sum(t * c[t] / (1 + y) ** (t + 1) for t in range(1, N + 1))

def P2(y):
    return sum(t * (t + 1) * c[t] / (1 + y) ** (t + 2) for t in range(1, N + 1))

y0 = F(4, 100)
p0, p1, p2 = P(y0), P1(y0), P2(y0)
print("unrounded price:", float(p0), "rounded half-even:", Decimal(float(p0)).quantize(Decimal(1), rounding=ROUND_HALF_EVEN))
print("P'(y0) exact:", float(p1), " P''(y0) exact:", float(p2))
print("preview -P'/P:", float(-p1 / p0), " P''/P:", float(p2 / p0))
# central differences in float as the lab does (h = 1e-5 for P, 1e-4 for P')
def cd(f, y, h):
    return (f(y + h) - f(y - h)) / (2 * h)
fd1 = cd(lambda y: float(P(F(y))), 0.04, 1e-5)
print("central diff P' float:", fd1, " diff from exact:", abs(float(p1) - fd1))

def taylor1(dy):
    return p0 + p1 * dy
def taylor2(dy):
    return p0 + p1 * dy + p2 * dy * dy / 2

for dy in [F(1, 100), F(5, 1000), F(25, 10000)]:
    e1 = P(y0 + dy) - taylor1(dy)
    e2 = P(y0 + dy) - taylor2(dy)
    print("dy", float(dy), "first-order err", float(e1), "second-order err", float(e2))
for dy in [F(-1, 100)]:
    print("dy", float(dy), "exact", float(P(y0 + dy)), "second-order", float(taylor2(dy)), "exact-minus-2nd", float(P(y0 + dy) - taylor2(dy)))
# the lab's exact price at +0.01 and -0.01 (exact rational P at 0.05 and 0.03)
for dy in [F(1, 100), F(-1, 100)]:
    ex = P(y0 + dy)
    ap = taylor2(dy)
    print("shift", float(dy), "exact cents", float(ex), "exact rounded", int(Decimal(float(ex)).quantize(Decimal(1), rounding=ROUND_HALF_EVEN)), "2nd-order", float(ap), "diff", float(ex - ap))
# ratios of errors (first order at 0.01/0.005/0.0025, second order)
def err1(dy): return float(P(y0 + dy) - taylor1(dy))
def err2(dy): return float(P(y0 + dy) - taylor2(dy))
ds = [F(1, 100), F(5, 1000), F(25, 10000)]
print("first-order ratios:", err1(ds[0]) / err1(ds[1]), err1(ds[1]) / err1(ds[2]))
print("second-order ratios:", err2(ds[0]) / err2(ds[1]), err2(ds[1]) / err2(ds[2]))
# float offset 0.04 + 0.01 vs 1/20
fl = 0.04 + 0.01
print("0.04+0.01 == 0.05:", fl == 0.05, " offset:", float(F(fl) - F(1, 20)))
print("P at float 0.05 move from 0.04+0.01 vs 1/20 (cents):", float(P(F(fl)) - P(F(1, 20))))
# two-cash-flow quiz: c1=-1, c2=1000, y=0.04, P'(y) = -sum t c_t (1+y)^(-t-1)
y = F(4, 100)
cc = {1: F(-1), 2: F(1000)}
print("two-cf P'(0.04):", float(-sum(t * cc[t] / (1 + y) ** (t + 1) for t in cc)))
# M1 price: 50/1.05 + 1050/1.05^2
print("M1 price:", float(F(50) / F(105, 100) + F(1050) / F(105, 100) ** 2))
