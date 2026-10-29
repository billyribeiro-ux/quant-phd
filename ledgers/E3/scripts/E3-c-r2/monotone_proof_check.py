"""Numerical check of the closed-form derivative used in the proposed monotonicity proof for omega_{1/2}.

With s = sqrt(p), omega = s / D(s), D(s) = 1 + 2 s sqrt(1 - s^2). Then d omega/ds = (D - s D') / D^2 and
D - s D' = (sqrt(1 - s^2) + 2 s^3) / sqrt(1 - s^2). Check both identities at many s in (0, 1), and the sign."""
import math
worst_id = 0.0
worst_sign = float("inf")
for i in range(1, 100000):
    s = i / 100000
    r = math.sqrt(1 - s * s)
    D = 1 + 2 * s * r
    Dp = 2 * (r - s * s / r)            # dD/ds = 2 (sqrt(1-s^2) - s^2 / sqrt(1-s^2))
    lhs = D - s * Dp
    rhs = (r + 2 * s**3) / r
    worst_id = max(worst_id, abs(lhs - rhs))
    worst_sign = min(worst_sign, lhs)
print("max |D - sD' - (sqrt(1-s^2)+2s^3)/sqrt(1-s^2)| over 99999 points:", worst_id)
print("minimum of D - sD' (positive means omega increasing in s):", worst_sign)
