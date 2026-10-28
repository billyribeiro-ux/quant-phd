"""Independent recomputation of M7 project Lab 1 and Lab 3 numbers (fractions, own enumeration of active sets)."""
from fractions import Fraction as F
from itertools import product

G = F(2)
S = [[F(4, 100), F(1, 100), F(0)], [F(1, 100), F(9, 100), F(2, 100)], [F(0), F(2, 100), F(16, 100)]]
MU = [F(5, 100), F(3, 100), F(-2, 100)]
N = 3

def solve(A, b):
    # Cramer-free Gaussian elimination, independent of the lab's helper
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        M[c] = [x / piv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]

# Enumerate all subsets of lower bounds held at zero; for each, solve the KKT system and test all four conditions.
found = []
for pattern in product([0, 1], repeat=N):
    held = [i for i in range(N) if pattern[i]]
    # unknowns: w (3), nu (1), lam (len held)
    m = N + 1 + len(held)
    A = [[F(0)] * m for _ in range(m)]
    b = [F(0)] * m
    for i in range(N):
        for j in range(N):
            A[i][j] = G * S[i][j]
        A[i][N] = F(1)
        for c, j in enumerate(held):
            if i == j:
                A[i][N + 1 + c] = F(-1)
        b[i] = MU[i]
    for j in range(N):
        A[N][j] = F(1)
    b[N] = F(1)
    for c, j in enumerate(held):
        A[N + 1 + c][j] = F(1)
        b[N + 1 + c] = F(0)
    try:
        sol = solve(A, b)
    except StopIteration:
        continue
    w, nu, lam = sol[:N], sol[N], sol[N + 1:]
    feasible = all(x >= 0 for x in w) and sum(w) == 1
    dual = all(l >= 0 for l in lam)
    if feasible and dual:
        found.append((held, w, nu, lam))
for held, w, nu, lam in found:
    obj = G / 2 * sum(S[i][j] * w[i] * w[j] for i in range(N) for j in range(N)) - sum(MU[i] * w[i] for i in range(N))
    print("active", held, "w", [str(x) for x in w], "nu", str(nu), "lam", [str(x) for x in lam], "obj", str(obj), float(obj))

# Lab 3 check numbers
w = [F(9, 11), F(2, 11), F(0)]
nu = F(-21, 1100)
lo = [F(0), F(0), F(9, 1100)]
def stat(wv, budget, lower, upper):
    return [G * sum(S[i][j] * wv[j] for j in range(N)) - MU[i] + budget - lower[i] + upper[i] for i in range(N)]
print("A stationarity", [str(x) for x in stat(w, nu, lo, [F(0)] * 3)])
print("B stationarity", [str(x) for x in stat(w, nu, [F(0), F(0), -F(9, 1100)], [F(0)] * 3)], "max", str(max(abs(x) for x in stat(w, nu, [F(0), F(0), -F(9, 1100)], [F(0)] * 3))))
mv = [F(9, 11) + F(1, 1000), F(2, 11) - F(1, 1000), F(0)]
print("C stationarity", [str(x) for x in stat(mv, nu, lo, [F(0)] * 3)], "max abs", str(max(abs(x) for x in stat(mv, nu, lo, [F(0)] * 3))))
print("C budget gap", str(sum(mv) - 1))
