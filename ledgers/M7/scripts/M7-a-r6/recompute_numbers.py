"""Independent recomputation of the numbers the M7 slice a pages state (L01-L03 and hub). No twin code is reused.

Usage: python3 -I ledgers/M7/scripts/M7-a-r6/recompute_numbers.py
"""
from fractions import Fraction as F
from itertools import product

out = []


def say(*a):
    out.append(" ".join(str(x) for x in a))


# ---- L01: grid counts ----
grid = [-2, -1, 0, 1, 2]
pts = list(product(grid, grid))
W = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
Q1 = [[2, 1], [1, 2]]
Q2 = [[1, 2], [2, 1]]


def qf(Q, x):
    return sum(F(Q[i][j]) * x[i] * x[j] for i in range(2) for j in range(2))


def comb(w, x, y):
    return (w * x[0] + (1 - w) * y[0], w * x[1] + (1 - w) * y[1])


cases = [(x, y, w) for x in pts for y in pts for w in W]
say("L01 cases per function", len(cases), "ordered pairs", len(pts) ** 2)
for name, Q in (("Q1", Q1), ("Q2", Q2)):
    ident = 0
    chord = 0
    for x, y, w in cases:
        z = comb(w, x, y)
        d = (x[0] - y[0], x[1] - y[1])
        if qf(Q, z) == w * qf(Q, x) + (1 - w) * qf(Q, y) - w * (1 - w) * qf(Q, d):
            ident += 1
        if qf(Q, z) <= w * qf(Q, x) + (1 - w) * qf(Q, y):
            chord += 1
    say(name, "identity", ident, "chord", chord)
neg = sum(1 for x, y in product(pts, pts) if qf(Q2, (x[0] - y[0], x[1] - y[1])) < 0)
say("Q2 negative ordered pairs", neg, "3*neg", 3 * neg, "3125-2573", 3125 - 2573)
mid = qf(Q2, (F(1, 2), F(1, 2)))
chord_val = F(1, 2) * qf(Q2, (1, 0)) + F(1, 2) * qf(Q2, (0, 1))
say("example midpoint", mid, "chord", chord_val, "diff", chord_val - mid, "term", F(1, 4) * qf(Q2, (1, -1)))
say("Q2 quad at (1,-1)", qf(Q2, (1, -1)))

# ---- L02: LCG, Sigma, closed form ----
state = 1
vals = []
for _ in range(9):
    state = (1103515245 * state + 12345) % 2**31
    vals.append(state % 7 - 3)
say("L02 A entries", vals)
A = [vals[0:3], vals[3:6], vals[6:9]]
S = [[F(sum(A[k][i] * A[k][j] for k in range(3)) + (1 if i == j else 0)) for j in range(3)] for i in range(3)]
say("Sigma", [[int(x) for x in row] for row in S])


def det3(m):
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def solve3(M, b):
    D = det3(M)
    res = []
    for c in range(3):
        Mc = [[b[r] if j == c else M[r][j] for j in range(3)] for r in range(3)]
        res.append(F(det3(Mc)) / D)
    return res


u = solve3(S, [F(1)] * 3)
s = sum(u)
lam = 1 / s
w = [lam * x for x in u]
fw = F(1, 2) * sum(w[i] * sum(S[i][j] * w[j] for j in range(3)) for i in range(3))
say("u", [str(x) for x in u], "s", s, "lambda", lam, "w", [str(x) for x in w], "f(w)", fw)
Sw = [sum(S[i][j] * w[j] for j in range(3)) for i in range(3)]
say("Sigma w - lambda 1", [str(Sw[i] - lam) for i in range(3)])
say("1'w", sum(w))
say("lambda decimal", float(lam), "177/55 =", F(177, 55), float(F(177, 55)))
say("L02 E1 first coordinate", 4 * F(47, 55) + 2 * F(17, 55) + 5 * F(-9, 55))

# ---- L03: grid minima, residuals, remark 4.3 ----
SIG = [[F(2), F(1)], [F(1), F(2)]]


def f_obj(w, mu):
    q = sum(w[i] * SIG[i][j] * w[j] for i in range(2) for j in range(2))
    return q / 2 - (mu[0] * w[0] + mu[1] * w[1])


def grid_min(mu):
    best = None
    arg = None
    for k in range(101):
        w1 = F(k, 100)
        v = f_obj((w1, 1 - w1), mu)
        if best is None or v < best:
            best, arg = v, w1
    return best, arg


say("L03 active grid min", grid_min((F(3, 2), F(1, 5))), "candidate", f_obj((F(1), F(0)), (F(3, 2), F(1, 5))))
say("L03 inactive grid min", grid_min((F(1), F(1))), "candidate", f_obj((F(1, 2), F(1, 2)), (F(1), F(1))))
say("L02/L03 f(3/5,2/5) mu=(1,1)", f_obj((F(3, 5), F(2, 5)), (F(1), F(1))), "expected -6/25")
say("Example 4.1 f(w*)", f_obj((F(1), F(0)), (F(3, 2), F(1, 5))), "expected -1/2")
say("Example 4.2 f(w*)", f_obj((F(1, 2), F(1, 2)), (F(1), F(1))), "expected -1/4")
say("M3 f(1/2,1/2) active", f_obj((F(1, 2), F(1, 2)), (F(3, 2), F(1, 5))), "expected -1/10")
say("E1 norm^2", F(1, 4) + F(1, 4), "norm", (F(1, 2)) ** 0.5, "sqrt2/2", 2**0.5 / 2)
inv = [[F(2, 3), F(-1, 3)], [F(-1, 3), F(2, 3)]]
mu = (F(3, 2), F(1, 5))
wu = (inv[0][0] * mu[0] + inv[0][1] * mu[1], inv[1][0] * mu[0] + inv[1][1] * mu[1])
say("Remark 4.3 w", [str(x) for x in wu], "sum", sum(wu), "expected 17/30")
nu = F(-1, 2)
say("Ex4.1 grad", (SIG[0][0] * 1 - mu[0], SIG[1][0] * 1 - mu[1]), "lambda2 = 4/5 + nu", F(4, 5) + nu)
d = (F(5, 3), F(-2, 3))
say("L02 M3 f(w*+d) with diag(1,2)", F(1, 2) * (F(25, 9) + 2 * F(4, 9)), "expected 11/6")
say("L02 M2 f(w*) diag(1,2)", F(1, 2) * (F(4, 9) * 1 + F(1, 9) * 2), "expected 1/3")

print("\n".join(out))
