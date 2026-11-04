"""Round 6 (M7-d): search small hand-built cases for an optimum whose inequality multipliers are all strictly positive
(the only case in which the dual-residual floor changes the value), using the reference allocator unchanged.
Also report whether any generated instance (seeds 0-49) has every inequality multiplier positive."""

import random
import sys
from fractions import Fraction as F

sys.path.insert(0, sys.argv[1])
import reference as ref  # noqa: E402  (the grader's reference, read-only)

def ineq(sol):
    return [*sol["lower"], *sol["upper"], *sol["sector"], *sol["plus"], *sol["minus"], sol["kappa"]]

rng = random.Random(6)
found = []
tries = 0
for _ in range(4000):
    n = rng.choice([2, 3])
    sector = [rng.randrange(2) for _ in range(n)]
    if len(set(sector)) < 2:
        sector[0], sector[-1] = 0, 1
    w0 = [F(1, n)] * n
    if rng.random() < 0.5:
        w0 = [F(rng.randint(1, 5), 10) for _ in range(n - 1)]
        w0.append(1 - sum(w0))
        if w0[-1] < 0:
            continue
    lower = [w0[i] if rng.random() < 0.6 else w0[i] - F(rng.randint(0, 3), 10) for i in range(n)]
    upper = [w0[i] if rng.random() < 0.6 else w0[i] + F(rng.randint(0, 3), 10) for i in range(n)]
    caps = [sum(w0[i] for i in range(n) if sector[i] == k) + F(rng.randint(0, 2), 10) for k in range(2)]
    mu = [F(rng.randint(-5, 20), 100) for _ in range(n)]
    sig = [[F(1, 10) if i == j else F(0) for j in range(n)] for i in range(n)]
    tau = F(rng.randint(0, 4), 10)
    case = {"gamma": F(rng.randint(1, 4)), "mu": mu, "sigma": [[float(x) for x in r] for r in sig],
            "w0": [float(x) for x in w0], "lower": [float(x) for x in lower], "upper": [float(x) for x in upper],
            "sector": sector, "sector_caps": [float(c) for c in caps], "turnover_limit": float(tau)}
    case["mu"] = [float(x) for x in mu]
    case["gamma"] = float(case["gamma"])
    try:
        out = ref.allocate(case)
    except (ValueError, TypeError, RuntimeError):
        continue
    tries += 1
    p = ref._parse(case)
    sol = ref._solve(p)
    vals = ineq(sol)
    if all(v > 0 for v in vals):
        found.append((case, [str(v) for v in vals]))
print("valid hand cases tried:", tries, "all-positive optima found:", len(found))
for case, vals in found[:2]:
    print(case)
    print("multipliers:", vals)
