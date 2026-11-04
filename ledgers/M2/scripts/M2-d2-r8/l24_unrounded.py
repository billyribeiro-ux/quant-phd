"""Re-derive the L24 Part B unrounded central errors at h = 1e-5 and 1e-7 and their difference (exact and float)."""
import math
from decimal import Decimal, getcontext

getcontext().prec = 60

def central(f, x, h):
    return (f(x + h) - f(x - h)) / (2.0 * h)

e = math.e
c5 = central(math.exp, 1.0, 10.0**-5)
c7 = central(math.exp, 1.0, 10.0**-7)
print("central at 1e-5 unrounded:", repr(c5), "error", repr(abs(c5 - e)))
print("central at 1e-7 unrounded:", repr(c7), "error", repr(abs(c7 - e)))
e5 = abs(c5 - e)
e7 = abs(c7 - e)
print("error difference (float):", repr(e5 - e7), "abs", repr(abs(e5 - e7)))
print("error difference in e-16 units:", (e5 - e7) / 1e-16)
# exact-decimal of the errors (exact float values)
D = Decimal
print("exact decimal of e5:", D(e5))
print("exact decimal of e7:", D(e7))
print("exact diff of errors:", D(e5) - D(e7))
print("ulp of e (float spacing near e):", math.ulp(e))
print("six-digit values from page: 5.858691e-11, 5.858736e-11 diff =", (5.858736e-11 - 5.858691e-11))
print("printed e-11 values:", f"{e5:.6e}", f"{e7:.6e}")
print("rounded printed lab values:", f"{e5:.3e}", f"{e7:.3e}")
print("sinh form at 1e-5 approx:", e * (math.sinh(1e-5)/1e-5 - 1), "at 1e-7:", e * (math.sinh(1e-7)/1e-7 - 1))
print("ulp(e)/2h at 1e-5:", math.ulp(e)/(2e-5), "at 1e-7:", math.ulp(e)/(2e-7))
