"""Limit of Proposition 3.5 and its comparison with d/rho, exact (FC1 slice c, round 12).

Shows the two hypothesis gaps: d < 0 breaks 'at most d/rho'; d = 0 makes equality hold with phi != 1 and rho != 1.
"""
from fractions import Fraction as F

cases = [(-1, 0, F(1, 2)), (0, 0, F(1, 2)), (1, 0, F(1, 2)), (1, 1, F(1, 2)), (1, F(1, 2), 1)]
for d, phi, rho in cases:
    limit = F(d) / (1 - F(phi) * (1 - F(rho)))
    bound = F(d) / F(rho)
    print(f"d={d} phi={phi} rho={rho}: limit={limit} d/rho={bound} at_most={limit <= bound} equal={limit == bound}")
