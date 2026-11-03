# Independent re-derivation of Lab 1 and Lab 3 numbers (no import of page code).
from fractions import Fraction as F
g = F(2)
S = [[F(4,100), F(1,100), F(0)], [F(1,100), F(9,100), F(2,100)], [F(0), F(2,100), F(16,100)]]
mu = [F(5,100), F(3,100), F(-2,100)]
# Budget-only: w = (mu - nu*1)/g ... solve g*S w = mu - nu*1, sum w = 1 by brute 2x2 elimination using Cramer on 4 unknowns
def solve(A, b):
    n = len(b); M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]
# unknowns (w1,w2,w3,nu): g*S w + nu*1 = mu ; sum w = 1
A = [[g*S[i][j] for j in range(3)] + [F(1)] for i in range(3)] + [[F(1),F(1),F(1),F(0)]]
b = mu + [F(1)]
x = solve(A, b)
print("budget-only w, nu:", [str(v) for v in x])
# Lab1 answer on face w3=0 with unknowns (w1,w2,lam3,nu)
w = [F(9,11), F(2,11), F(0)]; nu = F(-21,1100); lam3 = F(9,1100)
# stationarity: g*S w - mu + nu*1 - lam3*e3 = 0
res = [sum(g*S[i][j]*w[j] for j in range(3)) - mu[i] + nu - (lam3 if i == 2 else 0) for i in range(3)]
print("stationarity residual:", [str(r) for r in res], "budget gap:", str(sum(w)-1))
obj = g/2*sum(S[i][j]*w[i]*w[j] for i in range(3) for j in range(3)) - sum(mu[i]*w[i] for i in range(3))
print("objective:", str(obj), float(obj))
# global check: minimize over the simplex with w3=0 face and w3>0 region by dense grid of exact rationals (sanity)
best = None
import itertools
for a in range(0, 201):
    for c in range(0, 201 - a):
        w1 = F(a, 200); w2 = F(c, 200); w3 = 1 - w1 - w2
        if w3 < 0: continue
        ww = [w1, w2, w3]
        o = g/2*sum(S[i][j]*ww[i]*ww[j] for i in range(3) for j in range(3)) - sum(mu[i]*ww[i] for i in range(3))
        if best is None or o < best[0]: best = (o, ww)
print("grid min (step 1/200):", float(best[0]), [float(v) for v in best[1]], "vs answer", float(obj))
# Lab 3 candidates
def resid(w, nu, lo, up):
    prim = max([F(0), abs(sum(w)-1)] + [-x for x in w] + [x-1 for x in w])
    stat = max(abs(g*sum(S[i][j]*w[j] for j in range(3)) - mu[i] + nu - lo[i] + up[i]) for i in range(3))
    dual = max([F(0)] + [-x for x in lo] + [-x for x in up])
    comp = max([abs(lo[i]*w[i]) for i in range(3)] + [abs(up[i]*(w[i]-1)) for i in range(3)])
    return prim, stat, dual, comp
z = [F(0)]*3
print("A", [str(v) for v in resid(w, nu, [F(0),F(0),lam3], z)])
print("B", [str(v) for v in resid(w, nu, [F(0),F(0),-lam3], z)])
print("C", [str(v) for v in resid([F(9,11)+F(1,1000), F(2,11)-F(1,1000), F(0)], nu, [F(0),F(0),lam3], z)])
