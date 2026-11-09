# Verifier script (M7-b round 1): from-scratch recomputation of the L04 card numbers.
# Instance from tests/labs/M7/lab-M7-L04-1.py: Sigma = [[2,1],[1,2]], mu = (3/2, 1/5), budget 1'w = 1, w >= 0.
from fractions import Fraction as F
from itertools import product

S = [[F(2), F(1)], [F(1), F(2)]]
mu = [F(3, 2), F(1, 5)]
det = S[0][0] * S[1][1] - S[0][1] * S[1][0]
Sinv = [[S[1][1] / det, -S[0][1] / det], [-S[1][0] / det, S[0][0] / det]]


def quad(v, M):
    return sum(v[i] * M[i][j] * v[j] for i in range(2) for j in range(2))


def g(lam, nu):  # Example 2.2 closed form: g = -(1/2) r' Sinv r - nu, r = mu + lam - nu*1
    r = [mu[i] + lam[i] - nu for i in range(2)]
    return -F(1, 2) * quad(r, Sinv) - nu


def f(w):
    return F(1, 2) * quad(w, S) - sum(mu[i] * w[i] for i in range(2))


g00 = g([F(0), F(0)], F(0))
print("g(0,0) =", g00, "=", float(g00), "| p* - g(0,0) =", (F(-1, 2) - g00))  # c064: -199/300, 49/300
print("mu' Sinv mu =", sum(mu[i] * Sinv[i][j] * mu[j] for i in range(2) for j in range(2)))  # c064: 199/150
print("f(1,0) =", f([F(1), F(0)]), " g(0,3/10),-1/2 =", g([F(0), F(3, 10)], F(-1, 2)))  # c218
grid_nu = [F(-k, 10) for k in range(0, 11)]
best = max(g([F(0), F(0)], nu) for nu in grid_nu)
print("c060: max over lambda=(0,0), nu in {-1..0}/10 of g =", best, "; grid gap =", F(-1, 2) - best)  # expect 7/300
grid_dual = [F(k, 10) for k in range(0, 11)]
allg = [(g([a, b], nu), (a, b, nu)) for a, b in product(grid_dual, repeat=2) for nu in grid_nu]
print("dual points:", len(allg))
top = max(v for v, _ in allg)
print("largest dual value:", top, "attained at", [p for v, p in allg if v == top])  # c170
ws = [(F(k, 20), 1 - F(k, 20)) for k in range(21)]
print("primal points:", len(ws), "| weak duality pairs:", sum(1 for v, _ in allg for w in ws if v <= f(w)), "of", len(allg) * len(ws))  # c204
print("c213 grid gap:", min(f(w) for w in ws) - top)  # 0
print("c062 check: g at lam=(0,0) and nu=0 equals -1/2 * 199/150:", g00 == F(-1, 2) * F(199, 150))
