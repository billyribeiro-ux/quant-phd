"""Independent recomputation of the numbers on the changed M7 cards and the L05 and L08 examples (verifier round 4, slice e).

Run: .venv/bin/python -I ledgers/M7/scripts/M7-e-r4/recompute_r4.py
Uses only fractions and itertools; no reuse of the lab code.
"""
from fractions import Fraction as F
from itertools import product

print("== L05 Part A (Remark 2.4 data)")
Q = [[F(4), F(1), F(0)], [F(1), F(3), F(1)], [F(0), F(1), F(2)]]
c = [F(-1), F(0), F(2)]
A = [[F(1), F(1), F(1)], [F(0), F(1), F(-1)]]
b = [F(1), F(0)]
v = [F(-2), F(1), F(1)]


def det(m):
    n = len(m)
    if n == 1:
        return m[0][0]
    return sum(((-1) ** j) * m[0][j] * det([r[:j] + r[j + 1:] for r in m[1:]]) for j in range(n))


def solve(m, rhs):
    n = len(rhs)
    rows = [list(m[i]) + [rhs[i]] for i in range(n)]
    for col in range(n):
        piv = next(r for r in range(col, n) if rows[r][col] != 0)
        rows[col], rows[piv] = rows[piv], rows[col]
        for r in range(n):
            if r != col and rows[r][col] != 0:
                fac = rows[r][col] / rows[col][col]
                rows[r] = [a - fac * bb for a, bb in zip(rows[r], rows[col])]
    return [rows[i][n] / rows[i][i] for i in range(n)]


K = [Q[i] + [A[k][i] for k in range(2)] for i in range(3)] + [A[k] + [F(0), F(0)] for k in range(2)]
print("kkt_det", det(K), "(lab prints 19)")
sol = solve(K, [-x for x in c] + b)
x, lam = sol[:3], sol[3:]
print("x", [str(t) for t in x], "(lab: 13/19 3/19 3/19)")
print("lambda", [str(t) for t in lam], "(lab: -36/19 11/19)")
fq = lambda z: F(1, 2) * sum(z[i] * Q[i][j] * z[j] for i in range(3) for j in range(3)) + sum(c[i] * z[i] for i in range(3))
print("objective exact", fq(x), float(fq(x)), "(lab prints 0.7631578947; 551/722 =", F(551, 722), ")")
print("x'Qx", sum(x[i] * Q[i][j] * x[j] for i in range(3) for j in range(3)), "(817/361 expected)")
grad = [sum(Q[i][j] * x[j] for j in range(3)) + c[i] for i in range(3)]
print("grad at x", [str(g) for g in grad], "-A'lambda =", [str(-sum(A[k][i] * lam[k] for k in range(2))) for i in range(3)])
print("grad zero?", all(g == 0 for g in grad))
print("stationarity residual exact zero", all(grad[i] + sum(A[k][i] * lam[k] for k in range(2)) == 0 for i in range(3)))
print("constraint residual exact zero", all(sum(A[k][i] * x[i] for i in range(3)) == b[k] for k in range(2)))
print("Av", [sum(A[k][i] * v[i] for i in range(3)) for k in range(2)])
Qv = [sum(Q[i][j] * v[j] for j in range(3)) for i in range(3)]
print("Qv", Qv, "vQv", sum(v[i] * Qv[i] for i in range(3)), "(card/lesson: 19)")
# Remark 2.4 completing-the-square identity, symbolic check at random rational points
import random
random.seed(4)
ok = True
for _ in range(2000):
    x1, x2, x3 = (F(random.randint(-50, 50), random.randint(1, 9)) for _ in range(3))
    lhs = 4 * x1 * x1 + 3 * x2 * x2 + 2 * x3 * x3 + 2 * x1 * x2 + 2 * x2 * x3
    rhs = (2 * x1 + F(1, 2) * x2) ** 2 + F(11, 4) * (x2 + F(4, 11) * x3) ** 2 + F(18, 11) * x3 * x3
    ok = ok and lhs == rhs
print("Remark 2.4 completing-square identity holds on 2000 rational points:", ok)

