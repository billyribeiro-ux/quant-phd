"""Verifier script (M7-b round 1): independent recomputation of the numbers printed or stated in L04, L05 and L06.

Standard library only. Run with: python3 -I ledgers/M7/scripts/M7-b-r1/verify_numbers.py
"""
from fractions import Fraction as F
from itertools import product

def solve(a, b):
    """Gauss-Jordan on a copy, exact."""
    n = len(b)
    m = [list(map(F, row)) + [F(v)] for row, v in zip(a, b)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [x / piv for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] for i in range(n)]

def det(a):
    n = len(a)
    m = [list(map(F, r)) for r in a]
    d = F(1)
    for c in range(n):
        p = next((r for r in range(c, n) if m[r][c] != 0), None)
        if p is None:
            return F(0)
        if p != c:
            m[c], m[p] = m[p], m[c]
            d = -d
        d *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return d

print("=== L04 ===")
Sig = [[F(2), F(1)], [F(1), F(2)]]
mu = [F(3, 2), F(1, 5)]
Sinv = [[F(2, 3), F(-1, 3)], [F(-1, 3), F(2, 3)]]
assert [[sum(Sig[i][k] * Sinv[k][j] for k in range(2)) for j in range(2)] for i in range(2)] == [[1, 0], [0, 1]]
def g(lam, nu):
    r = [mu[i] + lam[i] - nu for i in range(2)]
    q = sum(r[i] * Sinv[i][j] * r[j] for i in range(2) for j in range(2))
    return -q / 2 - nu
def f(w):
    return sum(w[i] * Sig[i][j] * w[j] for i in range(2) for j in range(2)) / 2 - (mu[0] * w[0] + mu[1] * w[1])
lams = [F(j, 10) for j in range(11)]
nus = [F(j - 10, 10) for j in range(11)]
duals = [((a, b), n) for a in lams for b in lams for n in nus]
prim = [((F(k, 20), F(20 - k, 20))) for k in range(21)]
print("dual points", len(duals), "primal points", len(prim), "pairs", len(duals) * len(prim))
print("weak duality holds on", sum(1 for (l, n) in duals for w in prim if g(l, n) <= f(w)), "pairs")
mx = max(g(l, n) for l, n in duals)
print("max dual", mx, "attained at", [(l, n) for l, n in duals if g(l, n) == mx])
mn = min(f(w) for w in prim)
print("min primal", mn, "at", [w for w in prim if f(w) == mn])
print("grid gap", mn - mx)
print("g(0,0)", g((F(0), F(0)), F(0)), "gap below p*", F(-1, 2) - g((F(0), F(0)), F(0)))
print("g(kkt)", g((F(0), F(3, 10)), F(-1, 2)), "f(1,0)", f((F(1), F(0))))
# R3: lambda=0, nu grid in [-1,0]
r3 = [((F(0), F(0)), n) for n in nus]
mx3 = max(g(l, n) for l, n in r3)
print("R3 grid max", mx3, "at nu", [n for l, n in r3 if g(l, n) == mx3], "grid gap", mn - mx3)
# continuous max of g(0,nu)
best = max((g((F(0), F(0)), F(k, 10000)) , F(k, 10000)) for k in range(-10000, 1))
print("continuous max over nu approx", float(best[0]), "at nu approx", float(best[1]), "(expected -209/400 at -13/20)")
print("-209/400 =", float(F(-209, 400)), " g(0,-13/20) =", g((F(0), F(0)), F(-13, 20)))
print("Example 3.4 check: no need; M3 value", g((F(0), F(0)), F(0)) == F(-199, 300))

print("=== L05 ===")
QA = [[4, 1, 0], [1, 3, 1], [0, 1, 2]]
CA = [-1, 0, 2]
AA = [[1, 1, 1], [0, 1, -1]]
bA = [1, 0]
K = [QA[i] + [AA[0][i], AA[1][i]] for i in range(3)] + [AA[0] + [0, 0], AA[1] + [0, 0]]
print("KKT det", det(K))
sol = solve(K, [-c for c in CA] + bA)
print("x", sol[:3], "lambda", sol[3:])
x = sol[:3]
Qx = [sum(QA[i][j] * x[j] for j in range(3)) for i in range(3)]
obj = F(1, 2) * sum(x[i] * Qx[i] for i in range(3)) + sum(CA[i] * x[i] for i in range(3))
print("objective", obj, float(obj), "551/722 =", F(551, 722), float(F(551, 722)))
v = [-2, 1, 1]
print("A v", [sum(AA[r][i] * v[i] for i in range(3)) for r in range(2)], "v'Qv", sum(v[i] * QA[i][j] * v[j] for i in range(3) for j in range(3)))
print("R2.4 identity check at random points:", all(
    sum(QA[i][j] * y[i] * y[j] for i in range(3) for j in range(3))
    == (2 * y[0] + F(1, 2) * y[1]) ** 2 + F(11, 4) * (y[1] + F(4, 11) * y[2]) ** 2 + F(18, 11) * y[2] ** 2
    for y in [[F(a), F(b), F(c)] for a in range(-3, 4) for b in range(-3, 4) for c in range(-3, 4)]))
