"""Independent re-derivation of every number on the M7 project page (Labs 1 to 3 and the Rung 3 worked claims).

Run: python -I ledgers/M7/scripts/M7-d-r14/recheck_project_numbers_r14.py <repo_root>
Uses only fractions and the reference allocator for the hand cases. Prints each claim and whether it holds.
"""

import sys
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "course/modules/M/M7/grader"))
import reference as ref  # noqa: E402

GAMMA = F(2)
SIGMA = [[F(4, 100), F(1, 100), F(0)], [F(1, 100), F(9, 100), F(2, 100)], [F(0), F(2, 100), F(16, 100)]]
MU = [F(5, 100), F(3, 100), F(-2, 100)]
N = 3
results = []


def check(name, cond):
    results.append((name, bool(cond)))
    print(("HOLDS " if cond else "FAILS ") + name)


def solve(matrix, rhs):
    size = len(rhs)
    rows = [[*matrix[i], rhs[i]] for i in range(size)]
    for col in range(size):
        pivot = next(r for r in range(col, size) if rows[r][col] != 0)
        rows[col], rows[pivot] = rows[pivot], rows[col]
        for r in range(size):
            if r != col and rows[r][col] != 0:
                factor = rows[r][col] / rows[col][col]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[col], strict=True)]
    return [rows[i][size] / rows[i][i] for i in range(size)]


def kkt(held):
    size = N + 1 + len(held)
    m = [[F(0)] * size for _ in range(size)]
    b = [F(0)] * size
    for i in range(N):
        for j in range(N):
            m[i][j] = GAMMA * SIGMA[i][j]
        m[i][N] = F(1)
        for c, j in enumerate(held):
            if i == j:
                m[i][N + 1 + c] = F(-1)
        b[i] = MU[i]
    for j in range(N):
        m[N][j] = F(1)
    b[N] = F(1)
    for c, j in enumerate(held):
        m[N + 1 + c][j] = F(1)
    s = solve(m, b)
    return s[:N], s[N], s[N + 1:]


free, _, _ = kkt([])
check("step1 budget-only weights are 54/65, 5/26, -3/130", free == [F(54, 65), F(5, 26), F(-3, 130)])
held = [i for i in range(N) if free[i] < 0]
check("step2 held set is [2]", held == [2])
w, nu, lam = kkt(held)
check("step3 weights 9/11, 2/11, 0", w == [F(9, 11), F(2, 11), F(0)])
check("step3 budget multiplier -21/1100", nu == F(-21, 1100))
check("step3 bound multiplier 9/1100", lam == [F(9, 1100)])
res = [GAMMA * sum(SIGMA[i][j] * w[j] for j in range(N)) - MU[i] + nu for i in range(N)]
res[2] -= lam[0]
check("step4 stationarity residuals all zero", all(r == 0 for r in res))
check("step5 budget gap zero", sum(w) - 1 == 0)
check("step5 min weight 0, max weight 9/11", min(w) == 0 and max(w) == F(9, 11))
check("step6 product w*lam for held asset is 0", w[2] * lam[0] == 0)
quad = sum(SIGMA[i][j] * w[i] * w[j] for i in range(N) for j in range(N))
obj = GAMMA / 2 * quad - sum(MU[i] * w[i] for i in range(N))
check("step7 objective exactly -3/220", obj == F(-3, 220))
check("step7 objective approx -0.013636 to 6 places", f"{float(obj):.6f}" == "-0.013636")
check("Lab1 prose: budget-only third weight is negative (-3/130)", free[2] < 0)
check("Lab1 prose: budget-only weights shown 54/65 = 0.8308 etc (rounded 4dp)", f"{float(free[0]):.4f}" == "0.8308")

