"""Independent check of the numbers printed on the M7 project page: Lab 1 (KKT solution), Lab 3 (certificate checks).

Uses only fractions and a hand-written 3x3 solver, not the lab code. Usage: python -I -W error <this file>
"""

from fractions import Fraction as F

G = F(2)
S = [[F(4, 100), F(1, 100), F(0)], [F(1, 100), F(9, 100), F(2, 100)], [F(0), F(2, 100), F(16, 100)]]
MU = [F(5, 100), F(3, 100), F(-2, 100)]


def solve(a, b):
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


# Budget-only: gamma*S w + nu*1 = mu, sum w = 1 (unknowns w1..w3, nu)
a = [[G * S[i][j] for j in range(3)] + [F(1)] for i in range(3)] + [[F(1), F(1), F(1), F(0)]]
sol = solve(a, MU + [F(1)])
print("budget-only w:", [str(x) for x in sol[:3]], "nu:", str(sol[3]))
assert sol[:3] == [F(54, 65), F(5, 26), F(-3, 130)], "budget-only weights differ from page"

# Constrained: w3 = 0 held; unknowns w1, w2, nu, lam3 with stationarity for each weight, budget, w3 = 0
a = [
    [G * S[0][0], G * S[0][1], F(1), F(0)],
    [G * S[1][0], G * S[1][1], F(1), F(0)],
    [G * S[2][0], G * S[2][1], F(1), F(-1)],
    [F(1), F(1), F(0), F(0)],
]
w1, w2, nu, lam3 = solve(a, [MU[0], MU[1], MU[2], F(1)])
w = [w1, w2, F(0)]
print("constrained w:", [str(x) for x in w], "nu:", str(nu), "lam3:", str(lam3))
assert w == [F(9, 11), F(2, 11), F(0)] and nu == F(-21, 1100) and lam3 == F(9, 1100)
res = [G * sum(S[i][j] * w[j] for j in range(3)) - MU[i] + nu - (lam3 if i == 2 else 0) for i in range(3)]
print("stationarity residuals:", [str(r) for r in res])
q = sum(S[i][j] * w[i] * w[j] for i in range(3) for j in range(3))
obj = G / 2 * q - sum(MU[i] * w[i] for i in range(3))
print("objective:", str(obj), float(obj))
assert obj == F(-3, 220)
print("lab 1 numbers: OK")

# Lab 3 check B and C, recomputed from the stated formulas
w = [F(9, 11), F(2, 11), F(0)]
budget = nu
def stat(wv, lower):
    return [G * sum(S[i][j] * wv[j] for j in range(3)) - MU[i] + budget - lower[i] for i in range(3)]
print("check A stationarity:", [str(x) for x in stat(w, [F(0), F(0), lam3])])
flipped = [F(0), F(0), -lam3]
print("check B stationarity:", [str(x) for x in stat(w, flipped)], "dual:", str(max(F(0), -min(flipped))))
moved = [F(9, 11) + F(1, 1000), F(2, 11) - F(1, 1000), F(0)]
print("check C stationarity:", [str(x) for x in stat(moved, [F(0), F(0), lam3])], "budget gap:", str(sum(moved) - 1))
assert max(abs(x) for x in stat(w, flipped)) == F(9, 550)
assert max(abs(x) for x in stat(moved, [F(0), F(0), lam3])) == F(1, 6250)
print("lab 3 numbers: OK")
