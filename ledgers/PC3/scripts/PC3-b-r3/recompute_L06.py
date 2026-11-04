"""Independent recomputation of the L06 numbers (not importing the lab): forward price, case NPV and sensitivity.

Usage: python -I recompute_L06.py. Exact Fraction arithmetic; cents for money.
"""
from fractions import Fraction as F
import math

S = F(9700)
D = F(97, 100)
print("F = S/D =", S / D)
print("S - D*F at F=S/D =", S - D * (S / D))
# case
I = F(15_000_000)
m = F(5000)
lo, hi = F(200), F(1600)  # 2000*1*(1/10) and 4000*2*(1/5)
print("lower", 2000 * 1 * F(1, 10), "upper", 4000 * 2 * F(1, 5))
for r in (F(8, 100), F(10, 100), F(12, 100)):
    A = sum((1 / (1 + r) ** t for t in range(1, 4)), F(0))
    be = I / (m * A)
    npv = lambda u: -I + m * A * u
    print(f"r={float(r):.2f} A={float(A):.9f} break-even={float(be):.6f} NPV(lo)={float(npv(lo)):.4f} NPV(hi)={float(npv(hi)):.4f}")
    print("   exact NPV(lo) =", npv(lo), " exact NPV(hi) =", npv(hi))
A10 = F(3310, 1331)
print("A10 exact check", sum((1 / F(11, 10) ** t for t in range(1, 4)), F(0)) == A10)
be10 = I / (m * A10)
print("be10 exact", be10, float(be10))
