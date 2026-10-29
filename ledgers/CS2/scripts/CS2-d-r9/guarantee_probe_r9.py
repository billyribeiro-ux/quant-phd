"""Exact rank-guarantee probe: python -I guarantee_probe_r9.py <streamstats module path> ."""
import importlib.util, random, sys
from fractions import Fraction
spec = importlib.util.spec_from_file_location("ss", sys.argv[1])
ss = importlib.util.module_from_spec(spec); spec.loader.exec_module(ss)
rng = random.Random(9)
checks = viol = 0
probes = [0, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1]
for trial in range(400):
    n = rng.randint(1, 120)
    eps = rng.choice([0.05, 0.1, 0.2, 0.3])
    kind = trial % 3
    stream = [float(rng.randint(0, 50)) for _ in range(n)] if kind == 0 else (sorted(rng.random() for _ in range(n)) if kind == 1 else [float(i) for i in range(n)])
    sk = ss.QuantileSketch(eps)
    for x in stream:
        sk.add(x)
    for q in probes + [rng.random(), round(rng.random(), 7)]:
        v = sk.quantile(q)
        below = sum(1 for x in stream if x < v)
        at = sum(1 for x in stream if x <= v)
        qn = Fraction(q) * n; slack = Fraction(eps) * n
        checks += 1
        if not (below <= qn + slack and at >= qn - slack):
            viol += 1
print(f"checks {checks} violations {viol}")
