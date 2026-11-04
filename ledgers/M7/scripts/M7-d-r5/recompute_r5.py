"""Independent exact recomputation of the Lab 1 and Lab 3 numbers quoted on project.html (Fraction, no shared code)."""

from fractions import Fraction as F

SIG = [[F(4, 100), F(1, 100), F(0)], [F(1, 100), F(9, 100), F(2, 100)], [F(0), F(2, 100), F(16, 100)]]
MU = [F(5, 100), F(3, 100), F(-2, 100)]
G = F(2)
# budget-only: solve (G*SIG) w + nu*1 = MU, sum w = 1 by exact Cramer-style elimination via sympy-free Gauss
def gauss(A, b):
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]

A = [[G * SIG[i][j] for j in range(3)] + [F(1)] for i in range(3)] + [[F(1), F(1), F(1), F(0)]]
free = gauss(A, MU + [F(1)])
print("budget-only weights", [str(x) for x in free[:3]], "nu", str(free[3]))
# held: asset 2 (negative); unknowns w0,w1,w2,nu,lam2
A2 = [[G * SIG[i][j] for j in range(3)] + [F(1), F(-1) if i == 2 else F(0)] for i in range(3)]
A2.append([F(1), F(1), F(1), F(0), F(0)])
A2.append([F(0), F(0), F(1), F(0), F(0)])
sol = gauss(A2, MU + [F(1), F(0)])
w, nu, lam = sol[:3], sol[3], sol[4]
print("constrained w", [str(x) for x in w], "nu", str(nu), "lam", str(lam))
resid = [G * sum(SIG[i][j] * w[j] for j in range(3)) - MU[i] + nu - (lam if i == 2 else 0) for i in range(3)]
print("stationarity residuals", [str(r) for r in resid])
obj = G / 2 * sum(SIG[i][j] * w[i] * w[j] for i in range(3) for j in range(3)) - sum(MU[i] * w[i] for i in range(3))
print("objective", str(obj), float(obj))
# Lab 3 candidates
def res(wv, budget, lower, upper):
    primal = max([F(0), abs(sum(wv) - 1), *(-x for x in wv), *(x - 1 for x in wv)])
    stat = [G * sum(SIG[i][j] * wv[j] for j in range(3)) - MU[i] + budget - lower[i] + upper[i] for i in range(3)]
    dual = max([F(0), *(-x for x in lower), *(-x for x in upper)])
    cs = max([abs(lower[i] * wv[i]) for i in range(3)] + [abs(upper[i] * (wv[i] - 1)) for i in range(3)])
    return primal, max(abs(s) for s in stat), dual, cs
w1 = [F(9, 11), F(2, 11), F(0)]
bud = F(-21, 1100)
z = [F(0)] * 3
print("A", [str(x) for x in res(w1, bud, [F(0), F(0), F(9, 1100)], z)])
print("B", [str(x) for x in res(w1, bud, [F(0), F(0), F(-9, 1100)], z)])
print("C", [str(x) for x in res([F(9, 11) + F(1, 1000), F(2, 11) - F(1, 1000), F(0)], bud, [F(0), F(0), F(9, 1100)], z)])