QB = [[2, 1], [1, 2]]
CB = [-3, 1]
best = None
for mask in product((0, 1), repeat=2):
    fixed = [i for i in range(2) if mask[i]]
    free = [i for i in range(2) if not mask[i]]
    xx = [F(0), F(0)]
    if free:
        sub = [[QB[i][j] for j in free] for i in free]
        sol2 = solve(sub, [-CB[i] for i in free])
        for p, val in zip(free, sol2):
            xx[p] = val
    grad = [sum(QB[i][j] * xx[j] for j in range(2)) + CB[i] for i in range(2)]
    ok = all(t >= 0 for t in xx) and all(grad[i] >= 0 for i in fixed)
    print("set", fixed, "x", [str(t) for t in xx], "passes", ok)
    if ok:
        best = xx
val = F(1, 2) * sum(best[i] * QB[i][j] * best[j] for i in range(2) for j in range(2)) + sum(CB[i] * best[i] for i in range(2))
print("Part B optimum", best, "value", val)
grid = [F(k, 16) for k in range(33)]
def fB(a, b):
    return F(1, 2) * (2 * a * a + 2 * a * b + 2 * b * b) + (-3 * a + b)
print("grid points below", sum(1 for a in grid for b in grid if fB(a, b) < val), "of", len(grid) ** 2)
print("float grid min", min(float(fB(a, b)) for a in grid for b in grid), "vs", float(val))

print("=== L06 ===")
class Lcg:
    def __init__(self, s):
        self.s = s
    def draw(self, m):
        self.s = (1103515245 * self.s + 12345) % 2**31
        return self.s % m
gen = Lcg(2026)
M = [[F(gen.draw(7) - 3) for _ in range(4)] for _ in range(4)]
mu6 = [F(gen.draw(13) + 2, 100) for _ in range(4)]
S6 = [[sum(M[k][i] * M[k][j] for k in range(4)) / 16 + (F(1, 10) if i == j else 0) for j in range(4)] for i in range(4)]
print("M", [[int(v) for v in r] for r in M])
print("mu", [str(v) for v in mu6])
print("Sigma diag", [str(S6[i][i]) for i in range(4)])
def fg(gam, w):
    return gam / 2 * sum(w[i] * S6[i][j] * w[j] for i in range(4) for j in range(4)) - sum(mu6[i] * w[i] for i in range(4))
def risk(w):
    return sum(w[i] * S6[i][j] * w[j] for i in range(4) for j in range(4))
def ret(w):
    return sum(mu6[i] * w[i] for i in range(4))
def eq_point(gam, idx):
    k = len(idx)
    A = [[gam * S6[idx[i]][idx[j]] for j in range(k)] + [F(1)] for i in range(k)] + [[F(1)] * k + [F(0)]]
    b = [mu6[i] for i in idx] + [F(1)]
    s = solve(A, b)
    return s[:k], s[k]
def best_nonneg(gam):
    kept = []
    for mask in product((0, 1), repeat=4):
        zeros = [i for i in range(4) if mask[i]]
        free = [i for i in range(4) if not mask[i]]
        if not free:
            continue
        wf, lam = eq_point(gam, free)
        w = [F(0)] * 4
        for p, v in zip(free, wf):
            w[p] = v
        Sw = [sum(S6[i][j] * w[j] for j in range(4)) for i in range(4)]
        nu = [gam * Sw[i] - mu6[i] + lam for i in range(4)]
        if all(t >= 0 for t in w) and all(nu[i] >= 0 for i in zeros):
            kept.append((tuple(zeros), w))
    return kept
GAM = [F(1), F(2), F(4), F(8), F(16)]
for gam in GAM:
    we, lam = eq_point(gam, [0, 1, 2, 3])
    kept = best_nonneg(gam)
    bestk = min(kept, key=lambda kw: fg(gam, kw[1]))
    print("gamma", gam, "eq ret %.10f risk %.10f obj %.10f" % (float(ret(we)), float(risk(we)), float(fg(gam, we))),
          "sum-1 exact", sum(we) == 1, "| kept", len(kept), "zero sets", [k for k, _ in kept],
          "| best zeros", bestk[0], "ret %.10f risk %.10f obj %.10f" % (float(ret(bestk[1])), float(risk(bestk[1])), float(fg(gam, bestk[1]))))
    if gam == 16:
        print("E2 unrounded difference nonneg-minus-eq objective at gamma 16:", float(fg(gam, bestk[1]) - fg(gam, we)), "exact", fg(gam, bestk[1]) - fg(gam, we))
    if gam == 4:
        w4 = bestk[1]
        print("gamma=4 constrained weights unrounded", [float(t) for t in w4])
        d = [w4[i] - F(1, 4) for i in range(4)]
        turn = sum(abs(t) for t in d)
        print("E3/C114 unrounded turnover at gamma 4:", float(turn), "exact", turn)
        print("E3 turnover from six-place printed weights:", sum(abs(F(s) - F(1, 4)) for s in ["0.389219", "0.220570", "0.390211", "0.000000"]), float(sum(abs(F(s) - F(1, 4)) for s in ["0.389219", "0.220570", "0.390211", "0.000000"])))
        print("printed weights gamma 4 equal-only sum", F("0.427439") + F("0.487002") + F("0.517706") + F("-0.432147"))
        print("printed risk/return/ obj at gamma 4 nonneg (exact):", float(ret(w4)), float(risk(w4)), float(fg(gam, w4)))
print("gamma 16 nonneg risk exact float %.9f" % float(risk(bestk[1])))