# Lab 3 certificate for the three candidates (page's definitions restricted to budget and lower bounds)
def residuals(wv, budget, lower, upper):
    primal = max([F(0), abs(sum(wv, F(0)) - 1), *(-x for x in wv), *(x - 1 for x in wv)])
    stat = [GAMMA * sum((SIGMA[i][j] * wv[j] for j in range(N)), F(0)) - MU[i] + budget - lower[i] + upper[i] for i in range(N)]
    dual = max([F(0), *(-x for x in lower), *(-x for x in upper)])
    slack = [abs(lower[i] * wv[i]) for i in range(N)] + [abs(upper[i] * (wv[i] - 1)) for i in range(N)]
    return {"primal": primal, "stationarity": max(abs(s) for s in stat), "dual": dual, "complementary": max(slack)}

zero = [F(0)] * N
A = residuals(w, nu, [F(0), F(0), F(9, 1100)], zero)
B = residuals(w, nu, [F(0), F(0), -F(9, 1100)], zero)
moved = [F(9, 11) + F(1, 1000), F(2, 11) - F(1, 1000), F(0)]
C = residuals(moved, nu, [F(0), F(0), F(9, 1100)], zero)
check("Lab3 check A all four zero", all(v == 0 for v in A.values()))
check("Lab3 check B stationarity == 9/550", B["stationarity"] == F(9, 550))
check("Lab3 check B dual == 9/1100", B["dual"] == F(9, 1100))
check("Lab3 check B primal and complementary zero", B["primal"] == 0 and B["complementary"] == 0)
check("Lab3 check C stationarity == 1/6250", C["stationarity"] == F(1, 6250))
check("Lab3 check C primal, dual, complementary zero", C["primal"] == 0 and C["dual"] == 0 and C["complementary"] == 0)
r_moved = [GAMMA * sum(SIGMA[i][j] * moved[j] for j in range(N)) - MU[i] + nu - ([F(9, 1100)] if i == 2 else [F(0)])[0] for i in range(N)]
check("Lab3 interp: stationarity residual of the SECOND asset is -1/6250 (signed)", r_moved[1] == F(-1, 6250))
check("Lab3 interp: first asset residual is +3/50000 (0.00006)", r_moved[0] == F(3, 50000))
check("Lab3 interp: third asset residual is -1/25000 (-0.00004)", r_moved[2] == F(-1, 25000))
check("Lab3 interp: 2 x 9/1100 = 9/550", 2 * F(9, 1100) == F(9, 550))

# Hand cases quoted in the test-suite comments (reference allocator as oracle, checked against hand values)
def hand(**kw):
    base = {"gamma": 1.0, "sector": [0, 0], "sector_caps": [2.0], "turnover_limit": 2.0,
            "sigma": [[1.0, 0.0], [0.0, 1.0]], "lower": [-1.0, -1.0], "upper": [2.0, 2.0]}
    base.update(kw)
    return base

out = ref.allocate(hand(mu=[0.2, 0.5], w0=[0.8, 0.2], upper=[1.0, 1.0], turnover_limit=0.5))
check("test comment: without the 0.3 bound the turnover limit alone gives (0.55, 0.45)",
      abs(out["weights"][0] - 0.55) < 1e-9 and abs(out["weights"][1] - 0.45) < 1e-9)
out = ref.allocate(hand(mu=[0.2, 0.5], w0=[0.8, 0.2], upper=[1.0, 0.3], turnover_limit=0.5))
check("test comment: with the 0.3 bound the answer is (0.7, 0.3)",
      abs(out["weights"][0] - 0.7) < 1e-9 and abs(out["weights"][1] - 0.3) < 1e-9)
out = ref.allocate(hand(mu=[0.4, 0.0], w0=[0.5, 0.5], turnover_limit=0.2))
check("test comment: turnover binding answer (0.6, 0.4)",
      abs(out["weights"][0] - 0.6) < 1e-9 and abs(out["weights"][1] - 0.4) < 1e-9)
out = ref.allocate(hand(mu=[0.3, 0.1], w0=[0.5, 0.5]))
check("test comment: budget only (0.6, 0.4)", abs(out["weights"][0] - 0.6) < 1e-9 and abs(out["weights"][1] - 0.4) < 1e-9)

print()
print("TOTAL", len(results), "HOLDS", sum(1 for _, ok in results if ok), "FAILS", sum(1 for _, ok in results if not ok))
