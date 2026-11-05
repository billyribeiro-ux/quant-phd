"""Exhaustive generator-domain check, literal-sign bitwise check and seed spread (round 10).

Run: python3 -I domain_and_bitwise_r10.py <repo-root>  (imports solver/instance from a scratch dir passed as argv[2])
"""
import math
import random
import sys
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
sys.path.insert(0, str(scratch))
import instance  # noqa: E402
import lit  # noqa: E402
import solver  # noqa: E402

A, TV, TE = 2.0, 1.0, 1.0


def g0(sd, c):
    u = math.pow(1 + A * A * sd * sd / TV, -0.5)
    i = math.pow(1 + TE / TV + (TV + TE) * A * A * sd * sd / (TV * TV), -0.5)
    return u - math.exp(A * c) * i


bad = []
n = 0
for i in range(251):
    sd = round(0.5 + 0.001 * i, 3)
    for j in range(31):
        c = round(0.120 + 0.001 * j, 3)
        n += 1
        o = solver.solve_model(sd, c)
        if not (0.0 < o["informed_fraction"] < 1.0):
            bad.append((sd, c))
print("generator domain points:", n, "points whose solver fraction is not interior:", len(bad))

# seed spread over 0..49
vals = [(instance.make_instance(s)["noise_sd"], instance.make_instance(s)["info_cost"]) for s in range(50)]
print("seeds 0-49: distinct instances", len(set(vals)), "noise_sd", min(v[0] for v in vals), max(v[0] for v in vals),
      "cost", min(v[1] for v in vals), max(v[1] for v in vals))

random.seed(10)
diff = 0
worst = 0.0
for _ in range(3000):
    sd = random.uniform(0.05, 3.0)
    c = random.uniform(0.0, 0.4)
    a = solver.solve_model(sd, c)
    b = lit.solve_model(sd, c)
    for k in a:
        if a[k] != b[k]:
            diff += 1
            worst = max(worst, abs(a[k] - b[k]))
print("literal price-sign variant: 3000 random inputs, bitwise-different outputs", diff, "worst abs diff", worst)

extremes = [1e-300, 1e-12, 0.6, 1.0, 50.0, 1e75, 1e150]
costs = [0.0, 0.13, 1.0, 10.0, 350.0]
ok = 0
for sd in extremes:
    for c in costs:
        o = solver.solve_model(sd, c)
        if all(math.isfinite(v) for v in o.values()) and 0 <= o["informed_fraction"] <= 1 and 0 <= o["price_informativeness"] <= 1:
            ok += 1
print("exception-range probe: finite and in range", ok, "of", len(extremes) * len(costs))
