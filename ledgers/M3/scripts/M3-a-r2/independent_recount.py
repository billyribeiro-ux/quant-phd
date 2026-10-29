# Round 2, slice M3-a: independent recount of the L01 and L02 lab claims with different algorithms
# (numpy matrix_rank for L01 ranks; adjugate-formula inverse with Fraction for L02, not the lab's Gauss-Jordan).
import sys
from fractions import Fraction as F

import numpy as np


class Gen:
    def __init__(self, seed):
        self.s = seed % 2**31

    def draw(self, bound):
        self.s = (1103515245 * self.s + 12345) % 2**31
        return ((self.s >> 16) % (2 * bound + 1)) - bound


def l01_counts():
    g = Gen(20261028)

    def vec(n):
        return [g.draw(3) for _ in range(n)]

    def count(n, k, draws):
        return sum(np.linalg.matrix_rank(np.array([vec(n) for _ in range(k)], dtype=float).T) == k for _ in range(draws))

    out = [count(3, 3, 200), count(3, 4, 200), count(4, 4, 200), count(4, 5, 200)]
    dep = tri = r3 = 0
    for _ in range(100):
        v1, v2, v3 = vec(4), vec(4), vec(4)
        v4 = [2 * a - b + c for a, b, c in zip(v1, v2, v3, strict=True)]
        dep += np.linalg.matrix_rank(np.array([v1, v2, v3, v4], dtype=float).T) < 4
        tri += np.linalg.matrix_rank(np.array([v1, v2, v3], dtype=float).T) == 3
        r3 += np.linalg.matrix_rank(np.array([v1, v2, v3, v4], dtype=float).T) == 3
    return out, (dep, tri, r3)


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def inv3(m):
    d = det3(m)
    if d == 0:
        return None
    cof = [[0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            minor = [[m[r][c] for c in range(3) if c != j] for r in range(3) if r != i]
            cof[i][j] = (-1) ** (i + j) * (minor[0][0] * minor[1][1] - minor[0][1] * minor[1][0])
    return [[F(cof[j][i], d) for j in range(3)] for i in range(3)]


def mm(a, b):
    return [[sum(F(a[i][k]) * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def l02_counts():
    g = Gen(7)

    def dm(bound):
        return [[F(g.draw(bound)) for _ in range(3)] for _ in range(3)]

    rejected = 0
    ok_formula = ok_comp = 0
    first = None
    for p in range(50):
        a, c = dm(4), dm(4)
        while True:
            s = dm(3)
            si = inv3(s)
            if si is None:
                rejected += 1
            else:
                break
        formula = mm(mm(si, a), s)
        ok_formula += formula == mm(si, mm(a, s))
        ok_comp += mm(mm(si, mm(c, a)), s) == mm(mm(mm(si, c), s), mm(si, mm(a, s)))
        if p == 0:
            first = formula
    return rejected, first, ok_formula, ok_comp


if __name__ == "__main__":
    counts, planted = l01_counts()
    print("L01 independent counts (numpy rank):", counts)
    print("L01 planted (dependent, independent triples, rank3):", planted)
    rejected, first, ok_formula, ok_comp = l02_counts()
    print('L02 coordinate-form equal (exact):', ok_formula, 'of 50; composition equal (exact):', ok_comp, 'of 50')
    print("L02 singular S rejected:", rejected)
    print("L02 first pair, S^-1 A S row by row:", [[str(x) for x in row] for row in first])
    sys.stdout.flush()
