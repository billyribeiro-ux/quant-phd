"""Re-derive L05 Part A numbers (KKT system of Remark 2.4) with exact fractions."""
from fractions import Fraction as F

def det(m):
    n = len(m)
    if n == 1:
        return F(m[0][0])
    return sum((-1) ** j * F(m[0][j]) * det([row[:j] + row[j + 1:] for row in m[1:]]) for j in range(n))

def solve(a, b):
    n = len(b)
    m = [[F(x) for x in row] + [F(bi)] for row, bi in zip(a, b)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]

Q = [[4, 1, 0], [1, 3, 1], [0, 1, 2]]
A = [[1, 1, 1], [0, 1, -1]]
c = [-1, 0, 2]
b = [1, 0]
K = [[Q[i][j] for j in range(3)] + [A[k][i] for k in range(2)] for i in range(3)]
K += [[A[k][j] for j in range(3)] + [0, 0] for k in range(2)]
print("det K", det(K))
rhs = [-x for x in c] + b
sol = solve(K, rhs)
x, lam = sol[:3], sol[3:]
print("x", x, "lambda", lam)
qx = [sum(Q[i][j] * x[j] for j in range(3)) for i in range(3)]
xqx = sum(x[i] * qx[i] for i in range(3))
print("x'Qx", xqx, "half", xqx / 2, "c'x", sum(c[i] * x[i] for i in range(3)))
print("objective", xqx / 2 + sum(c[i] * x[i] for i in range(3)))
grad = [qx[i] + c[i] for i in range(3)]
print("gradient Qx+c", grad, "-A'lambda", [-(A[0][i] * lam[0] + A[1][i] * lam[1]) for i in range(3)])
print("residual A x - b", [sum(A[k][i] * x[i] for i in range(3)) - b[k] for k in range(2)])
v = [-2, 1, 1]
print("A v", [sum(A[k][i] * v[i] for i in range(3)) for k in range(2)])
print("v'Qv", sum(v[i] * Q[i][j] * v[j] for i in range(3) for j in range(3)))
print("Qv", [sum(Q[i][j] * v[j] for j in range(3)) for i in range(3)])
