"""Round 19: exact re-derivation of L03 prose numbers (Fractions). Run: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r19/rederive_L03_r19.py"""
import math
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP


def rhu(x):
    return math.floor(x + F(1, 2))


def dec(x, nd):
    q = Decimal(1).scaleb(-nd)
    return Decimal(x.numerator) / Decimal(x.denominator)


def d(x, nd):
    return float(Decimal(x.numerator) / Decimal(x.denominator)) if False else (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)


D = 1_000_000
K0 = 4_000_000
delta = F(1, 50)
phi = beta = F(1)
H = 12


def P(t, m):
    return (1 - delta) ** min(t, m)


def V(t, m):
    return D / P(t, m)


def K(t, m):
    return K0 - (V(t, m) - D)


def L(t, m):
    return V(t, m) / K(t, m)


def psi(t, m):
    return phi * (L(t, m) - F(D, K0))


def f(t, m):
    return beta * psi(t, m)


def depth(m, b=beta, p=phi):
    return max(b * p * (L(t, m) - F(D, K0)) for t in range(H + 1))


def depth_path_first(m):
    vals = [f(t, m) for t in range(H + 1)]
    mx = max(vals)
    return vals.index(mx)


print("P4 exact =", P(4, 4), float(P(4, 4)), " V4 exact =", float(V(4, 4)), "rounded", rhu(V(4, 4)))
print("(49/50)^4 =", (F(49, 50)) ** 4, " 5764801/6250000 =", F(5764801, 6250000))
print("K4 exact =", float(K(4, 4)), "rounded", rhu(K(4, 4)), " rounded-first:", K0 - (rhu(V(4, 4)) - D))
print("L4 exact =", float(L(4, 4)), "to 4dp", d(L(4, 4), 4), "rounded-first:", d(rhu(V(4, 4)) / K0 if False else F(rhu(V(4, 4)), K0 - (rhu(V(4, 4)) - D)), 4))
print("V12 exact =", float(V(12, 12)), "rounded", rhu(V(12, 12)))
print("V4 rounded:", rhu(V(4, 4)), " K4 rounded:", rhu(K(4, 4)), " M2 rounded-first gives", K0 - (rhu(V(4, 4)) - D))
print("L12 =", float(L(12, 12)), d(L(12, 12), 4))
depX = depth(12)
depY = depth(4)
print("depth X exact", float(depX), "% to 2dp", float(depX) * 100)
print("depth Y exact", float(depY), "% to 2dp", float(depY) * 100)
print("X - Y exact (pp)", float((depX - depY) * 100), "rounded 2dp", d((depX - depY) * 100, 2))
print("printed diff 9.20 - 2.69 =", F(920, 100) - F(269, 100))
print("depth(12)/depth(4) ratio =", float(depX / depY), "to 4dp", d(depX / depY, 4))
for pp in (F(1, 2), F(1), F(3)):
    bb = F(1)
    ph = pp / bb
    print(" product", pp, "ratio", float(depth(12, bb, ph) / depth(4, bb, ph)), d(depth(12, bb, ph) / depth(4, bb, ph), 4))
print("argmax X:", depth_path_first(12), " argmax Y:", depth_path_first(4))
print("Y index t=1..12:", [float(P(t, 4)) for t in range(1, 13)])
print("X depth path (5 nonzero, rounded % 2dp):", [round(float(f(t, 12)) * 100, 2) for t in range(13)])
print("Y depth path:", [round(float(f(t, 4)) * 100, 2) for t in range(13)])
print("leverage check t=4 Y:", d(L(4, 4), 4), " premium:", d(psi(4, 4), 4), " output %:", d(f(4, 4) * 100, 2))
print("monotone depth(m) m=0..12 (rounded % 2dp):", [d(depth(m) * 100, 2) for m in range(13)])
print("strictly rises m->m+1 all:", all(depth(m + 1) > depth(m) for m in range(12)))
# exact value 1,274,345.2124 cited in quiz
print("V12 to 4dp:", d(V(12, 12), 4))
# P_t values for X
print("X index at t 0..12 4dp:", [str(d(P(t, 12), 4)) for t in range(13)])
