"""Independent check of the L21 lab numbers by bisection (not Newton) and a second step size.

Usage: python -I rederive_L21.py
"""
from decimal import Decimal, getcontext

getcontext().prec = 40


def root_bisect(x: Decimal) -> Decimal:
    lo, hi = Decimal("0"), Decimal("1.5")
    for _ in range(200):
        mid = (lo + hi) / 2
        if mid**3 + x * mid - 1 > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


for xs in ("0.25", "0.5", "1.0", "2.0"):
    x = Decimal(xs)
    y = root_bisect(x)
    fy = 3 * y * y + x
    formula = -y / fy
    h = Decimal("1e-5")
    cd = (root_bisect(x + h) - root_bisect(x - h)) / (2 * h)
    cd2 = (root_bisect(x + Decimal("1e-4")) - root_bisect(x - Decimal("1e-4"))) / (2 * Decimal("1e-4"))
    print(f"x={xs} y={float(y):.10f} F_y={float(fy):.6f} formula={float(formula):.10f} "
          f"cd(1e-5)={float(cd):.10f} |diff|={float(abs(formula - cd)):.1e} cd(1e-4)-formula={float(cd2 - formula):.1e}")
