"""M2-d2 r10: L24 Proposition 3.1 example at x=2 (M3 solution, L24.html:298) and L23 zero-coupon derivative check."""
from fractions import Fraction as F
fwd = (F(21, 10) ** 3 - 2 ** 3) / F(1, 10)
print("forward quotient D+_h f(2) =", float(fwd), "error", float(fwd - 12))
M2 = 6 * 2.1  # sup |6x| on [2, 2.1] is attained at x = 2.1
print("sup |f''| on [2,2.1] =", M2, " bound 1/2 M2 h =", 0.5 * 12.6 * 0.1)
print("actual error 0.61 <= 0.63:", float(fwd - 12) <= 0.5 * 12.6 * 0.1)
