"""Independent re-derivation for E3-d round 5 (own code; uses reference.py only as the engine under test)."""
import importlib.util
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

G = Path("/Users/billyribeiro/.fanout/wt/verifyC5-E3-d/course/modules/E/E3/grader")
sys.path.insert(0, str(G))
from instance import make_instance  # noqa: E402

spec = importlib.util.spec_from_file_location("ref", G / "reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)


def ce_prospect(prizes, probs, g, lam):
    tot = sum(float(p) * (x ** (1 - g) if x >= 0 else -lam * (-x) ** (1 - g)) for x, p in zip(prizes, probs))
    return tot ** (1 / (1 - g)) if tot >= 0 else -((-tot / lam) ** (1 / (1 - g)))


def ce_crra(prizes, probs, g, wealth):
    fin = [wealth + x for x in prizes]
    e = sum(float(p) * w ** (1 - g) for p, w in zip(probs, fin))
    return e ** (1 / (1 - g)) - wealth


def ans_of(rec):
    return ([int(x) for x in rec["prizes_a"]], [Fraction(s) for s in rec["probs_a"]],
            [int(x) for x in rec["prizes_b"]], [Fraction(s) for s in rec["probs_b"]], rec["choice"])


def loglik(A, g, lam, kap):
    t = 0.0
    for pa, qa, pb, qb, c in A:
        z = kap * (ce_prospect(pa, qa, g, lam) - ce_prospect(pb, qb, g, lam)) / 1e4
        t += -math.log1p(math.exp(-z)) if c == "A" else -math.log1p(math.exp(z))
    return t


def fit(A):
    """Independent fit: scipy BFGS in unconstrained coords from a grid start, then SE from finite-difference Hessian."""
    best = None
    for g0 in (0.1, 0.5, 0.8):
        for l0 in (1.0, 2.5):
            for k0 in (0.8, 2.0):
                x0 = np.array([math.log(g0 / (1 - g0)), math.log(l0), math.log(k0)])
                f = lambda x: -loglik(A, 1 / (1 + math.exp(-x[0])), math.exp(x[1]), math.exp(x[2]))
                r = minimize(f, x0, method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 20000})
                r = minimize(f, r.x, method="BFGS", options={"gtol": 1e-9})
                if best is None or r.fun < best.fun:
                    best = r
    return best.x, -best.fun


def info(theta, A, h=1e-4):
    def F(x):
        return loglik(A, 1 / (1 + math.exp(-x[0])), math.exp(x[1]), math.exp(x[2]))
    n = 3
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            ei = np.eye(n)[i] * h
            ej = np.eye(n)[j] * h
            H[i, j] = (F(theta + ei + ej) - F(theta + ei - ej) - F(theta - ei + ej) + F(theta - ei - ej)) / (4 * h * h)
    return -H


out = {}
# --- Lab 1 numbers
G1, L1, K1, W1 = 0.40, 2.00, 1.50, 100_000
pairs = [
    ([2000, -1000], [Fraction(1, 2), Fraction(1, 2)], [500], [Fraction(1)], "A"),
    ([3000], [Fraction(1)], [4000, -2000], [Fraction(1, 4), Fraction(3, 4)], "B"),
    ([1500, 2500], [Fraction(1, 3), Fraction(2, 3)], [-500, 3000], [Fraction(1, 2), Fraction(1, 2)], "A"),
]
tot = 0.0
for k, (pa, qa, pb, qb, c) in enumerate(pairs, 1):
    cra_a, cra_b = ce_crra(pa, qa, G1, W1), ce_crra(pb, qb, G1, W1)
    pr_a, pr_b = ce_prospect(pa, qa, G1, L1), ce_prospect(pb, qb, G1, L1)
    z = K1 * (pr_a - pr_b) / 1e4
    pA = 1 / (1 + math.exp(-z))
    lp = math.log(pA if c == "A" else 1 - pA)
    tot += lp
    print(f"lab1 pair {k}: crra raw A={cra_a:.6f} B={cra_b:.6f}; prospect raw A={pr_a:.6f} B={pr_b:.6f}; "
          f"P(A)={pA:.6f} logP(chosen)={lp:.6f}")
print(f"lab1 total={tot:.6f}")
# Lab 2
z = 2.0 * (1500 - 2200) / 1e4
print(f"lab2 logA={-math.log1p(math.exp(-z)):.9f} logB={-math.log1p(math.exp(z)):.9f} P(A)={1/(1+math.exp(-z)):.9f}")
