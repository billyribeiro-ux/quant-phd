from fractions import Fraction as F
from decimal import Decimal, getcontext
getcontext().prec = 50
# Lab 1 bond: face 1000000, coupon 5%, 10 years, yield 4%
def exact(face, c, T, y):
    coupon = F(face) * c
    v = 1 / (1 + y)
    P = sum((coupon + (face if t == T else 0)) * v**t for t in range(1, T + 1))
    d1 = -sum(t * (coupon + (face if t == T else 0)) * v**(t + 1) for t in range(1, T + 1))
    d2 = sum(t * (t + 1) * (coupon + (face if t == T else 0)) * v**(t + 2) for t in range(1, T + 1))
    return P, d1, d2
P, d1, d2 = exact(1_000_000, F(5, 100), 10, F(4, 100))
print("L1 price", float(P), "d1", float(d1), "d2", float(d2), "duration", float(-d1 / P))
print("L1 rel diff d1 vs float-printed", float(abs(d1 - F("-8514667.3953"))))
P3, d13, _ = exact(2_500_000, F(6, 100), 12, F(5, 100))
print("L3 price", float(P3), "rounded", round(P3), "d1", float(d13))
# half-even check on exact price
print("L3 exact d1 with 6 decimals", f"{float(d13):.6f}")
# L1 mismatch relative to analytic:
print("L1 d1 exact-minus-printed", float(d1) + 8514667.3953)
# Lab 3 central errors: float reproduction
v = 1 / 1.05
