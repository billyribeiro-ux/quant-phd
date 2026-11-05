"""Independent recomputation of the L03 model numbers (LX1-b round 7). Uses exact Fractions and mpmath-free float checks."""
from fractions import Fraction as F
import math
D = F(1_000_000); N0 = F(4_000_000); C = N0 + D; d = F(1, 50); H = 12
def V(m, t): return D / (1 - d) ** min(t, m)
def ell(x): return x / (C - x)
def f(m, t, phi=F(1), beta=F(1)): return beta * phi * (ell(V(m, t)) - ell(D))
def depth(m, phi=F(1), beta=F(1)): return max(f(m, t, phi, beta) for t in range(H + 1))
def first(m):
    top = depth(m); return next(t for t in range(H + 1) if f(m, t) == top)
def r2(x, places):  # half-up rounding of a non-negative Fraction
    s = math.floor(x * 10**places + F(1, 2)); return s / 10**places
print("V_12 exact:", float(V(12, 12)), " whole-cent round:", math.floor(V(12, 12) + F(1, 2)))
print("V_4 exact:", float(V(4, 4)))
print("L0:", float(ell(D)))
for m in (12, 4):
    print(f"economy m={m}")
    for t in range(H + 1):
        Vt = V(m, t); lev = Vt / (C - Vt); psi = ell(Vt) - ell(D)
        print(f"  t={t:2d} index={float((1-d)**min(t,m)):.6f} V={math.floor(Vt+F(1,2))} lev={float(lev):.6f} psi={float(psi):.6f} fall%={float(100*psi):.6f}")
dx, dy = depth(12), depth(4)
print("depth X %:", float(100 * dx), " first t:", first(12))
print("depth Y %:", float(100 * dy), " first t:", first(4))
print("X-Y unrounded pp:", float(100 * (dx - dy)))
print("printed diff:", float(r2(100*dx,2) - r2(100*dy,2)))
print("ratio X/Y (phi=beta=1):", float(dx / dy))
for phi in (F(1, 2), F(1), F(3)):
    print("ratio with phi", phi, float(depth(12, phi) / depth(4, phi)))
print("depth Corollary 3.4 equivalence check:", all(depth(m) <= depth(m + 1) for m in range(H)), all(depth(m) < depth(m+1) for m in range(H)))
print("closed form (b) check m=12:", float(F(1) * (V(12,12) / (N0 + D - V(12,12)) - D / N0)), " depth:", float(depth(12)))
print("(b) check m=4:", float(V(4,4) / (N0 + D - V(4,4)) - D / N0), float(depth(4)))
print("Y depth exceeds X on quadratic premium check ratio^2:", float((dx/dy)**2))
# Quiz/Part answers
print("quiz numeric 1274345 vs V_12 round:", math.floor(V(12,12)+F(1,2)))
