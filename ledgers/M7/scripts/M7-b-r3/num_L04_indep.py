"""Independent exact check of L04 numbers: Example 2.2, M3, P1, E1-E3, R3 and the Lab 1 grid counts."""
from fractions import Fraction as F

S = [[F(2), F(1)], [F(1), F(2)]]
SI = [[F(2, 3), F(-1, 3)], [F(-1, 3), F(2, 3)]]
MU = [F(3, 2), F(1, 5)]

def quad(M, v):
    return sum(v[i] * M[i][j] * v[j] for i in range(2) for j in range(2))

def g(lam, nu):
    r = [MU[0] + lam[0] - nu, MU[1] + lam[1] - nu]
    return -F(1, 2) * quad(SI, r) - nu

def f(w):
    return F(1, 2) * quad(S, w) - (MU[0] * w[0] + MU[1] * w[1])

print("M3 g(0,0)", g((F(0), F(0)), F(0)), "mu'Sinv mu", quad(SI, MU))
print("Ex2.2 g*", g((F(0), F(3, 10)), F(-1, 2)), "f(1,0)", f((F(1), F(0))))
print("R3 nu=-3/5", g((F(0), F(0)), F(-3, 5)), "nu=-7/10", g((F(0), F(0)), F(-7, 10)))
print("R3 continuous value at -13/20:", g((F(0), F(0)), F(-13, 20)))
grid_nu = [F(j - 10, 10) for j in range(11)]
best = max(g((F(0), F(0)), nu) for nu in grid_nu)
print("R3 restricted grid max", best, "grid gap", f((F(1), F(0))) - best)
print("E2 g(0,0) - p*", g((F(0), F(0)), F(0)) - F(-1, 2))
lams = [F(j, 10) for j in range(11)]
dual = [((a, b), nu) for a in lams for b in lams for nu in grid_nu]
prim = [(F(k, 20), F(20 - k, 20)) for k in range(21)]
print("dual points", len(dual), "primal", len(prim), "pairs", len(dual) * len(prim))
print("weak duality pairs holding", sum(1 for (l, n) in dual for w in prim if g(l, n) <= f(w)))
vals = [g(l, n) for (l, n) in dual]
mx = max(vals)
print("largest dual", mx, "attaining", sum(1 for v in vals if v == mx), "smallest primal", min(f(w) for w in prim))
print("grid gap", min(f(w) for w in prim) - mx)
