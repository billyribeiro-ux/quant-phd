"""Independent re-derivation of the numbers in cards.json (LX1-d round 8). Stdlib only, exact where possible."""
import csv, math, sys
from fractions import Fraction as Fr
from decimal import Decimal, ROUND_HALF_UP

def hu(x):  # half-up to whole number for Fraction
    return math.floor(x + Fr(1, 2))

# L01 Theorem 1.3 / Prop 2.2 / Remark 1.3 numbers
d1, r, g = 400, Fr(9, 100), Fr(3, 100)
F0 = Fr(d1) / (r - g)
print("F0 =", F0, float(F0), "rounded", hu(F0))
q = (1 + g) / (1 + r)
print("q =", q, float(q), "0<q<1", 0 < q < 1)
print("F2 =", float(Fr(d1) * (1 + g) ** 2 / (r - g)), "rounded", hu(Fr(d1) * (1 + g) ** 2 / (r - g)))
print("PV of single 400 at 9% =", Fr(400) / (1 + r), "=", float(Fr(400) / (1 + r)), "rounded", hu(Fr(400) / (1 + r)))
print("F0(1%) =", Fr(400) / (Fr(9, 100) - Fr(1, 100)), " F0(3%) =", float(Fr(400) / (Fr(9, 100) - Fr(3, 100))))
print("gaps at 6000:", Fr(6000) - Fr(400) / (Fr(9, 100) - Fr(1, 100)), float(Fr(6000) - Fr(400) / (Fr(9, 100) - Fr(3, 100))))
print("g* at P0=6000:", Fr(9, 100) - Fr(400, 6000), float(Fr(9, 100) - Fr(400, 6000)))
# S_N identity exact
for N in (1, 10, 60, 200):
    S = sum(Fr(d1) * (1 + g) ** (s - 1) / (1 + r) ** s for s in range(1, N + 1))
    print("N", N, "identity", S == F0 * (1 - q ** N))

# L01 Lab 1 Part B (seeded) - re-derive with the lab's own seed and rule, independently
import random
rng = random.Random(20261103)
fund = lambda t, gg: Fr(d1) * (1 + gg) ** t / (r - gg)
wedges = [Fr(rng.randint(-8, 25), 100) for _ in range(13)]
pos3 = sum(1 for t in range(13) if hu(fund(t, g) * (1 + wedges[t])) - hu(fund(t, g)) > 0)
rng2 = random.Random(20261103)
w2 = [Fr(rng2.randint(-8, 25), 100) for _ in range(13)]
pos1 = sum(1 for t in range(13) if hu(fund(t, g) * (1 + w2[t])) - hu(fund(t, Fr(1, 100))) > 0)
print("Lab1 L01 positive periods 3%:", pos3, "of 13; 1%:", pos1, "of 13")

# L03 model depths with phi = beta = 1
D, N0 = 1_000_000, 4_000_000
delta = Fr(1, 50)
def depth(m, phi=Fr(1), beta=Fr(1), H=12):
    def V(t):
        return Fr(D) / (1 - delta) ** min(t, m)
    def L(t):
        Vt = V(t); Nt = N0 - (Vt - D); return Vt / Nt
    L0 = Fr(D, N0)
    return max(beta * phi * (L(t) - L0) for t in range(H + 1))
dX, dY = depth(12), depth(4)
print("depth X =", float(100 * dX), "Y =", float(100 * dY), "diff pp", float(100 * (dX - dY)))
print("ratio X/Y =", float(dX / dY), "exact", dX / dY)
for phi, beta in ((Fr(1, 2), Fr(1)), (Fr(1), Fr(1)), (Fr(3), Fr(1))):
    print("ratio at phi,beta", phi, beta, float(depth(12, phi, beta) / depth(4, phi, beta)))
print("V12 exact", float(Fr(D) / (1 - delta) ** 12), "rounded", hu(Fr(D) / (1 - delta) ** 12))
print("P4 exact", (1 - delta) ** 4, "V4 exact", float(Fr(D) / (1 - delta) ** 4))
print("depth(12) first-attained t: uniqueness check not needed")
print("ln 1.1 =", math.log(1.1), "simple-log", 0.1 - math.log(1.1))
