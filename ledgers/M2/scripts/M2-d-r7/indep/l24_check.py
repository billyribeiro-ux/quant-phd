# Re-derive L24 central errors for exp at 1 in IEEE double, same operations as the lab, and the unrounded gap.
import math
e = math.e
def central(f, x, h): return (f(x + h) - f(x - h)) / (2.0 * h)
for k in (4, 5, 6, 7):
    h = 10.0 ** -k
    err = abs(central(math.exp, 1.0, h) - e)
    print("k", k, "central error %.12e" % err)
from decimal import Decimal as D, getcontext
getcontext().prec = 50
print("ulp(e) = %.6e" % (math.ulp(e) if hasattr(math, "ulp") else 0))
print("e 2.22e-16/e sqrt check: 2*sqrt(delta/e)=%.4e, (3*delta/e)^(1/3)=%.4e" % (2*math.sqrt(2.22e-16/e), (3*2.22e-16/e)**(1/3)))
