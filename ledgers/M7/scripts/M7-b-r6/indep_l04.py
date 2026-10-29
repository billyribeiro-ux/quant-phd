"""Independent recomputation of the L04 Lab 1 grid numbers and the R3 grid example (exact Fractions, own code)."""
from fractions import Fraction as F
MU = (F(3, 2), F(1, 5)); S = ((F(2), F(1)), (F(1), F(2)))
det = S[0][0] * S[1][1] - S[0][1] * S[1][0]
Si = ((S[1][1] / det, -S[0][1] / det), (-S[1][0] / det, S[0][0] / det))
def q(m, v): return v[0] * (m[0][0] * v[0] + m[0][1] * v[1]) + v[1] * (m[1][0] * v[0] + m[1][1] * v[1])
def g(lam, nu):
    r = (MU[0] + lam[0] - nu, MU[1] + lam[1] - nu)
    return -F(1, 2) * q(Si, r) - nu
def f(w): return F(1, 2) * q(S, w) - (MU[0] * w[0] + MU[1] * w[1])
dual = [((F(a, 10), F(b, 10)), F(n, 10)) for a in range(11) for b in range(11) for n in range(-10, 1)]
prim = [(F(k, 20), 1 - F(k, 20)) for k in range(21)]
print("dual points", len(dual), "primal points", len(prim), "pairs", len(dual) * len(prim))
print("weak duality pairs holding", sum(g(l, n) <= f(w) for l, n in dual for w in prim))
gmax = max(g(l, n) for l, n in dual)
print("largest dual", gmax, "attained at", sum(g(l, n) == gmax for l, n in dual), "point(s)")
print("smallest primal", min(f(w) for w in prim), "grid gap", min(f(w) for w in prim) - gmax)
print("g(0,0)", g((F(0), F(0)), F(0)), "g(kkt)", g((F(0), F(3, 10)), F(-1, 2)), "f(1,0)", f((F(1), F(0))))
# R3: restrict to lambda=(0,0), nu in steps of 1/10 on [-1,0]
r3 = [g((F(0), F(0)), F(n, 10)) for n in range(-10, 1)]
print("R3 grid max over nu", max(r3), "at nu", [F(n, 10) for n in range(-10, 1) if g((F(0), F(0)), F(n, 10)) == max(r3)])
print("R3 gap", min(f(w) for w in prim) - max(r3))
print("R3 continuous g(0,-13/20)", g((F(0), F(0)), F(-13, 20)), "g(0,-3/5)", g((F(0), F(0)), F(-3, 5)), "g(0,-7/10)", g((F(0), F(0)), F(-7, 10)))
print("M3 g(0,0) == -199/300:", g((F(0), F(0)), F(0)) == F(-199, 300))
