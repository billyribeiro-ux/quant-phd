"""Independent recomputation of the Lab 1 (L01) hypothesis counts, exact arithmetic.

Grid: {-2..2}^2 (25 points), weights {0, 1/4, 1/2, 3/4, 1}. Q1, Q2 as on L01.html line 154.
"""
from fractions import Fraction as F
from itertools import product

Q1 = [[2, 1], [1, 2]]
Q2 = [[1, 2], [2, 1]]
pts = list(product(range(-2, 3), repeat=2))
ws = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]


def q(Q, x):
    return sum(Q[i][j] * x[i] * x[j] for i in range(2) for j in range(2))


def chord_fail(Q):
    fails = 0
    total = 0
    for x in pts:
        for y in pts:
            for t in ws:
                z = (t * x[0] + (1 - t) * y[0], t * x[1] + (1 - t) * y[1])
                total += 1
                if q(Q, z) > t * q(Q, x) + (1 - t) * q(Q, y):
                    fails += 1
    return fails, total


def gap_identity_holds(Q):
    ok = 0
    total = 0
    for x in pts:
        for y in pts:
            for t in ws:
                z = (t * x[0] + (1 - t) * y[0], t * x[1] + (1 - t) * y[1])
                gap = t * q(Q, x) + (1 - t) * q(Q, y) - q(Q, z)
                d = (x[0] - y[0], x[1] - y[1])
                total += 1
                if gap == t * (1 - t) * q(Q, d):
                    ok += 1
    return ok, total


neg_pairs = sum(1 for x in pts for y in pts if q(Q2, (x[0] - y[0], x[1] - y[1])) < 0)
f1, t1 = chord_fail(Q1)
f2, t2 = chord_fail(Q2)
print("ordered pairs", len(pts) ** 2, "weights", len(ws), "cases per function", t1)
print("Q1 chord failures:", f1, "of", t1)
print("Q2 chord failures:", f2, "of", t2)
print("ordered pairs with (x-y)'Q2(x-y) < 0:", neg_pairs)
print("3 x negative pairs:", 3 * neg_pairs, "equals Q2 failures:", 3 * neg_pairs == f2)
print("gap identity Q1:", gap_identity_holds(Q1), "Q2:", gap_identity_holds(Q2))
