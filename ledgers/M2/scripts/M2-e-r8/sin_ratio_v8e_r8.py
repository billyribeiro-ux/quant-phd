import math, sys
from fractions import Fraction
sys.path.insert(0, "course/modules/M/M2/grader")
from instance import make_instance
def cen(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)
lo, hi = None, None
lo_x = hi_x = None
for seed in range(50):
    for s in (seed, seed + 7919):
        inst = make_instance(s)
        x0 = inst["x0"]
        exact = math.cos(x0)
        e1 = abs(cen(math.sin, x0, 1e-2) - exact)
        e2 = abs(cen(math.sin, x0, 5e-3) - exact)
        r = e1 / e2
        if lo is None or r < lo: lo, lo_x = r, (s, x0)
        if hi is None or r > hi: hi, hi_x = r, (s, x0)
print("float-quotient ratio min %.9f at %s, max %.9f at %s" % (lo, lo_x, hi, hi_x))
print("rounded 7dp: min %.7f max %.7f" % (lo, hi))
