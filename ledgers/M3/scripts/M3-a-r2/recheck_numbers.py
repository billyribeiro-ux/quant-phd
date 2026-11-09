"""Verifier re-derivation (M3 slice a, round 2) of the printed numbers in labs L01-L03, by a method independent of the twins.

L01 counts use determinants of square minors (not elimination) on the same seeded draws; the draw
generator is re-implemented from the constants printed in the twin. L02 uses the adjugate formula for
3 x 3 inverses in Fractions and numpy.linalg.inv for the float check. L03 recomputes the characteristic
polynomial and the eigenvector identities by hand-written algebra, and the numpy residuals.
Usage: python -I -W error ledgers/M3/scripts/M3-a-r2/recheck_numbers.py
"""

from fractions import Fraction
from itertools import combinations

import numpy as np

MUL, INC, MOD = 1103515245, 12345, 2**31


class Gen:
    def __init__(self, seed):
        self.s = seed % MOD

    def step(self):
        self.s = (MUL * self.s + INC) % MOD
        return self.s >> 16

    def entry(self, b):
        return self.step() % (2 * b + 1) - b


def det(m):
    """Laplace expansion, exact integers or Fractions, for square lists."""
    n = len(m)
    if n == 1:
        return m[0][0]
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    return sum((-1) ** j * m[0][j] * det([row[:j] + row[j + 1 :] for row in m[1:]]) for j in range(n))


def indep_by_minors(cols):
    """Columns are linearly independent iff some k x k minor of the n x k matrix is nonzero (k = len(cols))."""
    k = len(cols)
    n = len(cols[0])
    rows = [[cols[j][i] for j in range(k)] for i in range(n)]
    if k > n:
        return False
    for rs in combinations(range(n), k):
        if det([rows[r] for r in rs]) != 0:
            return True
    return False


def vec(g, n, b=3):
    return [g.entry(b) for _ in range(n)]


# ---- L01
g = Gen(20261028)
out = {}
for label, (n, k) in {"R3_3": (3, 3), "R3_4": (3, 4), "R4_4": (4, 4), "R4_5": (4, 5)}.items():
    out[label] = sum(indep_by_minors([vec(g, n) for _ in range(k)]) for _ in range(200))
print("L01 R^3 3-vec", out["R3_3"], "of 200 (twin prints 188)")
print("L01 R^3 4-vec", out["R3_4"], "of 200 (twin prints 0)")
print("L01 R^4 4-vec", out["R4_4"], "of 200 (twin prints 198)")
print("L01 R^4 5-vec", out["R4_5"], "of 200 (twin prints 0)")
dep = trip = r3 = 0
for _ in range(100):
    v1, v2, v3 = vec(g, 4), vec(g, 4), vec(g, 4)
    v4 = [2 * a - b + c for a, b, c in zip(v1, v2, v3)]
    four = [v1, v2, v3, v4]
    dep += not indep_by_minors(four)
    trip += indep_by_minors([v1, v2, v3])
    rows = [[four[j][i] for j in range(4)] for i in range(4)]
    rows = [[four[j][i] for j in range(4)] for i in range(4)]
    # rank of the 4-list is 3 iff det = 0 and some 3-subset of the four columns is independent
    r3 += det(rows) == 0 and any(indep_by_minors([four[a], four[b], four[c]]) for a, b, c in combinations(range(4), 3))
print("L01 planted dependent", dep, "of 100 (twin prints 100)")
print("L01 independent triples", trip, "of 100 (twin prints 100)")
print("L01 planted rank-3 (approx test)", r3, "of 100 (twin prints 100)")

# ---- L02: exact inverse via adjugate, independent of the twin's elimination
def inv3(m):
    d = det(m)
    if d == 0:
        return None
    adj = [[0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            minor = [[m[r][c] for c in range(3) if c != j] for r in range(3) if r != i]
            adj[j][i] = (-1) ** (i + j) * det(minor)
    return [[Fraction(adj[i][j], d) for j in range(3)] for i in range(3)]


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


g2 = Gen(7)
rej = 0
ok_coord = ok_comp = ok_float = 0
first = None
for pair in range(50):
    A = [[g2.entry(4) for _ in range(3)] for _ in range(3)]
    C = [[g2.entry(4) for _ in range(3)] for _ in range(3)]
    while True:
        P = [[g2.entry(3) for _ in range(3)] for _ in range(3)]
        Pi = inv3(P)
        if Pi is not None:
            break
        rej += 1
    Af = [[Fraction(x) for x in r] for r in A]
    Cf = [[Fraction(x) for x in r] for r in C]
    Pf = [[Fraction(x) for x in r] for r in P]
    M = mm(mm(Pi, Af), Pf)
    # coordinates of A p_j in basis P: y_j = P^{-1} (A p_j)
    cols = []
    for j in range(3):
        pj = [Pf[i][j] for i in range(3)]
        apj = [sum(Af[i][k] * pj[k] for k in range(3)) for i in range(3)]
        cols.append([sum(Pi[i][k] * apj[k] for k in range(3)) for i in range(3)])
    built = [[cols[j][i] for j in range(3)] for i in range(3)]
    ok_coord += built == M
    MC = mm(mm(Pi, Cf), Pf)
    comp = mm(mm(Pi, mm(Cf, Af)), Pf)  # P^{-1} C A P
    ok_comp += comp == mm(MC, M)
    Pn = np.array(P, dtype=float)
    Fn = np.linalg.inv(Pn) @ np.array(A, dtype=float) @ Pn
    Mf = np.array([[float(x) for x in r] for r in M])
    ok_float += bool(np.all(np.abs(Fn - Mf) <= 1e-12 * np.maximum(1.0, np.abs(Mf))))
    if pair == 0:
        first = M
print("L02 rejected singular P", rej, "(twin prints 7)")
print("L02 coordinates equal P^-1AP", ok_coord, "of 50 (twin prints 50)")
print("L02 composition equal", ok_comp, "of 50 (twin prints 50)")
print("L02 float within 1e-12", ok_float, "of 50 (twin prints 50)")
print("L02 first pair matrix:", [[str(x) for x in r] for r in first], "(twin prints 3 -35/2 37/3 / 0 5 -5/3 / -2 8 -6)")

# ---- L03: independent algebra and numpy residuals
A = np.array([[2.0, 1.0, 0.0], [0.0, 3.0, 1.0], [0.0, 0.0, 5.0]])
for lam, v in [(2, (1, 0, 0)), (3, (1, 1, 0)), (5, (1, 3, 6))]:
    Av = [sum(int(A[i][k]) * v[k] for k in range(3)) for i in range(3)]
    print("L03 eigenpair", lam, Av == [lam * x for x in v])
w, V = np.linalg.eig(A)
print("L03 numpy eigenvalues sorted", np.sort(w.real))
print("L03 max residual", max(float(np.max(np.abs(A @ V[:, j] - w[j] * V[:, j]))) for j in range(3)))
print("L03 det(A-3I)", np.linalg.det(A - 3 * np.eye(3)))
Bm = np.array([[1.0, 1.0], [0.0, 1.0]])
print("L03 rank(B-I)", np.linalg.matrix_rank(Bm - np.eye(2)), "eigvals B", np.linalg.eigvals(Bm))
print("L03 det P", det([[1, 1, 1], [0, 1, 3], [0, 0, 6]]))
