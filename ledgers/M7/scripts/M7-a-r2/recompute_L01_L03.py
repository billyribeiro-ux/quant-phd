"""Independent recomputation (M7 slice a, round 2) of the numbers in L01-L03 prose, quiz and problem solutions.

Written separately from the lab twins: it re-derives each number from the formulas, with Fraction arithmetic.
Run: python -I -W error ledgers/M7/scripts/M7-a-r2/recompute_L01_L03.py  (exit 0 means every check passed).
"""

from __future__ import annotations

import itertools
from fractions import Fraction as F

fails: list[str] = []


def check(label: str, got: object, want: object) -> None:
    ok = got == want
    print(f"{'OK  ' if ok else 'FAIL'} {label}: got {got} want {want}")
    if not ok:
        fails.append(label)


def q(Q: list[list[int]], x: tuple[F, F]) -> F:
    return sum((F(Q[i][j]) * x[i] * x[j] for i in range(2) for j in range(2)), F(0))


def mix(l: F, x: tuple[F, F], y: tuple[F, F]) -> tuple[F, F]:
    return (l * x[0] + (1 - l) * y[0], l * x[1] + (1 - l) * y[1])


# ---- L01 lab numbers
Q1 = [[2, 1], [1, 2]]
Q2 = [[1, 2], [2, 1]]
grid = [(F(a), F(b)) for a in range(-2, 3) for b in range(-2, 3)]
weights = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
cases = [(x, y, w) for x in grid for y in grid for w in weights]
check("L01 cases per function", len(cases), 3125)
for name, Q in (("Q1", Q1), ("Q2", Q2)):
    ident = sum(
        q(Q, mix(w, x, y)) == w * q(Q, x) + (1 - w) * q(Q, y) - w * (1 - w) * q(Q, (x[0] - y[0], x[1] - y[1]))
        for x, y, w in cases
    )
    check(f"L01 {name} identity count", ident, 3125)
chord_q1 = sum(q(Q1, mix(w, x, y)) <= w * q(Q1, x) + (1 - w) * q(Q1, y) for x, y, w in cases)
chord_q2 = sum(q(Q2, mix(w, x, y)) <= w * q(Q2, x) + (1 - w) * q(Q2, y) for x, y, w in cases)
check("L01 Q1 chord count", chord_q1, 3125)
check("L01 Q2 chord count", chord_q2, 2573)
neg = sum(1 for x, y in itertools.product(grid, repeat=2) if q(Q2, (x[0] - y[0], x[1] - y[1])) < 0)
check("L01 Q2 negative ordered pairs", neg, 184)
check("L01 failures = 3 * negatives", (3125 - chord_q2) == 3 * neg, True)
check("L01 failures count 552", 3125 - chord_q2, 552)
x, y = (F(1), F(0)), (F(0), F(1))
check("L01 Q2 midpoint value", q(Q2, mix(F(1, 2), x, y)), F(3, 2))
check("L01 Q2 chord value", F(1, 2) * q(Q2, x) + F(1, 2) * q(Q2, y), F(1))
check("L01 Q2 gap = 1/4 (x-y)'Q2(x-y)", F(1, 4) * q(Q2, (F(1), F(-1))), F(-1, 2))
check("L01 (1,-1) Q2 form", q(Q2, (F(1), F(-1))), F(-2))
check("L01 (1,1) Q1 form", q(Q1, (F(1), F(1))), F(6))
check("L01 (2,2) Q1 form", q(Q1, (F(2), F(2))), F(24))


def trace_det(M: list[list[int]]) -> tuple[int, int]:
    return M[0][0] + M[1][1], M[0][0] * M[1][1] - M[0][1] * M[1][0]


# eigenvalues of a 2x2 symmetric matrix are the roots of t^2 - trace t + det
for label, M, eig in (
    ("H=2Q1", [[4, 2], [2, 4]], (6, 2)),
    ("H=2Q2", [[2, 4], [4, 2]], (6, -2)),
    ("Q1", Q1, (3, 1)),
    ("Q2", Q2, (3, -1)),
):
    tr, dt = trace_det(M)
    check(f"L01 {label} trace/det match eigenvalues {eig}", (tr, dt), (eig[0] + eig[1], eig[0] * eig[1]))
check("L01 2Q1 == H of Q1", [[2 * v for v in r] for r in Q1], [[4, 2], [2, 4]])
check("L01 2Q2 == H of Q2", [[2 * v for v in r] for r in Q2], [[2, 4], [4, 2]])
# R1 general identity: x'Qx = x1^2 + x2^2 for Q=[[1,1],[-1,1]]
for a, b in [(3, -5), (1, 2), (-4, 7)]:
    check(f"L01 R1 x'Qx at ({a},{b})", q([[1, 1], [-1, 1]], (F(a), F(b))), F(a * a + b * b))
