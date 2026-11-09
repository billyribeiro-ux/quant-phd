"""Round 20 independent re-derivation of LX1 L01 numbers and the Proposition 1.4 hypothesis counterexample.

Run from the checkout root: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r20/rederive_L01_r20.py
"""
from fractions import Fraction as F
import math
import random


def rnd(x):
    return math.floor(x + F(1, 2))


d1, r, g = F(400), F(9, 100), F(3, 100)
F0 = d1 / (r - g)
print("F0", F0, float(F0), rnd(F0))
q = (1 + g) / (1 + r)
print("q", q, float(q), "q exact 103/109:", q == F(103, 109))
for N in (10, 60, 200):
    S = sum(d1 * (1 + g) ** (s - 1) / (1 + r) ** s for s in range(1, N + 1))
    print("N", N, "S rounded", rnd(S), "identity", S == F0 * (1 - q ** N), "F0 q^N rounded", rnd(F0 * q ** N))
F2 = d1 * (1 + g) ** 2 / (r - g)
print("F2", float(F2), rnd(F2))
print("Mech1", float(250 / (F(10, 100) - F(4, 100))), rnd(F(250) / (F(10, 100) - F(4, 100))))
print("Mech2 F3", float(250 * (F(104, 100)) ** 3 / (F(10, 100) - F(4, 100))), rnd(F(250) * F(104, 100) ** 3 / F(6, 100)))
print("Mech3 S10 (growth 5 percent equals rate)", sum(F(100) * (1 + F(5, 100)) ** (s - 1) / F(105, 100) ** s for s in range(1, 11)), F(20000, 21))
print("Res1 g*", float(F(9, 100) - F(400, 6000)))
print("Emp3 printed ratio", float(F(2175, 8698) * 100), "unrounded fund t9", float(400 * F(103, 100) ** 9 / F(6, 100)))

# Lab Part B/C: seeded wedges, same draw order as the lab, exact arithmetic
SEED = 20261103
rng = random.Random(SEED)
wedges = [F(rng.randint(-8, 25), 100) for _ in range(13)]
fund = lambda gr, t: d1 * (1 + gr) ** t / (r - gr)
pos = 0
gaps = []
for t in range(13):
    f = rnd(fund(g, t))
    p = rnd(fund(g, t) * (1 + wedges[t]))
    gaps.append(p - f)
    pos += (p - f) > 0
print("Part B positive count", pos, "gaps", gaps, "largest", max(gaps), gaps.index(max(gaps)))
altpos = 0
for t in range(13):
    p = rnd(fund(g, t) * (1 + wedges[t]))
    a = rnd(fund(F(1, 100), t))
    altpos += (p - a) > 0
print("Part C positive count", altpos)

# Proposition 1.4 hypothesis check: its proof needs 1 + r > 0. Counterexample when r <= -1.
r2, g2 = F(-2), F(-1, 2)   # g2 >= r2, 1 + g2 > 0, d1 = 1 (scale-free), but r2 <= -1
partial = []
S = F(0)
for N in range(1, 41):
    S += (1 * (1 + g2) ** (N - 1)) / (1 + r2) ** N
    partial.append(S)
print("counterexample r=-2, g=-1/2, d1=1: S_1, S_2, S_10, S_40 =", float(partial[0]), float(partial[1]), float(partial[9]), float(partial[39]))
print("closed form d1/(r-g) =", float(1 / (r2 - g2)), "(partial sums converge to the closed form here, not +infinity)")
