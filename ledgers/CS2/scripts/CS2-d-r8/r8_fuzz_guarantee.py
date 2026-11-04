"""Round 8: fuzz the rank guarantee (Conventions) and Welford/rolling exactness of candidate streamstats modules.

usage: r8_fuzz_guarantee.py <module.py> [<module.py> ...]   (each run in its own process)
Guarantee: #{x < v} <= qn + eps*n and #{x <= v} >= qn - eps*n, exact Fractions of the floats passed (as in the grader).
"""
import importlib.util
import random
import sys
from fractions import Fraction

path = sys.argv[1]
spec = importlib.util.spec_from_file_location("cand", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
QuantileSketch = mod.QuantileSketch
rng = random.Random(8)
qs = [Fraction(k, 20) for k in range(21)] + [Fraction(1, 3), Fraction(2, 7), Fraction(1, 10), Fraction(9999, 10000)]
eps_list = [0.05, 0.1, 0.2, 0.3, 0.5, 0.9]
trials = 0
violations = []
for _ in range(1500):
    n = rng.randint(1, 60)
    kind = rng.random()
    if kind < 0.4:
        stream = [float(rng.randint(0, 20)) for _ in range(n)]          # heavy ties
    elif kind < 0.7:
        stream = [round(rng.uniform(-50, 50), 1) for _ in range(n)]     # one decimal
    else:
        stream = [rng.uniform(-1e6, 1e6) for _ in range(n)]
    if rng.random() < 0.2:
        stream.sort()
    eps = rng.choice(eps_list)
    sk = QuantileSketch(eps)
    for x in stream:
        sk.add(x)
    for q in qs:
        qf = float(q)
        v = sk.quantile(qf)
        trials += 1
        below = sum(1 for x in stream if x < v)
        at = sum(1 for x in stream if x <= v)
        qe = Fraction(qf)  # the exact rational of the float the grader passes (test_project.guarantee_holds)
        if not (below <= qe * n + Fraction(eps) * n and at >= qe * n - Fraction(eps) * n):
            violations.append((n, eps, str(q), v, below, at))
            break
    if len(violations) >= 3:
        break
print(f"{path.rsplit('/', 1)[-1]}: probes {trials}, guarantee violations found {len(violations)}")
for vi in violations[:3]:
    print("   violation (n, eps, q, v, below, at):", vi)