# R3 check of eigen condition on a grid of symmetric matrices
ok_r3 = True
for a, b, c in itertools.product(range(-3, 4), repeat=3):
    # eigenvalues of [[a,b],[b,c]]: (a+c +- sqrt((a-c)^2+4b^2))/2; both >=0 iff a+c>=0 and ac-b^2>=0
    disc = (a - c) ** 2 + 4 * b * b
    both_nonneg = (a + c - disc**0.5) / 2 >= -1e-12 and (a + c + disc**0.5) / 2 >= -1e-12
    cond = a + c >= 0 and a * c - b * b >= 0
    if both_nonneg != cond:
        ok_r3 = False
        print("R3 counterexample", a, b, c)
check("L01 R3 equivalence on grid [-3,3]^3", ok_r3, True)

# ---- L02
# LCG seed 1: state=(1103515245*state+12345) mod 2^31 ; value = state % 7 - 3
state = 1
vals = []
for _ in range(9):
    state = (1103515245 * state + 12345) % 2**31
    vals.append(state % 7 - 3)
check("L02 A entries", vals, [1, 2, 3, 1, -1, 2, -1, -1, 0])
A = [vals[0:3], vals[3:6], vals[6:9]]
S = [[sum(A[k][i] * A[k][j] for k in range(3)) + (1 if i == j else 0) for j in range(3)] for i in range(3)]
check("L02 Sigma", S, [[4, 2, 5], [2, 7, 4], [5, 4, 14]])


def solve3(M: list[list[F]], b: list[F]) -> list[F]:
    # Cramer's rule, exact
    def det(m: list[list[F]]) -> F:
        return (
            m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
        )

    d = det(M)
    out = []
    for c in range(3):
        Mc = [[b[r] if k == c else M[r][k] for k in range(3)] for r in range(3)]
        out.append(det(Mc) / d)
    return out


SM = [[F(v) for v in row] for row in S]
u = solve3(SM, [F(1), F(1), F(1)])
total = sum(u)
check("L02 1'Sigma^-1 1", total, F(55, 177))
lam = 1 / total
check("L02 lambda", lam, F(177, 55))
w = [lam * t for t in u]
check("L02 w", w, [F(47, 55), F(17, 55), F(-9, 55)])
check("L02 budget", sum(w), F(1))
grad = [sum(SM[i][j] * w[j] for j in range(3)) for i in range(3)]
check("L02 Sigma w - lambda 1 zero", [g - lam for g in grad], [F(0)] * 3)
fw = sum(w[i] * grad[i] for i in range(3)) / 2
check("L02 f(w)", fw, F(177, 110))
check("L02 E1 first coordinate", 4 * w[0] + 2 * w[1] + 5 * w[2], F(177, 55))
# 36 of 36 claims over six directions and six steps
dirs = [(1, -1, 0), (0, 1, -1), (1, 0, -1), (2, -1, -1), (-1, 2, -1), (1, 1, -2)]
steps = [F(-1, 2), F(1, 2), F(1), F(-1), F(2), F(3, 2)]


def fq(v: list[F]) -> F:
    return sum(v[i] * grad[i] for i in range(3)) / 2 if False else sum(
        v[i] * sum(SM[i][j] * v[j] for j in range(3)) for i in range(3)
    ) / 2


ident = nonneg = 0
for d in dirs:
    dv = [F(t) for t in d]
    dsd = sum(dv[i] * sum(SM[i][j] * dv[j] for j in range(3)) for i in range(3))
    for t in steps:
        moved = [w[i] + t * dv[i] for i in range(3)]
        gap = fq(moved) - fw
        ident += gap == t * t * dsd / 2
        nonneg += gap >= 0
check("L02 increase identity count", ident, 36)
check("L02 increase nonneg count", nonneg, 36)
# Problem M2 diag(1,2)
check("L02 M2 f(w*)", F(1, 2) * (F(4, 9) * 1 + F(1, 9) * 2), F(1, 3))
# Problem M3 d=(1,-1) at w*=(2/3,1/3): increase 3/2
fd = F(1, 2) * ((F(5, 3)) ** 2 * 1 + (F(-2, 3)) ** 2 * 2)
check("L02 M3 f(w*+d)", fd, F(11, 6))
check("L02 M3 increase", fd - F(1, 3), F(3, 2))
# Quiz: lambda decimal to 4 places
check("L02 quiz lambda 3.2182", round(177 / 55, 4), 3.2182)
# misc: A=(2): 2*2+1
check("L02 quiz A^TA+I for A=2", 2 * 2 + 1, 5)
# P2 Sigma=0: all points zero
# R1 w3 negative
check("L02 w3 negative", w[2] < 0, True)

