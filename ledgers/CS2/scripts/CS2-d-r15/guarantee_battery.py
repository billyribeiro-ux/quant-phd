"""Exact rank-guarantee battery for a streamstats-like module given by path (argv[1])."""
import importlib.util, random, sys
from fractions import Fraction
import math

path = sys.argv[1]
spec = importlib.util.spec_from_file_location("mod", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def check(values_in, eps_float, probes):
    sk = mod.QuantileSketch(eps_float)
    for x in values_in:
        sk.add(x)
    n = len(values_in)
    E = Fraction(eps_float)
    s = sorted(values_in)
    prev = None
    for q in sorted(probes):
        v = sk.quantile(q)
        Q = Fraction(q)
        below = sum(1 for y in values_in if y < v)
        atmost = sum(1 for y in values_in if y <= v)
        if not (below <= Q * n + E * n and atmost >= Q * n - E * n):
            return ("violation", q, below, atmost, n)
        if prev is not None and v < prev:
            return ("monotone", q)
        prev = v
    return None

PROBES = [0, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1]
rng = random.Random(7)
found = []
trials = 0
for trial in range(int(sys.argv[2]) if len(sys.argv) > 2 else 3000):
    n = rng.choice([1,2,3,4,5,6,7,8,10,12,15,20,30,40,60,100,200,400])
    eps = rng.choice([0.05, 0.1, 0.2])
    kind = rng.choice(["random","sorted","rev","repeat","offset"])
    if kind == "random":
        vals = [float(rng.randint(0, 50)) for _ in range(n)]
    elif kind == "sorted":
        vals = sorted(rng.random() for _ in range(n))
    elif kind == "rev":
        vals = sorted((rng.random() for _ in range(n)), reverse=True)
    elif kind == "repeat":
        vals = [float(rng.randint(0, 3)) for _ in range(n)]
    else:
        vals = [10000 + round(rng.random(), 1) for _ in range(n)]
    trials += 1
    r = check(vals, eps, PROBES + [rng.random()])
    if r is not None:
        found.append((n, eps, kind, r))
print(path.split("/")[-1], "trials", trials, "violations", len(found))
for f in found[:3]:
    print("  ", f)
