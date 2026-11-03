# Independent recomputation (does not import the lab twins).
import math
from fractions import Fraction as Fr
from decimal import Decimal, getcontext

getcontext().prec = 60

# L24 E3: unrounded central-quotient errors at h = 1e-5 and 1e-7 (float arithmetic, no print rounding)
def central(h):
    return (math.exp(1.0 + h) - math.exp(1.0 - h)) / (2.0 * h)
for k in (5, 7, 6, 4):
    h = 10.0 ** -k
    c = central(h)
    print("k", k, "h", repr(h), "central", repr(c), "err vs math.e", repr(abs(c - math.e)))
e5 = abs(central(10.0 ** -5) - math.e)
e7 = abs(central(10.0 ** -7) - math.e)
print("E3 errors 1e-5 %.9e 1e-7 %.9e diff %.6e  diff/ulp(e)=%.4f" % (e5, e7, abs(e5 - e7), abs(e5 - e7) / 2**-51))
print("ulp(e) =", math.ulp(math.e), " half ulp(e) =", math.ulp(math.e) / 2)
print("delta = 2.22e-16 ; 2 sqrt(delta/e) =", 2 * math.sqrt(2.22e-16 / math.e), " (3 delta/e)^(1/3) =", (3 * 2.22e-16 / math.e) ** (1 / 3))
print("E2 bound 2 delta / 1e-15 =", 2 * 2.22e-16 / 1e-15, " 1/2 e h at 1e-5 =", 0.5 * math.e * 1e-5)
print("predicted forward minimiser decade: log10(1.8e-8)=", math.log10(1.8e-8), " log10(6.3e-6)=", math.log10(6.3e-6))
print("ratio 4.531e-9/5.859e-11 =", 4.531e-9 / 5.859e-11)

# L23: exact price, derivatives and expansion errors at base yield 0.04 (Decimal, 60 digits, from the formulas)
def cf(t):
    return 5000 + (100000 if t == 10 else 0)
def P_dec(y):
    v = Decimal(1) + Decimal(y)
    return sum(Decimal(cf(t)) / v ** t for t in range(1, 11))
def P1_dec(y):
    v = Decimal(1) + Decimal(y)
    return sum(-t * Decimal(cf(t)) / v ** (t + 1) for t in range(1, 11))
def P2_dec(y):
    v = Decimal(1) + Decimal(y)
    return sum(t * (t + 1) * Decimal(cf(t)) / v ** (t + 2) for t in range(1, 11))
y0 = Decimal("0.04")
print("P(0.04) =", P_dec(y0))
print("P'(0.04) =", P1_dec(y0), " P''(0.04) =", P2_dec(y0))
print("-P'/P =", -P1_dec(y0) / P_dec(y0), " P''/P =", P2_dec(y0) / P_dec(y0))
for dy in ("0.01", "-0.01"):
    y = y0 + Decimal(dy)
    exact = P_dec(y)
    approx2 = P_dec(y0) + P1_dec(y0) * Decimal(dy) + Decimal("0.5") * P2_dec(y0) * Decimal(dy) ** 2
    print("shift", dy, "exact", exact, "second-order", approx2, "unrounded error exact-approx", exact - approx2)
# first-order error at shift 0.01 (for ratio sanity)
dy = Decimal("0.01")
print("first-order error at +0.01 =", P_dec(y0 + dy) - (P_dec(y0) + P1_dec(y0) * dy))
# E3: float yield 0.04 + 0.01 vs 0.05
yf = 0.04 + 0.01
print("float 0.04+0.01 =", repr(yf), " offset from 0.05 =", Decimal(yf) - Decimal("0.05"))
print("P'(0.05) =", P1_dec(Decimal("0.05")), " effect on price of offset =", P1_dec(Decimal("0.05")) * (Decimal(yf) - Decimal("0.05")))
print("P(float 0.05) - 100000 =", P_dec(Decimal(yf)) - 100000)
# card example: two cash flows c1=-1, c2=1000, N=2, y=0.04
y = Decimal("0.04")
pp = -(1 * Decimal(-1) / (1 + y) ** 2 + 2 * Decimal(1000) / (1 + y) ** 3)
print("two-cash-flow P'(0.04) =", pp)
# M1 of L23: 1000 face, 5% coupon, 2 years, yield 5%
print("L23 M1 direct:", Decimal(50) / Decimal("1.05") + Decimal(1050) / Decimal("1.05") ** 2)
print("L23 M3 P'(0.04) zero-coupon 100 at year2:", -200 / Decimal("1.04") ** 3)
