"""Recompute numbers quoted by M2 cards (Lab 1 of L23, L10, L09, L13, L24 claims) with exact fractions and floats."""
from fractions import Fraction as Fr
import math

# L23 bond: face 100000 cents, coupon 5000 per year, 10 years, face repaid at year 10
flows = [(t, 5000 + (100000 if t == 10 else 0)) for t in range(1, 11)]
def price(y):
    return sum(c * (1 + y) ** (-t) for t, c in flows)
y0 = 0.04
P0 = price(y0)
dP = -sum(t * c * (1 + y0) ** (-t - 1) for t, c in flows)
d2P = sum(t * (t + 1) * c * (1 + y0) ** (-t - 2) for t, c in flows)
print("P(0.04) = %.6f (card 108110.895779)" % P0)
print("P'(0.04) = %.6f (card -851466.739529)" % dP)
print("P''(0.04) = %.6f (card 8376648.511919)" % d2P)
print("P(0.05) = %.6f (card 100000)" % price(0.05))
print("P(0.03) = %.6f (card 117060 at shift -0.01 from 0.04 => y=0.03)" % price(0.03))
v = 1 / 1.04
P1 = P0 + dP * 0.01
print("first-order error at +0.01 = %.6e (card 4.037716e+02 is the 1st order error)" % (price(0.05) - P1))
# L10 Lab 1 part A: f = 3x^2-2 on [0,1], uniform partition, U_n-L_n = 3/n
for n in (2, 128):
    U = sum(Fr(2 * i * i + 0, 1) for i in [])  # placeholder to keep exact types
print("L10 part A: n=128 lower sum L_128 = sum (f(x_{i-1})) /n with f increasing")
n = 128
f = lambda x: 3 * x * x - 2
Ln = sum(f(Fr(i - 1, n)) for i in range(1, n + 1)) / n
Un = sum(f(Fr(i, n)) for i in range(1, n + 1)) / n
print("  L_128 = %.8f, U_128 = %.8f, U-L = %s" % (float(Ln), float(Un), Un - Ln))
