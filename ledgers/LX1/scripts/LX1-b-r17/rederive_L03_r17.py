"""Independent re-derivation of the L03 model numbers (LX1-b round 17). Exact Fractions and Decimal only."""
from fractions import Fraction as F
from decimal import Decimal, getcontext, ROUND_HALF_UP
getcontext().prec = 50

D = F(1_000_000)
K0 = F(4_000_000)
C = K0 + D
DELTA = F(1, 50)
H = 12

def P(m, t):
    return (1 - DELTA) ** min(t, m)

def V(m, t):
    return D / P(m, t)

def lam(x):
    return x / (C - x)

L0 = lam(D)

def depth_path(m):
    return [lam(V(m, t)) - L0 for t in range(H + 1)]  # phi = beta = 1

def dec(x, places=6):
    return Decimal(x.numerator) / Decimal(x.denominator)

def rnd(x, places):
    q = Decimal(1).scaleb(-places)
    return dec(x).quantize(q, rounding=ROUND_HALF_UP)

print("P_12 exact decimal:", dec(P(12, 12), 20), "rounded 4dp:", rnd(P(12, 12), 4))
print("P_4 exact:", P(4, 4), "=", dec(P(4, 4), 12))
print("V_4 X/Y:", dec(V(4, 4), 8), "rounded cents:", rnd(V(4, 4), 0))
print("V_12:", dec(V(12, 12), 10), "rounded cents:", rnd(V(12, 12), 0))
for m in (4, 12):
    print(f"m={m} leverage t=4:", dec(lam(V(m, 4)), 10))
print("L_4 exact (economy Y) 4dp:", rnd(lam(V(4, 4)), 4), " exact:", dec(lam(V(4, 4)), 10))
print("K_4 exact:", dec(K0 - (V(4, 4) - D), 6))
print("K_4 L_4 via K:", dec(V(4, 4) / (K0 - (V(4, 4) - D)), 10))
dX = max(depth_path(12)); dY = max(depth_path(4))
print("depth X exact:", dec(dX, 10), "pct 2dp:", rnd(100 * dX, 2))
print("depth Y exact:", dec(dY, 10), "pct 2dp:", rnd(100 * dY, 2), " pct 4dp:", rnd(100*dY, 4))
print("difference exact pct:", dec(100 * (dX - dY), 6), "rounded 2dp:", rnd(100 * (dX - dY), 2))
print("ratio X/Y:", dec(dX / dY, 10), "rounded 4dp:", rnd(dX / dY, 4))
print("ratio X/Y invariance check (phi,beta) product:", [dec(F(a)*dX/(F(a)*dY),8) for a in (F(1,2), 1, 3)])
print("X depth first at:", [t for t, v in enumerate(depth_path(12)) if v == dX][:1])
print("Y depth first at:", [t for t, v in enumerate(depth_path(4)) if v == dY][:1])
dep = [max(depth_path(m)) for m in range(H + 1)]
print("never falls:", all(dep[m] <= dep[m+1] for m in range(H)), " strict:", all(dep[m] < dep[m+1] for m in range(H)))
print("Part C rounded pct:", [str(rnd(100*d, 2)) for d in dep])
print("Y index unchanged periods t=1..12:", sum(1 for t in range(1, 13) if P(4, t) == P(4, t-1)))
print("Y index 4dp t=0..12:", [str(rnd(P(4, t), 4)) for t in range(13)])
print("X index 4dp t=0..12:", [str(rnd(P(12, t), 4)) for t in range(13)])
print("X V_t cents:", [int(rnd(V(12, t), 0)) for t in range(13)])
print("X leverage 4dp:", [str(rnd(lam(V(12, t)), 4)) for t in range(13)])
print("X premium 4dp:", [str(rnd(lam(V(12, t)) - L0, 4)) for t in range(13)])
print("Y leverage 4dp:", [str(rnd(lam(V(4, t)), 4)) for t in range(13)])
