"""M7-a round 1 witness: independent recomputation of the printed numbers in L01, L02, L03 (own code, no twin imports)."""
from fractions import Fraction as F
from itertools import product

# ---- L01 ----
Q1 = [[2, 1], [1, 2]]
Q2 = [[1, 2], [2, 1]]
def qf(Q, x):
    return sum(Q[i][j] * x[i] * x[j] for i in range(2) for j in range(2))
grid = [-2, -1, 0, 1, 2]
pts = list(product(grid, grid))
weights = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
cases = [(x, y, w) for x in pts for y in pts for w in weights]
def chord_ok(Q, x, y, w):
    z = (w * x[0] + (1 - w) * y[0], w * x[1] + (1 - w) * y[1])
    return qf(Q, z) <= w * qf(Q, x) + (1 - w) * qf(Q, y)
def ident_ok(Q, x, y, w):
    z = (w * x[0] + (1 - w) * y[0], w * x[1] + (1 - w) * y[1])
    d = (x[0] - y[0], x[1] - y[1])
    return qf(Q, z) == w * qf(Q, x) + (1 - w) * qf(Q, y) - w * (1 - w) * qf(Q, d)
print("L01 cases per function", len(cases))
print("L01 Q1 identity", sum(ident_ok(Q1, x, y, w) for x, y, w in cases))
print("L01 Q2 identity", sum(ident_ok(Q2, x, y, w) for x, y, w in cases))
print("L01 Q1 chord", sum(chord_ok(Q1, x, y, w) for x, y, w in cases))
print("L01 Q2 chord", sum(chord_ok(Q2, x, y, w) for x, y, w in cases))
neg = sum(1 for x, y in product(pts, repeat=2) if qf(Q2, (x[0] - y[0], x[1] - y[1])) < 0)
print("L01 negative ordered pairs for Q2", neg, "3*neg", 3 * neg)
z = (F(1, 2), F(1, 2))
print("L01 Q2 midpoint", qf(Q2, z), "chord", F(1, 2) * qf(Q2, (1, 0)) + F(1, 2) * qf(Q2, (0, 1)))
print("L01 Q2 at (1,-1)", qf(Q2, (1, -1)))
# eigenvalues by hand: Q1 3,1 ; Q2 3,-1
# ---- L02 ----
def lcg(seed, count):
    s = seed
    out = []
    for _ in range(count):
        s = (1103515245 * s + 12345) % 2**31
        out.append(s % 7 - 3)
    return out
ent = lcg(1, 9)
print("L02 A entries", ent)
A = [ent[0:3], ent[3:6], ent[6:9]]
S = [[F(sum(A[k][i] * A[k][j] for k in range(3)) + (1 if i == j else 0)) for j in range(3)] for i in range(3)]
print("L02 Sigma", [[int(v) for v in r] for r in S])
def det(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
D = det(S)
def solve_cramer(M, b):
    dM = det(M)
    res = []
    for c in range(3):
        Mc = [[(b[r] if j == c else M[r][j]) for j in range(3)] for r in range(3)]
        res.append(F(det(Mc)) / dM)
    return res
u = solve_cramer(S, [F(1)] * 3)
tot = sum(u)
lam = 1 / tot
w = [lam * x for x in u]
print("L02 sum u", tot, "lambda", lam, "w", w, "f(w)", sum(w[i] * sum(S[i][j] * w[j] for j in range(3)) for i in range(3)) / 2)
print("L02 Sigma w - lambda 1", [sum(S[i][j] * w[j] for j in range(3)) - lam for i in range(3)])
print("L02 lambda decimal", float(lam), "4dp", f"{float(lam):.4f}")
# ---- L03 ----
def f3(w1, mu):
    w2 = 1 - w1
    Sg = [[2, 1], [1, 2]]
    v = (w1, w2)
    quad = sum(Sg[i][j] * v[i] * v[j] for i in range(2) for j in range(2))
    return F(1, 2) * quad - (mu[0] * w1 + mu[1] * w2)
for name, mu, cand in [("active", (F(3, 2), F(1, 5)), F(1)), ("inactive", (F(1), F(1)), F(1, 2))]:
    vals = [(f3(F(k, 100), mu), F(k, 100)) for k in range(101)]
    m = min(vals)
    print("L03", name, "grid min", m[0], "at w1", m[1], "candidate f", f3(cand, mu))
# active KKT residual of off point (1/2,1/2) with mu (3/2,1/5), nu -1/2, lam (0,3/10)
mu = (F(3, 2), F(1, 5))
h = F(1, 2)
Sw = (2 * h + h, h + 2 * h)
grad = (Sw[0] - mu[0], Sw[1] - mu[1])
nu = F(-1, 2); lam2 = (F(0), F(3, 10))
print("L03 off-point stationarity", (grad[0] + nu - lam2[0], grad[1] + nu - lam2[1]))
print("L03 Remark 4.3 unconstrained", (F(14, 15), F(-11, 30)))
