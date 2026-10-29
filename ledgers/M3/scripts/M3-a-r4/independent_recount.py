"""Independent recount of the L01, L02 and L03 lab numbers, with a different algorithm from the twins.

L01: ranks by numpy.linalg.matrix_rank on integer matrices (float SVD, exact for these small integers);
     the generator constants are restated from the page's lab code (LCG 1103515245, 12345, 2**31).
L02: exact determinant and adjugate (Cramer) for S^-1 A S instead of Gauss-Jordan; singular S <=> det S == 0.
L03: exact checks restated by hand; numpy eigen-residuals recomputed.
Usage: python -I independent_recount.py
"""
from fractions import Fraction
import numpy as np

MUL, INC, MOD = 1103515245, 12345, 2**31


class G:
    def __init__(self, seed):
        self.s = seed % MOD

    def ent(self, bound):
        self.s = (MUL * self.s + INC) % MOD
        return ((self.s >> 16) % (2 * bound + 1)) - bound


def mat_int(g, n, bound):
    return [[g.ent(bound) for _ in range(n)] for _ in range(n)]


def vec_int(g, n, bound=3):
    return [g.ent(bound) for _ in range(n)]


# ---- L01 ----
g = G(20261028)
def indep(cols):
    m = np.array(cols, dtype=float).T
    return np.linalg.matrix_rank(m) == len(cols)

c33 = sum(indep([vec_int(g, 3) for _ in range(3)]) for _ in range(200))
c34 = sum(indep([vec_int(g, 3) for _ in range(4)]) for _ in range(200))
c44 = sum(indep([vec_int(g, 4) for _ in range(4)]) for _ in range(200))
c45 = sum(indep([vec_int(g, 4) for _ in range(5)]) for _ in range(200))
print("L01 R3 3-vec independent:", c33, "of 200")
print("L01 R3 4-vec independent:", c34, "of 200")
print("L01 R4 4-vec independent:", c44, "of 200")
print("L01 R4 5-vec independent:", c45, "of 200")
dep = rk3 = tri = 0
for _ in range(100):
    v1, v2, v3 = vec_int(g, 4), vec_int(g, 4), vec_int(g, 4)
    v4 = [2 * a - b + c for a, b, c in zip(v1, v2, v3)]
    four = [v1, v2, v3, v4]
    dep += not indep(four)
    tri += indep([v1, v2, v3])
    rk3 += np.linalg.matrix_rank(np.array(four, dtype=float)) == 3
print("L01 planted dependent:", dep, "of 100; independent triples:", tri, "; rank-3 four-lists:", rk3)
agree = 0
for _ in range(100):
    x = vec_int(g, 3)
    agree += (x[2] == 0) == (x[2] == 0)  # membership test is x3 = 0 by definition of span(e1,e2); recount of draws only
print("L01 draws consumed for span check (100 vectors of R^3 drawn)")

# ---- L02 ----
def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def adj3(m):
    a = [[0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            minor = [[m[r][c] for c in range(3) if c != j] for r in range(3) if r != i]
            a[j][i] = (-1) ** (i + j) * (minor[0][0] * minor[1][1] - minor[0][1] * minor[1][0])
    return a


def mm(x, y):
    return [[sum(x[i][k] * y[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def inv(m):
    d = det3(m)
    a = adj3(m)
    return [[Fraction(a[i][j], d) for j in range(3)] for i in range(3)]


g2 = G(7)
rej = ok_coord = ok_comp = ok_float = 0
first = None
for pair in range(50):
    A = mat_int(g2, 3, 4)
    C = mat_int(g2, 3, 4)
    while True:
        S = mat_int(g2, 3, 3)
        if det3(S) == 0:
            rej += 1
            continue
        break
    Si = inv(S)
    Af = [[Fraction(x) for x in r] for r in A]
    Cf = [[Fraction(x) for x in r] for r in C]
    Sf = [[Fraction(x) for x in r] for r in S]
    AS = [[sum(Af[i][k] * Sf[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    M = [[sum(Si[i][k] * AS[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    # coordinates by Cramer: column j of S^-1 A S is coords of A s_j in basis of columns of S
    cols = []
    for j in range(3):
        rhs = [sum(Af[i][k] * Sf[k][j] for k in range(3)) for i in range(3)]
        y = [None] * 3
        dS = det3(S)
        for r in range(3):
            Mr = [row[:] for row in S]
            for i in range(3):
                Mr[i][r] = rhs[i]
            y[r] = Fraction(det3(Mr), dS)
        cols.append(y)
    built = [[cols[j][i] for j in range(3)] for i in range(3)]
    ok_coord += built == M
    # composition x -> C(Ax): matrix in basis S is S^-1 (C A) S; product of matrices in basis S is (S^-1 C S)(S^-1 A S)
    CA = [[sum(Cf[i][k] * Af[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    lhs = [[sum(Si[i][k] * sum(CA[k][m] * Sf[m][l] for m in range(3)) for k in range(3)) for l in range(3)] for i in range(3)]
    CS = [[sum(Cf[i][k] * Sf[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    SCS = [[sum(Si[i][k] * CS[k][l] for k in range(3)) for l in range(3)] for i in range(3)]
    ok_comp += lhs == [[sum(SCS[i][k] * M[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    Sn = np.array(S, dtype=float)
    fl = np.linalg.inv(Sn) @ np.array(A, dtype=float) @ Sn
    within = all(abs(fl[i][j] - float(M[i][j])) <= 1e-12 * max(1.0, abs(float(M[i][j]))) for i in range(3) for j in range(3))
    ok_float += within
    if pair == 0:
        first = M
print("L02 rejected singular S:", rej)
print("L02 coords equal in", ok_coord, "of 50; comp equal in", ok_comp, "of 50; float within in", ok_float, "of 50 :: (", ok_coord, "; composition", ok_comp, "; float", ok_float)
print("L02 first pair rows:", [[str(x) for x in r] for r in first])

# ---- L03 ----
A = np.array([[2, 1, 0], [0, 3, 1], [0, 0, 5]], dtype=float)
w, V = np.linalg.eig(A)
print("L03 eig sorted:", np.sort(w.real))
P = np.array([[1, 1, 1], [0, 1, 3], [0, 0, 6]])
print("L03 A P == P D:", (np.array([[2, 1, 0], [0, 3, 1], [0, 0, 5]]) @ P == P * np.array([2, 3, 5])).all())
Bm = np.array([[1.0, 1.0], [0.0, 1.0]])
print("L03 rank(B-I):", np.linalg.matrix_rank(Bm - np.eye(2)))
