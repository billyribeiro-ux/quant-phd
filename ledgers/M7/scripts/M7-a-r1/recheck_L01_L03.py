"""Independent recomputation of the numbers on M7 hub, L01, L02 and L03 (verifier round 1, slice M7-a).

Written from the page statements, not from the lab code. Standard library only.
"""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction as F
from itertools import product

# ---- L01 -------------------------------------------------------------------
G = [-2, -1, 0, 1, 2]
pts = list(product(G, G))
W = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]


def qf(Q, x):
    return sum(F(Q[i][j]) * x[i] * x[j] for i in range(2) for j in range(2))


Q1 = [[2, 1], [1, 2]]
Q2 = [[1, 2], [2, 1]]
cases = [(x, y, w) for x in pts for y in pts for w in W]
print("L01 cases", len(cases))
for name, Q in (("Q1", Q1), ("Q2", Q2)):
    ident = 0
    chord = 0
    for x, y, w in cases:
        z = (w * x[0] + (1 - w) * y[0], w * x[1] + (1 - w) * y[1])
        d = (x[0] - y[0], x[1] - y[1])
        lhs = w * qf(Q, x) + (1 - w) * qf(Q, y) - qf(Q, z)
        ident += lhs == w * (1 - w) * qf(Q, d)
        chord += lhs >= 0
    print(name, "identity", ident, "chord", chord)
neg = sum(1 for x, y in product(pts, repeat=2) if qf(Q2, (x[0] - y[0], x[1] - y[1])) < 0)
print("Q2 negative ordered pairs", neg, "failures", len(cases) - sum(1 for _ in []) if False else "")
fail_q2 = sum(1 for x, y, w in cases if not (lambda z: qf(Q2, z) <= w * qf(Q2, x) + (1 - w) * qf(Q2, y))(
    (w * x[0] + (1 - w) * y[0], w * x[1] + (1 - w) * y[1])))
print("Q2 chord failures", fail_q2, "= 3 x negative pairs:", fail_q2 == 3 * neg)
mid = qf(Q2, (F(1, 2), F(1, 2)))
print("Q2 midpoint of (1,0),(0,1):", mid, "chord", F(1, 2) * 1 + F(1, 2) * 1, "gap", F(1, 2) * 1 + F(1, 2) * 1 - mid)
print("Q2 quad at (1,-1):", qf(Q2, (1, -1)), "; Q2 eigen (1,-1)->", qf(Q2, (1, -1)) / 2)
print("Q1 midpoint of circle points squared norm:", F(1, 4) + F(1, 4))

# ---- L02 -------------------------------------------------------------------
def lcg(seed, count):
    s = seed
    out = []
    for _ in range(count):
        s = (1103515245 * s + 12345) % 2**31
        out.append(s % 7 - 3)
    return out


a = lcg(1, 9)
A = [a[0:3], a[3:6], a[6:9]]
Sig = [[sum(A[k][i] * A[k][j] for k in range(3)) + (1 if i == j else 0) for j in range(3)] for i in range(3)]
print("L02 A", a)
print("L02 Sigma", Sig)


def solve(M, b):
    n = len(b)
    R = [[F(M[i][j]) for j in range(n)] + [F(b[i])] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if R[r][c] != 0)
        R[c], R[p] = R[p], R[c]
        for r in range(n):
            if r != c and R[r][c] != 0:
                f = R[r][c] / R[c][c]
                R[r] = [x - f * y for x, y in zip(R[r], R[c])]
    return [R[i][n] / R[i][i] for i in range(n)]


u = solve(Sig, [1, 1, 1])
s = sum(u)
lam = 1 / s
w = [lam * x for x in u]
print("u", u, "s", s, "lambda", lam, "w", w, "sum", sum(w))
Sw = [sum(F(Sig[i][j]) * w[j] for j in range(3)) for i in range(3)]
print("Sigma w - lambda 1", [x - lam for x in Sw])
fw = sum(w[i] * Sw[i] for i in range(3)) / 2
print("f(w)", fw, "lambda/2", lam / 2)
# 4-place decimal of 177/55
q = Decimal(lam.numerator) / Decimal(lam.denominator)
print("177/55 decimal", q, "rounded half-up to 4 places:", q.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))
print("2/3 to 4 places:", (Decimal(2) / Decimal(3)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))
print("1/3 to 4 places:", (Decimal(1) / Decimal(3)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))
print("sqrt(1/2) to 4 places:", round(0.5 ** 0.5, 4))

# ---- L03 -------------------------------------------------------------------
S = [[F(2), F(1)], [F(1), F(2)]]


def obj(w, mu):
    sw = (S[0][0] * w[0] + S[0][1] * w[1], S[1][0] * w[0] + S[1][1] * w[1])
    return F(1, 2) * (w[0] * sw[0] + w[1] * sw[1]) - (mu[0] * w[0] + mu[1] * w[1])


for mu, label in (((F(3, 2), F(1, 5)), "active"), ((F(1), F(1)), "inactive")):
    vals = [(obj((F(k, 100), 1 - F(k, 100)), mu), F(k, 100)) for k in range(101)]
    m = min(vals)
    print(label, "grid min", m[0], "at w1", m[1])
# Example 4.1 closed form along budget line: f(t,1-t)
print("active: f(t,1-t) = t^2 - 23 t/10 + 4/5 check at t=1:", F(1) - F(23, 10) + F(4, 5))
print("inactive: f(t,1-t) = t^2 - t check at 1/2:", F(1, 4) - F(1, 2))
Sinv = [[F(1, 3) * 2, F(1, 3) * -1], [F(1, 3) * -1, F(1, 3) * 2]]
mu = (F(3, 2), F(1, 5))
w0 = (Sinv[0][0] * mu[0] + Sinv[0][1] * mu[1], Sinv[1][0] * mu[0] + Sinv[1][1] * mu[1])
print("Remark 4.3 Sigma^-1 mu", w0, "sum", w0[0] + w0[1])
print("P3 coefficient (Sw*-mu)'(-1,1) for w2 direction:", (F(1, 2)) * -1 + F(4, 5) * 1)
print("M3 objective at (1/2,1/2) mu=(3/2,1/5):", obj((F(1, 2), F(1, 2)), mu))
print("M2 f(3/5,2/5) mu=(1,1):", obj((F(3, 5), F(2, 5)), (F(1), F(1))))
print("E1 norm", (F(1, 4) + F(1, 4)) ** 0.5)
