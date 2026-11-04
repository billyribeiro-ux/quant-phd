# Independent re-derivation of the L03 numbers in exact Fractions. Imports nothing from the twin.
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP
import math

def rhu(x, places):
    q = Decimal(1).scaleb(-places)
    return Decimal(x.numerator) / Decimal(x.denominator) if False else None

def half_up(x: F, places: int) -> str:
    # exact half-up rounding of a non-negative Fraction to `places` decimals
    scaled = x * 10**places
    n = math.floor(scaled + F(1, 2))
    whole, frac = divmod(n, 10**places)
    return f"{whole}.{frac:0{places}d}"

def half_up_int(x: F) -> int:
    return math.floor(x + F(1, 2))

D, N0, DELTA, H = 1_000_000, 4_000_000, F(1, 50), 12
C = N0 + D

def P(m, t): return (1 - DELTA) ** min(t, m)
def V(m, t): return F(D) / P(m, t)
def L(m, t):
    v = V(m, t); n = N0 - (v - D); assert n > 0; return v / n
L0 = F(D, N0)
assert L(0, 0) == L0
def f(m, t): return L(m, t) - L0          # phi = beta = 1
def depth(m): return max(f(m, t) for t in range(H + 1))
def first(m):
    top = depth(m); return next(t for t in range(H + 1) if f(m, t) == top)

print("L0", half_up(L0, 4))
for name, m in (("X", 12), ("Y", 4)):
    print("economy", name)
    for t in range(H + 1):
        print(f"  t={t:2d} index {half_up(P(m,t),4)} debt {half_up_int(V(m,t))} lev {half_up(L(m,t),4)} prem {half_up(f(m,t),4)} fall {half_up(100*f(m,t),2)}")
print("depth X %", half_up(100*depth(12), 2), "t", first(12), "exact", float(100*depth(12)))
print("depth Y %", half_up(100*depth(4), 2), "t", first(4), "exact", float(100*depth(4)))
print("X-Y unrounded %", float(100*(depth(12)-depth(4))), half_up(100*(depth(12)-depth(4)), 2))
print("rounded difference of printed", F(902,100)-F(269,100))
print("ratio X/Y", float(depth(12)/depth(4)), half_up(depth(12)/depth(4), 4))
for m in range(13):
    print("m", m, "depth%", half_up(100*depth(m), 2))
print("never falls", all(depth(m) <= depth(m+1) for m in range(12)), "strict", all(depth(m) < depth(m+1) for m in range(12)))
# closed form (b) at t=m equals path value
for m in (4, 12):
    closed = (F(D)*(1-DELTA)**(-m)) / (C - F(D)*(1-DELTA)**(-m)) - F(D, N0)
    print("closed form", m, closed == depth(m), float(closed))
# Corollary 3.4 ratio for several products
for phi, beta in ((F(1,2),F(1)),(F(1),F(1)),(F(3),F(1)),(F(7,3),F(5,2))):
    print("ratio phi,beta", phi, beta, half_up(depth(12)/depth(4), 4))
# M1-M3
P4 = (F(49, 50)) ** 4
print("P4", P4, float(P4), "V4", float(F(D)/P4), half_up_int(F(D)/P4))
V4 = F(D)/P4
N4 = N0 - (V4 - D)
print("N4", float(N4), half_up_int(N4), "L4", float(V4/N4), half_up(V4/N4, 4))
print("V4 round-first N4", N0 - (half_up_int(V4) - D), "L4 round-first", half_up_int(V4)/ (N0 - (half_up_int(V4)-D)))
print("V12", float(V(12,12)), half_up_int(V(12,12)))
print("E1 Y depth exact %", float(100*depth(4)))
print("E3 Y indices unchanged periods", sum(1 for t in range(5,13) if P(4,t)==P(4,t-1)), "count of t in 1..12 unchanged", sum(1 for t in range(1,13) if P(4,t)==P(4,t-1)))
print("Part A baseline t=0 premium 0")
print("Remark 4.2 V_m < N0+D", V(12,12) < N0 + D, float(V(12,12)))
print("A monotone closed form path max at t=m", all(f(12,t) <= f(12,12) for t in range(13)))
