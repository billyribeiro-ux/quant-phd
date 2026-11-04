"""Round 8 (M7-d): independent checks of the generated instances (seeds 0-49) and of the page's Lab 1 and Lab 3 numbers.
Usage: python -I instances_labs_r8.py <repo-root>"""
import json
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "course/modules/M/M7/grader"))
from instance import make_instance  # noqa: E402

counts: Counter[int] = Counter()
payloads = set()
bad = []
for seed in range(50):
    c = json.loads(make_instance(seed)["payload"])
    n = len(c["mu"])
    counts[n] += 1
    payloads.add(json.dumps(c, sort_keys=True))
    ex = [[F(repr(v)) for v in row] for row in c["sigma"]]
    sym = all(ex[i][j] == ex[j][i] for i in range(n) for j in range(n))
    # Cholesky-style pivots for positive definiteness
    a = [row[:] for row in ex]
    pd = True
    for k in range(n):
        if a[k][k] <= 0:
            pd = False
            break
        for i in range(k + 1, n):
            f = a[i][k] / a[k][k]
            for j in range(k + 1, n):
                a[i][j] -= f * a[k][j]
    w0 = [F(repr(v)) for v in c["w0"]]
    lo = [F(repr(v)) for v in c["lower"]]
    up = [F(repr(v)) for v in c["upper"]]
    box = all(lo[i] <= w0[i] <= up[i] for i in range(n))
    budget = sum(w0) == 1
    caps = all(sum(w0[i] for i in range(n) if c["sector"][i] == k) <= F(repr(c["sector_caps"][k])) for k in range(len(c["sector_caps"])))
    sectors_used = sorted(set(c["sector"])) == list(range(len(c["sector_caps"])))
    gamma_ok = c["gamma"] > 0 and c["turnover_limit"] >= 0
    if not (sym and pd and box and budget and caps and sectors_used and gamma_ok and len(c["sector_caps"]) == 2):
        bad.append(seed)
print("asset counts over seeds 0-49:", dict(sorted(counts.items())))
print("distinct instances:", len(payloads), "of 50; invalid seeds:", bad)

# Lab 1 and Lab 3 numbers, recomputed with exact fractions (independent of the lab code).
G = F(2)
S = [[F(4, 100), F(1, 100), F(0)], [F(1, 100), F(9, 100), F(2, 100)], [F(0), F(2, 100), F(16, 100)]]
MU = [F(5, 100), F(3, 100), F(-2, 100)]


def solve(M, r):
    n = len(r)
    A = [M[i][:] + [r[i]] for i in range(n)]
    for c_ in range(n):
        p = next(i for i in range(c_, n) if A[i][c_] != 0)
        A[c_], A[p] = A[p], A[c_]
        for i in range(n):
            if i != c_ and A[i][c_] != 0:
                f = A[i][c_] / A[c_][c_]
                A[i] = [x - f * y for x, y in zip(A[i], A[c_])]
    return [A[i][n] / A[i][i] for i in range(n)]


# budget only: G S w + nu 1 = mu, sum w = 1 (unknowns w0,w1,w2,nu)
M = [[G * S[i][j] for j in range(3)] + [F(1)] for i in range(3)] + [[F(1), F(1), F(1), F(0)]]
sol = solve(M, MU + [F(1)])
print("lab1 budget-only weights:", [str(x) for x in sol[:3]], "nu:", str(sol[3]))
# constrained: w2 = 0 (held), unknowns w0,w1,nu,lambda
w = [F(9, 11), F(2, 11), F(0)]
nu = F(-21, 1100)
lam = F(9, 1100)
stat = [G * sum(S[i][j] * w[j] for j in range(3)) - MU[i] + nu - (lam if i == 2 else 0) for i in range(3)]
print("lab1 answer stationarity residuals:", [str(s) for s in stat], "budget gap:", str(sum(w) - 1))
obj = G / 2 * sum(S[i][j] * w[i] * w[j] for i in range(3) for j in range(3)) - sum(MU[i] * w[i] for i in range(3))
print("lab1 objective:", str(obj), float(obj))


def res(w, budget, lower, upper):
    primal = max([F(0), abs(sum(w) - 1)] + [-x for x in w] + [x - 1 for x in w])
    stat = [G * sum(S[i][j] * w[j] for j in range(3)) - MU[i] + budget - lower[i] + upper[i] for i in range(3)]
    dual = max([F(0)] + [-x for x in lower] + [-x for x in upper])
    comp = max([abs(lower[i] * w[i]) for i in range(3)] + [abs(upper[i] * (w[i] - 1)) for i in range(3)])
    return primal, max(abs(s) for s in stat), dual, comp


zero = [F(0)] * 3
print("lab3 A:", [str(x) for x in res(w, nu, [F(0), F(0), lam], zero)])
print("lab3 B:", [str(x) for x in res(w, nu, [F(0), F(0), -lam], zero)])
moved = [F(9, 11) + F(1, 1000), F(2, 11) - F(1, 1000), F(0)]
print("lab3 C:", [str(x) for x in res(moved, nu, [F(0), F(0), lam], zero)])

# Starting-weight sums: do the seed cases sum to exactly one in floats? (decides whether an in-place rescale can fire)
exact_sum = sum(1 for seed in range(50) if sum(json.loads(make_instance(seed)["payload"])["w0"]) == 1)
print("seed cases with float sum(w0) == 1 exactly:", exact_sum, "of 50")
