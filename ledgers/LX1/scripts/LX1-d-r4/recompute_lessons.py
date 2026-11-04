"""Independent exact recomputation of numbers quoted by cards c002-c013, c024, c025, c034, c037-c039, c046, c061, c066, c067."""
import math
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP


def rhu(x):
    return int(math.floor(x + F(1, 2)))


# L01
d1, r, g = F(400), F(9, 100), F(3, 100)
F0 = d1 / (r - g)
print("c012/c002 F0 exact", F0, float(F0), "rounded", rhu(F0))
pv = F(400) / (1 + r)
print("c012 PV single dividend exact", pv, float(pv), rhu(pv), " 40000/109 =", F(40000, 109), float(F(40000, 109)))
q = (1 + g) / (1 + r)
print("c003/c004 q", q, float(q), 0 < q < 1)
for N in (10, 60, 200):
    S = sum(d1 * (1 + g) ** (s - 1) / (1 + r) ** s for s in range(1, N + 1))
    print("N", N, "identity", S == F0 * (1 - q**N))
# c005 / c013 : g>=r, r>-1 ; sums grow
r2, g2 = F(5, 100), F(5, 100)
print("c005 q at g=r:", (1 + g2) / (1 + r2))
# c011 witness
for gg in (F(1, 100), F(3, 100)):
    fb = d1 / (r - gg)
    print("c011 g", gg, "F0", float(fb), "price 6000 gap", 6000 - float(fb))
# c009/c010 from seeded draws reproduced by lab; checked via lab outputs elsewhere
# L01 Mechanics for context: 250, r=.10,g=.04
print("L01 mech1 F0", F(250) / (F(10, 100) - F(4, 100)), rhu(F(250) / (F(10, 100) - F(4, 100))))

# L02 real values from lab's printed index (exact fractions the lab uses)
# Recompute path independently with the same seed-free printed changes
changes = [-1, 1, 1, 3, -4, -1, 2, -4, -3, 3, 2, -4]
P = [F(100)]
for c in changes:
    P.append(P[-1] * (1 + F(c, 100)))
V = [F(1_000_000) * F(100) / p for p in P]
cents = [rhu(v) for v in V]
print("c024 cents", cents)
print("c024 each differs from predecessor:", all(cents[t] != cents[t - 1] for t in range(1, 13)), "exact all differ:", all(V[t] != V[t - 1] for t in range(1, 13)))
print("c025 identity all t:", all(V[t] / V[t - 1] == P[t - 1] / P[t] for t in range(1, 13)))
falls = [t for t in range(1, 13) if P[t] < P[t - 1]]
rises = [t for t in range(1, 13) if V[t] > V[t - 1]]
print("c066 falls", falls, len(falls), "rises", rises, len(rises), "equal", falls == rises)
print("P12 unrounded", float(P[12]), "V12/V0", float(V[12] / V[0]))
print("c024 changes in P each period nonzero:", all(P[t] != P[t - 1] for t in range(1, 13)))
# M1 L02 for context
print("L02 M1", F(2000) * 100 / 80)

# L03 depths
D = 1_000_000
N0 = 4_000_000
delta = F(1, 50)
H = 12
phi = F(1)
beta = F(1)


def depth(m, phi=F(1), beta=F(1)):
    L0 = F(D) / N0
    best = None
    arg = None
    for t in range(H + 1):
        P = (1 - delta) ** min(t, m)
        V = F(D) / P
        N = N0 - (V - D)
        L = V / N
        ft = beta * phi * (L - L0)
        if best is None or ft > best:
            best, arg = ft, t
    return best, arg


dx, tx = depth(12)
dy, ty = depth(4)
print("c037 X depth %", float(100 * dx), "first t", tx)
print("c038 Y depth %", float(100 * dy), "first t", ty)
print("c039/c067 ratio", float(dx / dy), "ratio products", [float(depth(12, p, b)[0] / depth(4, p, b)[0]) for p, b in ((F(1, 2), F(1)), (F(1), F(1)), (F(3), F(1)))])
print("E2 diff unrounded", float(100 * (dx - dy)))
print("c046 beta=2 depth X %", float(100 * depth(12, F(1), F(2))[0]))
# closed form check
Vm = F(D) / (1 - delta) ** 12
C = N0 + D
ell = lambda x: x / (C - x)
print("Prop 3.2(b) closed form X %", float(100 * (ell(Vm) - ell(F(D))))  )
print("c012 PV 40000/109 rounds", rhu(F(40000, 109)))
print("c034 depth(0):", depth(0)[0])
print("c035 deeper X Y:", dx > dy)
print("c041/L03 m=4 exact V4", float(F(D) / (1 - delta) ** 4), "L4", float((F(D) / (1 - delta) ** 4) / (N0 + D - F(D) / (1 - delta) ** 4)))
