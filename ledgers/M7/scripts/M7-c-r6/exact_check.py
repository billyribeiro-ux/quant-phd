"""Recompute the L07/L08 numbers that the pages print, in exact arithmetic (fractions).

Run as: python3 -I exact_check.py   (no arguments; prints one line per check)
"""

from fractions import Fraction as F
from math import comb

# L07 toy problem (Lab 1): wealth grid, reward table, bequest W // 100
GRID = (0, 100, 200, 300, 400)
REWARD = {0: 0, 100: 60, 200: 100, 300: 120, 400: 130}
H7 = 4


def feasible(w):
    return tuple(c for c in GRID if c <= w)


V7 = [{} for _ in range(H7 + 1)]
V7[H7] = {w: w // 100 for w in GRID}
for t in range(H7 - 1, -1, -1):
    for w in GRID:
        V7[t][w] = max(REWARD[c] + V7[t + 1][w - c] for c in feasible(w))
print("L07 W400 column", [V7[t][400] for t in range(5)])
print("L07 V0(400)-V3(400)", V7[0][400] - V7[3][400])
print("L07 greedy/optimal ratio", F(130, 240), float(F(130, 240)))
print("L07 check 220 via 200,100,100", 100 + 60 + 60 + 0)
print("L07 C(8,4)", comb(8, 4))
diffs = [V7[t][400] - V7[t + 1][400] for t in range(4)]
print("L07 E1 diffs", diffs)

# L08 maintenance problem: beta = 9/10, H = 6, terminal 0, states 0,1,2
D = F(9, 10)
PROFIT = {0: 6, 1: 4, 2: 1}


def rew(s, a):
    return F(PROFIT[s]) if a == "run" else F(-4)


def nxt(s, a):
    return min(s + 1, 2) if a == "run" else 0


def step(u):
    return {s: max(rew(s, a) + D * u[nxt(s, a)] for a in ("run", "repair")) for s in (0, 1, 2)}


V = [{0: F(0), 1: F(0), 2: F(0)}]
for _ in range(6):
    V.append(step(V[-1]))
V = V[::-1]
print("L08 V0(0) exact", V[0][0], float(V[0][0]))
print("L08 V0(0)-V1(0)", V[0][0] - V[1][0], float(V[0][0] - V[1][0]))
print("L08 V4(0)", V[4][0], "V5(0)", V[5][0])
print("L08 plans enumerated", 3 * sum(2 ** (6 - t) for t in range(6)))
U = [{0: F(0), 1: F(0), 2: F(0)}]
for _ in range(6):
    U.append(step(U[-1]))
changes = [max(abs(U[n + 1][s] - U[n][s]) for s in (0, 1, 2)) for n in range(6)]
print("L08 changes", [str(c) for c in changes], [float(c) for c in changes])
print("L08 ratios", [str(changes[n] / changes[n - 1]) for n in range(1, 6)])
print("L08 M1 V4(0) by hand", rew(0, "run") + D * V[5][1], rew(0, "repair") + D * V[5][0])
