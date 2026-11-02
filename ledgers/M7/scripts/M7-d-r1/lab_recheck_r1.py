"""Independent exact recheck of Lab 1 (KKT of the long-only allocation) and Lab 3 (three candidate certificates).

Usage: python3 -I lab_recheck_r1.py   (no inputs; prints the values the page quotes)
"""
from fractions import Fraction as F

g = F(2)
S = [[F(4, 100), F(1, 100), F(0)], [F(1, 100), F(9, 100), F(2, 100)], [F(0), F(2, 100), F(16, 100)]]
mu = [F(5, 100), F(3, 100), F(-2, 100)]
w = [F(9, 11), F(2, 11), F(0)]
nu = F(-21, 1100)
lam3 = F(9, 1100)
r = [g * sum(S[i][j] * w[j] for j in range(3)) - mu[i] + nu - (lam3 if i == 2 else 0) for i in range(3)]
print("lab1 stationarity", [str(x) for x in r], "budget gap", str(sum(w) - 1))
obj = g / 2 * sum(S[i][j] * w[i] * w[j] for i in range(3) for j in range(3)) - sum(mu[i] * w[i] for i in range(3))
print("lab1 objective", str(obj), round(float(obj), 6))


def res(wv, lower, upper, budget):
    primal = max([F(0), abs(sum(wv) - 1)] + [-x for x in wv] + [x - 1 for x in wv])
    st = [g * sum(S[i][j] * wv[j] for j in range(3)) - mu[i] + budget - lower[i] + upper[i] for i in range(3)]
    dual = max([F(0)] + [-x for x in lower] + [-x for x in upper])
    comp = max([abs(lower[i] * wv[i]) for i in range(3)] + [abs(upper[i] * (wv[i] - 1)) for i in range(3)])
    return [str(primal), str(max(abs(x) for x in st)), str(dual), str(comp)]


zero = [F(0)] * 3
print("check A", res(w, [F(0), F(0), lam3], zero, nu))
print("check B", res(w, [F(0), F(0), -lam3], zero, nu))
moved = [F(9, 11) + F(1, 1000), F(2, 11) - F(1, 1000), F(0)]
print("check C", res(moved, [F(0), F(0), lam3], zero, nu))
