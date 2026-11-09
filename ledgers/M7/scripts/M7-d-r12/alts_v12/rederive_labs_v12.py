"""Independent re-derivation of the project page's Lab 1 and Lab 3 numbers, with Fractions, and a cross-check of Lab 1's
answer through the grader's reference solver (a separate code path; the reference takes the case as the grader does).

Usage: python -I rederive_labs_v12.py <repo_root>
"""

import sys
from fractions import Fraction as F
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "course/modules/M/M7/grader"))
from reference import allocate  # noqa: E402

gamma = F(2)
sigma = [[F(4, 100), F(1, 100), F(0)], [F(1, 100), F(9, 100), F(2, 100)], [F(0), F(2, 100), F(16, 100)]]
mu = [F(5, 100), F(3, 100), F(-2, 100)]


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


# Lab 1 by hand: stationarity 2 Sigma w - mu + nu 1 + ... ; budget; w3 = 0 (asset 3 held at zero).
# Unknowns: w1, w2, nu, lam3 with the stationarity of w1, w2, w3, budget and w3 = 0.
A = [
    [gamma * sigma[0][0], gamma * sigma[0][1], F(1), F(0)],
    [gamma * sigma[1][0], gamma * sigma[1][1], F(1), F(0)],
    [gamma * sigma[2][0], gamma * sigma[2][1], F(1), F(-1)],
    [F(1), F(1), F(0), F(0)],
]
b = [mu[0], mu[1], mu[2], F(1)]
w1, w2, nu, lam3 = solve(A, b)
w3 = F(0)
print("Lab 1 exact: w =", w1, w2, w3, "nu =", nu, "lam3 =", lam3)
assert (w1, w2, nu, lam3) == (F(9, 11), F(2, 11), F(-21, 1100), F(9, 1100))
# Budget-only weights: stationarity 2 Sigma w - mu + nu 1 = 0, sum = 1
M = [[gamma * sigma[i][j] for j in range(3)] + [F(1)] for i in range(3)] + [[F(1), F(1), F(1), F(0)]]
free = solve(M, [mu[0], mu[1], mu[2], F(1)])
print("Lab 1 budget-only weights:", free[:3])
assert free[:3] == [F(54, 65), F(5, 26), F(-3, 130)]
quad = sum(sigma[i][j] * w1 * w1 * 0 for i in range(3) for j in range(3))  # placeholder kept zero; recomputed below
w = [w1, w2, w3]
obj = gamma / 2 * sum(sigma[i][j] * w[i] * w[j] for i in range(3) for j in range(3)) - sum(mu[i] * w[i] for i in range(3))
print("Lab 1 objective exact:", obj, "float:", f"{float(obj):.6f}")
assert obj == F(-3, 220)
# Residuals of the four KKT fields at the Lab 1 answer, by hand definitions
stat = [gamma * sum(sigma[i][j] * w[j] for j in range(3)) - mu[i] + nu - (lam3 if i == 2 else 0) for i in range(3)]
print("Lab 1 stationarity:", stat)
assert all(s == 0 for s in stat)

# Lab 3 candidates: the page's residual definitions for the box problem.
lower = [F(0), F(0), lam3]
upper = [F(0), F(0), F(0)]


def resid(wv, budget, lo, up):
    primal = max([F(0), abs(sum(wv) - 1), *(-x for x in wv), *(x - 1 for x in wv)])
    stat_ = [gamma * sum(sigma[i][j] * wv[j] for j in range(3)) - mu[i] + budget - lo[i] + up[i] for i in range(3)]
    dual = max([F(0), *(-x for x in lo), *(-x for x in up)])
    comp = max([abs(lo[i] * wv[i]) for i in range(3)] + [abs(up[i] * (wv[i] - 1)) for i in range(3)])
    return primal, max(abs(s) for s in stat_), dual, comp


print("check A:", resid(w, nu, lower, upper))
print("check B:", resid(w, nu, [F(0), F(0), -lam3], upper))
moved = [w[0] + F(1, 1000), w[1] - F(1, 1000), w[2]]
print("check C:", resid(moved, nu, lower, upper))
assert resid(w, nu, lower, upper) == (0, 0, 0, 0)
assert resid(w, nu, [F(0), F(0), -lam3], upper) == (0, F(9, 550), F(9, 1100), 0)
assert resid(moved, nu, lower, upper) == (0, F(1, 6250), 0, 0)

# Reference cross-check: the Lab 1 problem as a grader case (sector cap 1, turnover limit 10, w0 uniform, upper 1).
case = {
    "label": "SIMULATED", "gamma": 2.0, "mu": [0.05, 0.03, -0.02],
    "sigma": [[0.04, 0.01, 0.0], [0.01, 0.09, 0.02], [0.0, 0.02, 0.16]],
    "w0": [1 / 3, 1 / 3, 1 / 3], "lower": [0.0, 0.0, 0.0], "upper": [1.0, 1.0, 1.0],
    "sector": [0, 0, 0], "sector_caps": [1.0], "turnover_limit": 10.0,
}
out = allocate(case)
print("reference on Lab 1 data: weights", out["weights"], "budget mult", out["multipliers"]["budget"],
      "lower", out["multipliers"]["lower"], "certificate", out["certificate"])
assert abs(out["weights"][0] - 9 / 11) < 1e-9 and abs(out["weights"][1] - 2 / 11) < 1e-9
print("re-derivation: all asserts passed")
