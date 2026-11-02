"""E3-e round 13: independent re-derivation of project Lab 3 numbers and the exemplar B instrument facts (python -I)."""
import sys, math, re
from fractions import Fraction
import numpy as np
from scipy.optimize import minimize

src = open(sys.argv[1], encoding="utf-8").read()
block = src[src.index("ANSWERS"):src.index("def value")]
ns = {"Fraction": Fraction}
exec("from typing import *\n" + block.replace(": list[tuple[int, str, list[int], list[str], list[int], list[str]]]", ""), ns)
ANS = ns["ANSWERS"]
print("answers", len(ANS))
prizes = [x for a in ANS for lot in (a[2], a[4]) for x in lot]
print("prize min max", min(prizes), max(prizes))
for a in ANS:
    for lot_p, lot_q in ((a[2], a[3]), (a[4], a[5])):
        assert sum(Fraction(q) for q in lot_q) == 1, a[0]
print("all probability vectors sum to exactly 1: True")
print("prizes per lottery", sorted({len(a[2]) for a in ANS} | {len(a[4]) for a in ANS}))
def mixed(a):
    for pr, pq in ((a[2], a[3]), (a[4], a[5])):
        if any(x > 0 and Fraction(p) > 0 for x, p in zip(pr, pq)) and any(x < 0 and Fraction(p) > 0 for x, p in zip(pr, pq)):
            return True
    return False
print("mixed count", sum(mixed(a) for a in ANS), "pairs without mixed", [a[0] for a in ANS if not mixed(a)])

def ce(prizes, probs, g, lam):
    def v(x):
        return x ** (1 - g) if x >= 0 else -lam * (-x) ** (1 - g)
    tot = sum(float(Fraction(p)) * v(x) for x, p in zip(prizes, probs))
    return tot ** (1 / (1 - g)) if tot >= 0 else -((-tot / lam) ** (1 / (1 - g)))

def ll(th):
    g = 1 / (1 + math.exp(-th[0])); lam = math.exp(th[1]); k = math.exp(th[2])
    s = 0.0
    for a in ANS:
        z = k * (ce(a[2], a[3], g, lam) - ce(a[4], a[5], g, lam)) / 1e4
        s += -math.log1p(math.exp(-z)) if a[1] == "A" else -math.log1p(math.exp(z))
    return s

best = None
for g0 in np.linspace(0.05, 0.95, 7):
    for l0 in (0.5, 1, 2, 4, 8):
        for k0 in (0.5, 2, 5):
            x0 = [math.log(g0 / (1 - g0)), math.log(l0), math.log(k0)]
            r = minimize(lambda t: -ll(t), x0, method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 20000})
            if best is None or r.fun < best.fun:
                best = r
th = best.x
g, lam, k = 1 / (1 + math.exp(-th[0])), math.exp(th[1]), math.exp(th[2])
print(f"independent NM: gamma {g:.6f} lambda {lam:.6f} kappa {k:.6f} logL {-best.fun:.6f}")

def hess(f, x, h=1e-4):
    n = len(x); H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            e_i = np.eye(n)[i] * h; e_j = np.eye(n)[j] * h
            H[i, j] = (f(x + e_i + e_j) - f(x + e_i - e_j) - f(x - e_i + e_j) + f(x - e_i - e_j)) / (4 * h * h)
    return H
Hn = -hess(ll, th)
cov = np.linalg.inv(Hn)
gr = g * (1 - g) * math.sqrt(cov[0, 0]); sl = lam * math.sqrt(cov[1, 1]); sk = k * math.sqrt(cov[2, 2])
print(f"independent SE: gamma {gr:.4f} lambda {sl:.4f} kappa {sk:.4f}")
