"""Extra numeric checks for L04 E2 (normal quantile) and L06 displayed values; verifier's own code.
Run: python3 -I extra_checks.py
"""
from statistics import NormalDist
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP
print("z(0.975) =", NormalDist().inv_cdf(0.975))
print("z(0.975) to 6 dp =", round(NormalDist().inv_cdf(0.975), 6))
print("sqrt(0.25/20) =", (0.25 / 20) ** 0.5, " z =", (0.65 - 0.5) / (0.25 / 20) ** 0.5)
# Degenerate point range check for L06 Corollary 3.3: NPV(u) = mA(u - u*) with u* = 399300/331
ustar = F(399300, 331)
for ell, h in ((ustar, ustar), (ustar, ustar + 1), (ustar - 1, ustar)):
    vals = [ (u - ustar) for u in (ell, h)]
    print("range", float(ell), float(h), "sign of (u-u*) at ends:", [(v > 0) - (v < 0) for v in vals])
# check that a point range with l=h=u* is admissible under Prop 3.2 (one factor, l=h=u*)
print("point factor range admissible: 0 < l <= h with l = h =", float(ustar))