print("== L05 Part B (Q=[[2,1],[1,2]], c=(-3,1), x>=0)")
QB = [[F(2), F(1)], [F(1), F(2)]]
cB = [F(-3), F(1)]
cands = []
for mask in product((0, 1), repeat=2):
    fixed = [i for i in range(2) if mask[i]]
    free = [i for i in range(2) if not mask[i]]
    xx = [F(0), F(0)]
    if free:
        sub = [[QB[i][j] for j in free] for i in free]
        rhs = [-cB[i] for i in free]
        if len(free) == 1:
            sol1 = [rhs[0] / sub[0][0]]
        else:
            sol1 = solve(sub, rhs)
        for p, val in zip(free, sol1):
            xx[p] = val
    g = [sum(QB[i][j] * xx[j] for j in range(2)) + cB[i] for i in range(2)]
    primal = all(t >= 0 for t in xx)
    dual = all(g[i] >= 0 for i in fixed)
    print("candidate", "{" + ",".join(str(i + 1) for i in fixed) + "}", "x", [str(t) for t in xx], "primal", primal, "dual", dual)
    if primal and dual:
        cands.append((fixed, xx))
print("passing", len(cands))
xh = cands[0][1]
val = F(1, 2) * sum(xh[i] * QB[i][j] * xh[j] for i in range(2) for j in range(2)) + sum(cB[i] * xh[i] for i in range(2))
print("xhat", [str(t) for t in xh], "objective", val)
grid = [F(k, 16) for k in range(33)]
pts = [(a, bb) for a in grid for bb in grid]
below = sum(1 for a, bb in pts if F(1, 2) * (QB[0][0] * a * a + 2 * QB[0][1] * a * bb + QB[1][1] * bb * bb) + cB[0] * a + cB[1] * bb < val)
print("grid points", len(pts), "below", below, "min equals candidate", min(F(1, 2) * (2 * a * a + 2 * a * bb + 2 * bb * bb) - 3 * a + bb for a, bb in pts) == val)

print("== L08 negative-discount example (H=2, beta=-1, reward x=0, y=1, B=0, f(s,a)=s)")
beta = F(-1)
r = {"x": F(0), "y": F(1)}
B = F(0)
totals = {}
for a0, a1 in product("xy", repeat=2):
    totals[(a0, a1)] = r[a0] + beta * r[a1] + beta * beta * B
print("plan totals", totals)
V0 = max(totals.values())
U2 = B
V1 = max(r[a] + beta * B for a in "xy")
U1 = max(r[a] + beta * U2 for a in "xy")
U0 = max(r[a] + beta * U1 for a in "xy")
print("V0", V0, "V1", V1, "U1", U1, "U0", U0, "U0 != V0:", U0 != V0)
print("beta>=0 case, sanity (beta=1): V0 =", max(r[a0] + r[a1] for a0, a1 in product("xy", repeat=2)))

print("== L01 Q2 eigen and P3 (negative eigenvector gives a negative gap)")
Q2 = [[F(1), F(2)], [F(2), F(1)]]
mv = lambda m, z: [sum(m[i][j] * z[j] for j in range(2)) for i in range(2)]
print("Q2(1,1)", mv(Q2, [F(1), F(1)]), "Q2(1,-1)", mv(Q2, [F(1), F(-1)]))
qf = lambda z: sum(z[i] * Q2[i][j] * z[j] for i in range(2) for j in range(2))
vv = [F(1), F(-1)]
print("q(v)", qf(vv), "gap at lambda=1/2 between x=v,y=0:", F(1, 2) * qf(vv) + F(1, 2) * qf([F(0), F(0)]) - qf([vv[0] / 2, vv[1] / 2]))

print("== Remark 2.2 (n=2, Q=I, A rows (1,0), K singular) and Remark 3.2 (n=1, Q=1, c=-1, G=-1, h=0)")
QI = [[F(1), F(0)], [F(0), F(1)]]
A22 = [[F(1), F(0)], [F(1), F(0)]]
K22 = [QI[i] + [A22[k][i] for k in range(2)] for i in range(2)] + [A22[k] + [F(0), F(0)] for k in range(2)]
for row in K22:
    print("row", [str(t) for t in row])
print("det K (Remark 2.2) =", det(K22), "; rows 3 and 4 equal:", K22[2] == K22[3])
f32 = lambda z: F(1, 2) * z * z - z
print("Remark 3.2: f(0) =", f32(F(0)), " f(1) =", f32(F(1)), " stationarity at xbar=0: xbar - 1 - mu = 0 gives mu =", F(0) - 1)
print("Remark 3.2 mu = -1 is negative:", F(-1) < 0)
