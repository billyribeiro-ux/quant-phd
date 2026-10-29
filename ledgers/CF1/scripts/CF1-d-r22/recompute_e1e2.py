import math
from statistics import NormalDist
d = 84543.40 - 79078.68
print("error_cents", round(d, 2))
z = d / 4400.22
print("z_unrounded", z, "z_4dp", round(z, 4))
Phi = NormalDist().cdf
print("two_sided_tail_at_1.2419", 2 * (1 - Phi(1.2419)), "at_unrounded", 2 * (1 - Phi(z)))
lo, hi = 0.0552 - 1.96 * 0.0010, 0.0552 + 1.96 * 0.0010
print("E2_band", round(lo, 5), round(hi, 5))
print("E2 p unrounded", 2761 / 50000, "se", math.sqrt((2761/50000)*(1-2761/50000)/50000))
