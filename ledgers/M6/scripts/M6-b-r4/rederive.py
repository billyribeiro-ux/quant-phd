"""Independent re-derivation of the L05-L08 numbers (verifier round 4, M6-b). Run with python3 -I."""

import itertools
import math
from fractions import Fraction as F

# L05: block integral and quadrature errors
c = math.atan(2) - math.pi / 4
print("L05 block integral", round(c, 10), "9 blocks", round(9 * c, 10), "10 blocks", round(10 * c, 9))
print("L05 quadrature error y-first", 0.7853982936 - math.pi / 4)

# L07: cell averages and MSE of the cell average
P = [F(n, 16) for n in (1, 2, 1, 3, 2, 3, 2, 2)]
X = [F(v) for v in (2, -1, 4, 0, 3, -2, 1, 5)]
CELLS = ((0, 1, 2), (3, 4), (5, 6, 7))
avg = {}
for cell in CELLS:
    pc = sum(P[w] for w in cell)
    a = sum(P[w] * X[w] for w in cell) / pc
    for w in cell:
        avg[w] = a
    print("L07 cell", cell, "prob", pc, "avg", a)
mse = sum(P[w] * (X[w] - avg[w]) ** 2 for w in range(8))
print("L07 MSE of cell average", mse, float(mse))

# L08: cell test on the ten-step tree, independent of the lab twin
N = 10


def wt(path, p):
    out = F(1)
    for s in path:
        out *= p if s == 1 else 1 - p
    return out


for p in (F(1, 2), F(1, 3)):
    good = 0
    tot = 0
    for k in range(N):
        for pre in itertools.product((1, -1), repeat=k):
            mem = [q for q in itertools.product((1, -1), repeat=N) if q[:k] == pre]
            m = sum(wt(q, p) for q in mem)
            av = sum(wt(q, p) * sum(q[: k + 1]) for q in mem) / m
            tot += 1
            good += av == sum(pre)
    print("L08 p", p, "cells agreeing", good, "of", tot)
