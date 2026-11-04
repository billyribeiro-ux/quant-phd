"""Round 6 (M7-d): independent recomputation of every number the M7 project page prints for Labs 1 and 3 and the hand cases.

Pure stdlib, exact Fractions, a fresh solver written from the KKT conditions (no import from the lab or the grader).
"""

from fractions import Fraction as F

GAMMA = F(2)
SIGMA = [[F(4, 100), F(1, 100), F(0)], [F(1, 100), F(9, 100), F(2, 100)], [F(0), F(2, 100), F(16, 100)]]
MU = [F(5, 100), F(3, 100), F(-2, 100)]


def gauss(a, b):
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def kkt(held):
    """Budget-only or with held assets at zero: unknowns w (3), nu, and one bound multiplier per held asset."""
    N = 3
    size = N + 1 + len(held)
    A = [[F(0)] * size for _ in range(size)]
    b = [F(0)] * size
    for i in range(N):
        for j in range(N):
            A[i][j] = GAMMA * SIGMA[i][j]
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
    s = gauss(A, b)
    return s[:N], s[N], s[N + 1:]


free, _, _ = kkt([])
print("budget-only weights", [str(x) for x in free])
held = [i for i in range(3) if free[i] < 0]
w, nu, lam = kkt(held)
print("held", held, "weights", [str(x) for x in w], "nu", str(nu), "lam", [str(x) for x in lam])
res = [GAMMA * sum(SIGMA[i][j] * w[j] for j in range(3)) - MU[i] + nu for i in range(3)]
for c, j in enumerate(held):
    res[j] -= lam[c]
print("stationarity", [str(x) for x in res], "budget gap", str(sum(w) - 1))
obj = GAMMA / 2 * sum(SIGMA[i][j] * w[i] * w[j] for i in range(3) for j in range(3)) - sum(MU[i] * w[i] for i in range(3))
print("objective", str(obj), float(obj))

# Lab 3 candidates, residuals as defined on the page (budget and lower bounds only, plus w_i <= 1)
def residuals(wv, budget, lower, upper):
    primal = max([F(0), abs(sum(wv) - 1), *(-x for x in wv), *(x - 1 for x in wv)])
    stat = [GAMMA * sum(SIGMA[i][j] * wv[j] for j in range(3)) - MU[i] + budget - lower[i] + upper[i] for i in range(3)]
    dual = max([F(0), *(-x for x in lower), *(-x for x in upper)])
    comp = max([abs(lower[i] * wv[i]) for i in range(3)] + [abs(upper[i] * (wv[i] - 1)) for i in range(3)])
    return primal, max(abs(s) for s in stat), dual, comp

z = [F(0)] * 3
A_ = [F(9, 11), F(2, 11), F(0)]
bud = F(-21, 1100)
lo = [F(0), F(0), F(9, 1100)]
up = [F(0)] * 3
print("A", [str(v) for v in residuals(A_, bud, lo, up)])
print("B", [str(v) for v in residuals(A_, bud, [F(0), F(0), F(-9, 1100)], z)])
moved = [F(9, 11) + F(1, 1000), F(2, 11) - F(1, 1000), F(0)]
print("C", [str(v) for v in residuals(moved, bud, lo, up)])
print("C stationarity float", float(residuals(moved, bud, lo, up)[1]))
