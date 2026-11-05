"""Independent recomputation of the L03 model numbers (closed form of Proposition 3.2(b)); run as python3 -I.

Usage: python3 -I indep_L03.py
Prints exact values rounded half up only for display, plus the cross-checks named in the output.
"""
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

D = F(1_000_000)
N0 = F(4_000_000)
C = N0 + D
d = F(1, 50)


def ell(x):
    return x / (C - x)


def rhu(x, places):
    q = Decimal(1).scaleb(-places)
    v = (Decimal(x.numerator) / Decimal(x.denominator))
    return v.quantize(q, rounding=ROUND_HALF_UP)


def V(m, t):
    return D * (1 - d) ** (-min(t, m))


def depth_closed(m):
    # Proposition 3.2(b) with phi = beta = 1
    return ell(V(m, m)) - ell(D)


def depth_path_max(m):
    # brute-force path maximum from the model definition, phi = beta = 1
    best = None
    for t in range(13):
        Vt = V(m, t)
        Nt = N0 - (Vt - D)
        Lt = Vt / Nt
        L0 = D / N0
        ft = Lt - L0
        best = ft if best is None or ft > best else best
    return best


dX_cf, dY_cf = depth_closed(12), depth_closed(4)
dX_bf, dY_bf = depth_path_max(12), depth_path_max(4)
print("closed form == path max (X):", dX_cf == dX_bf)
print("closed form == path max (Y):", dY_cf == dY_bf)
print("depth X exact (float)", float(dX_cf))
print("depth Y exact (float)", float(dY_cf))
print("depth X shown 2dp (percent):", rhu(100 * dX_cf, 2))
print("depth Y shown 2dp (percent):", rhu(100 * dY_cf, 2))
print("difference X minus Y exact percentage points (float):", float(100 * (dX_cf - dY_cf)))
print("difference shown 2dp:", rhu(100 * (dX_cf - dY_cf), 2))
print("difference of the shown values 9.20 - 2.69 =", F("9.20") - F("2.69"))
print("ratio X/Y exact (float):", float(dX_cf / dY_cf), "shown 4dp:", rhu(dX_cf / dY_cf, 4))
for m in range(13):
    print("m =", m, "depth percent 2dp", rhu(100 * depth_closed(m), 2))
print("V_12 exact cents (float):", float(V(12, 12)), "rounded", rhu(V(12, 12), 0))
print("V_4 exact cents rounded", rhu(V(4, 4), 0))
print("leverage L12 exact float", float(V(12, 12) / (N0 - (V(12, 12) - D))))
print("ratio alt cutoffs phi=1/2 vs 3 identical:", depth_closed(12) / depth_closed(4))