# ---- L03
SIG = [[2, 1], [1, 2]]


def f_obj(w2: tuple[F, F], mu: tuple[F, F]) -> F:
    return F(1, 2) * q(SIG, w2) - (mu[0] * w2[0] + mu[1] * w2[1])


muA = (F(3, 2), F(1, 5))
muB = (F(1), F(1))
check("L03 Ex4.1 f(w*)", f_obj((F(1), F(0)), muA), F(-1, 2))
check("L03 Ex4.2 f(w*)", f_obj((F(1, 2), F(1, 2)), muB), F(-1, 4))
check("L03 Ex4.1 grad", (F(2) - muA[0], F(1) - muA[1]), (F(1, 2), F(4, 5)))
check("L03 Ex4.2 grad", (F(3, 2) - muB[0], F(3, 2) - muB[1]), (F(1, 2), F(1, 2)))
check("L03 Ex4.1 lambda2", F(4, 5) - F(1, 2), F(3, 10))
check("L03 Ex4.1 dual residual flip", max(-F(-3, 10), F(0)), F(3, 10))
check("L03 M2 f(3/5,2/5)", f_obj((F(3, 5), F(2, 5)), muB), F(-6, 25))
check("L03 M3 grad at (1/2,1/2) active mu", (F(3, 2) - muA[0], F(3, 2) - muA[1]), (F(0), F(13, 10)))
check("L03 M3 f(1/2,1/2) active mu", f_obj((F(1, 2), F(1, 2)), muA), F(-1, 10))
# direct: Sigma^{-1} mu with Sigma^{-1} = (1/3)[[2,-1],[-1,2]]
inv = [[F(2, 3), F(-1, 3)], [F(-1, 3), F(2, 3)]]
w0 = (inv[0][0] * muA[0] + inv[0][1] * muA[1], inv[1][0] * muA[0] + inv[1][1] * muA[1])
check("L03 Remark4.3 Sigma^-1 mu", w0, (F(14, 15), F(-11, 30)))
check("L03 Remark4.3 sum 17/30", w0[0] + w0[1], F(17, 30))
# Lab 1 grid minimum: over k/100
best = min(((f_obj((F(k, 100), 1 - F(k, 100)), muA), k) for k in range(101)))
check("L03 active grid minimum value and k", best, (F(-1, 2), 100))
bestB = min(((f_obj((F(k, 100), 1 - F(k, 100)), muB), k) for k in range(101)))
check("L03 inactive grid minimum value and k", bestB, (F(-1, 4), 50))
# P3: f(w) >= -1/2 on feasible grid
check("L03 P3 bound on grid", all(f_obj((F(k, 100), 1 - F(k, 100)), muA) >= F(-1, 2) for k in range(101)), True)
# P3 identity: f(w) = -1/2 + (3/10) w2 + 1/2 d'Sigma d  for w=(1-w2,w2)
for w2 in [F(0), F(1, 3), F(1), F(-2)]:
    wv = (1 - w2, w2)
    lhs = f_obj(wv, muA)
    rhs = F(-1, 2) + F(3, 10) * w2 + F(1, 2) * q(SIG, (-w2, w2))
    check(f"L03 P3 expansion at w2={w2}", lhs, rhs)
# Problem M1 lower: f=x^2+y^2 min on x+y=1 is 1/2
check("L03 M1 p*", F(1, 2) ** 2 * 2, F(1, 2))
# Example 3.1, Problem R1 (L03): f=-x^2 on R
# Problem E1: norm of (-1/2,1/2)
check("L03 E1 norm squared", F(1, 4) + F(1, 4), F(1, 2))
# Remark: 0.7071
check("L03 E1 norm rounded", round((0.5) ** 0.5 * 1.0, 4), 0.7071)
# Problem M2 numeric 1-(-6/25) etc
check("L03 M2 -6/25 = -0.24", float(F(-6, 25)), -0.24)
# P1 example: -x^2 at midpoint 0 vs average -1
check("L03 P1 example", (F(0) > F(-1)), True)
# Misconception 1: (x^2-1)^2 KKT points
check("L03 (x^2-1)^2 at 0 is local max value 1 > 0", (0 ** 2 - 1) ** 2, 1)

print("FAILS:", fails)
raise SystemExit(1 if fails else 0)
