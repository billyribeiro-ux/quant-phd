"""Round-8 verifier script: exact check of the rank guarantee (project.html Conventions) for a QuantileSketch module.

Usage: python -I guarantee_probe_r8.py <module.py>. Streams with repeats, sorted runs and probes with many decimals.
"""
import importlib.util, random, sys
from fractions import Fraction
from pathlib import Path

spec = importlib.util.spec_from_file_location("sk", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
rng = random.Random(8)
violations = []
trials = 0
for trial in range(1500):
    n = rng.randint(1, 120)
    eps = rng.choice([0.05, 0.1, 0.2, 0.3])
    kind = trial % 3
    if kind == 0:
        xs = [float(rng.randint(0, 5)) for _ in range(n)]          # heavy repeats
    elif kind == 1:
        xs = sorted(rng.random() for _ in range(n))               # sorted stream
    else:
        xs = [round(rng.random(), 2) for _ in range(n)]           # two-decimal values, repeats
    sk = mod.QuantileSketch(eps)
    for x in xs:
        sk.add(x)
    fe = Fraction(eps)
    for q in [0.0, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1.0, 0.5000004, 0.1000003, round(rng.random(), 9), rng.random()]:
        v = sk.quantile(q)
        fq = Fraction(q)
        n_ = len(xs)
        below = sum(1 for x in xs if x < v)
        atorbelow = sum(1 for x in xs if x <= v)
        trials += 1
        if not (below <= fq * n_ + fe * n_ and atorbelow >= fq * n_ - fe * n_):
            violations.append((n_, eps, q, v, below, atorbelow))
print(Path(sys.argv[1]).name, "checks", trials, "violations", len(violations))
for item in violations[:5]:
    print("  n, eps, q, v, below, at_or_below =", item)
