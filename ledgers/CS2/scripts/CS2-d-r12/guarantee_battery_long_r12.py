"""Rank-guarantee battery: sketch module path argv[1]; random and tie-heavy streams; all q on a 101-grid (python -I)."""
import importlib.util
import random
import sys
from fractions import Fraction
from pathlib import Path

spec = importlib.util.spec_from_file_location("sk", Path(sys.argv[1]))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 7)
checks = 0
viol = 0
first = None
for trial in range(int(sys.argv[3]) if len(sys.argv) > 3 else 300):
    eps = rng.choice([0.05, 0.1, 0.2, 0.3, 0.5, 0.9])
    n = rng.randint(1, 400)
    kind = trial % 3
    if kind == 0:
        stream = [rng.uniform(-100, 100) for _ in range(n)]
    elif kind == 1:
        stream = [float(rng.randint(0, 3)) for _ in range(n)]
    else:
        stream = sorted(rng.uniform(0, 10) for _ in range(n))
    sk = mod.QuantileSketch(eps)
    for x in stream:
        sk.add(x)
    for k in range(101):
        q = k / 100
        v = sk.quantile(q)
        below = sum(1 for x in stream if x < v)
        at = sum(1 for x in stream if x <= v)
        qn = Fraction(q) * n
        sl = Fraction(eps) * n
        checks += 1
        if not (below <= qn + sl and at >= qn - sl):
            viol += 1
            if first is None:
                first = (trial, n, eps, q, v, below, at)
print("checks", checks, "violations", viol, "first", first)
