"""Search for rank-guarantee violations of a streamstats candidate (verifier round 5).

usage: guarantee_search_r5.py <candidate.py>
Random streams (n 1..60, values with ties and offsets), eps in {0.05, 0.1, 0.2, 0.01, 0.37},
q on a grid of k/100 and on the ten probes. Reports the first witness found, or none.
"""
import importlib.util, random, sys
from fractions import Fraction

spec = importlib.util.spec_from_file_location("cand", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
rng = random.Random(5)
checked = 0
witness = None
for trial in range(4000):
    n = rng.randint(1, 60)
    eps = rng.choice([0.05, 0.1, 0.2, 0.01, 0.37])
    kind = rng.choice(["uniform", "ties", "sorted", "offset"])
    if kind == "uniform":
        vals = [rng.uniform(-5, 5) for _ in range(n)]
    elif kind == "ties":
        vals = [float(rng.randint(0, 4)) for _ in range(n)]
    elif kind == "sorted":
        vals = sorted(rng.uniform(0, 100) for _ in range(n))
    else:
        vals = [round(1e6 + rng.uniform(-5, 5), 1) for _ in range(n)]
    sk = mod.QuantileSketch(eps)
    for x in vals:
        sk.add(x)
    qs = [k / 100 for k in range(101)] + [rng.random() for _ in range(3)]
    for q in qs:
        v = sk.quantile(q)
        checked += 1
        below = sum(1 for x in vals if x < v)
        at_or_below = sum(1 for x in vals if x <= v)
        qn = Fraction(q) * n
        slack = Fraction(eps) * n
        if not (below <= qn + slack and at_or_below >= qn - slack):
            witness = dict(n=n, eps=eps, q=q, kind=kind, stream=vals, answer=v, below=below, at_or_below=at_or_below)
            break
    if witness:
        break
print("checked", checked, "queries")
if witness:
    print("VIOLATION", {k: witness[k] for k in ("n", "eps", "q", "kind", "answer", "below", "at_or_below")})
    print("stream", witness["stream"])
else:
    print("no violation found")
