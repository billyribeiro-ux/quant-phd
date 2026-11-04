# Independent check of L24 numbers: exact (mpmath-free, Decimal 80 digits) and float signed errors.
import math
from decimal import Decimal, getcontext
getcontext().prec = 80
E = Decimal(1).exp()           # e to 80 digits
ef = math.e                    # float e used by the lab
def exp_d(x):  # Decimal exp
    return Decimal(x).exp()
print("float e =", repr(ef), "  e exact =", str(E)[:20])
for k in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15):
    h = 10.0 ** -k
    fwd = (math.exp(1.0 + h) - math.exp(1.0)) / h
    cen = (math.exp(1.0 + h) - math.exp(1.0 - h)) / (2.0 * h)
    # signed float errors vs the float e (as the lab does) and vs exact e
    print(f"k={k:2d} h={h:.0e} signed fwd err vs float e {fwd - ef: .6e}  signed cen err vs float e {cen - ef: .6e}")
# exact truncation errors via Decimal (exact e^{1+h} etc at 80 digits)
for k in (1, 3, 4, 5, 6, 7, 8, 9):
    h = Decimal(10) ** -k
    ex_fwd = (exp_d(1 + h) - E) / h          # exact forward quotient, exact function
    ex_cen = (exp_d(1 + h) - exp_d(1 - h)) / (2 * h)
    print(f"k={k} exact fwd err {float(ex_fwd - E):+.6e}  exact cen err {float(ex_cen - E):+.6e}  e*h/2={float(E*h/2):.6e} e*h^2/6={float(E*h*h/6):.6e}")
# e(sinh h / h - 1) check
h = Decimal(10) ** -5
print("central exact via sinh form at 1e-5:", float(E * ((exp_d(h) - exp_d(-h)) / (2 * h) - 1)))
# ulp of e
print("float ulp at e:", math.ulp(ef), " half ulp:", math.ulp(ef) / 2)
print("sqrt(delta/e)*2 with delta=half ulp:", 2 * math.sqrt((math.ulp(ef)/2) / ef))
print("(3 delta/e)^(1/3):", (3 * (math.ulp(ef)/2) / ef) ** (1/3))
# exact D+ error at h=1e-8 and the lab's signed computed error
for k in (8, 9):
    h = 10.0 ** -k
    print("k", k, "float fwd signed err", (math.exp(1.0 + h) - math.exp(1.0)) / h - ef)
# Decimal exact central at 1e-5 minus float e
print("central 1e-5 computed signed err vs float e:", (math.exp(1+1e-5)-math.exp(1-1e-5))/(2e-5) - ef)
print("float exp(1-1e-5), exp(1+1e-5):", repr(math.exp(1-1e-5)), repr(math.exp(1+1e-5)))
# grid spacing of quotient numerator at 1e-5 and 1e-7: ulp(e)/(2h)
for k in (5, 7):
    h = 10.0**-k
    print("k", k, "quotient grid spacing ulp(e)/(2h) =", math.ulp(ef) / (2*h))
# unrounded central at 1e-5 and 1e-7 (float arithmetic, no print rounding)
c5 = (math.exp(1+1e-5)-math.exp(1-1e-5))/(2e-5)
c7 = (math.exp(1+1e-7)-math.exp(1-1e-7))/(2e-7)
print("unrounded c5 err", abs(c5-ef), " c7 err", abs(c7-ef), " diff", abs(abs(c5-ef)-abs(c7-ef)))
print("unrounded errors (repr)", repr(abs(c5-ef)), repr(abs(c7-ef)))
