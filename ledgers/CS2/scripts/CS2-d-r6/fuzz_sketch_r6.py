"""Fuzz the QuantileSketch guarantee (project page, Conventions) on random streams, exact Fraction counts.

Usage: python3 -I fuzz_sketch_r6.py <module_path> <trials> <seed>
Prints the number of guarantee violations and the first counterexample if any.
"""
import importlib.util
import math
import random
import sys
from bisect import bisect_left
from fractions import Fraction

path, trials, seed0 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
spec = importlib.util.spec_from_file_location("impl", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

violations = 0
checked = 0
first = None
for t in range(trials):
    rng = random.Random(seed0 * 1_000_003 + t)
    n = rng.randint(1, 400)
    eps = rng.choice([0.05, 0.1, 0.2, 0.01, 0.3, 0.45, 0.5, 0.9, 1e-6, 0.999999])
    kind = rng.choice(["uniform", "sorted", "desc", "ties", "gauss", "offset"])
    if kind == "uniform":
        xs = [round(rng.uniform(-5, 5), rng.choice([1, 6])) for _ in range(n)]
    elif kind == "sorted":
        xs = sorted(round(rng.uniform(-5, 5), 1) for _ in range(n))
    elif kind == "desc":
        xs = sorted((round(rng.uniform(-5, 5), 1) for _ in range(n)), reverse=True)
    elif kind == "ties":
        xs = [float(rng.randint(0, 3)) for _ in range(n)]
    elif kind == "gauss":
        xs = [rng.gauss(0, 1) for _ in range(n)]
    else:
        xs = [10_000 + round(rng.uniform(-5, 5), 1) for _ in range(n)]
    sk = mod.QuantileSketch(eps)
    for x in xs:
        sk.add(x)
    for q in [0.0, 1e-9, 0.01, 0.1, 0.25, 0.333, 0.5, 0.75, 0.9, 0.99, 1.0] + [rng.random() for _ in range(5)]:
        v = sk.quantile(q)
        qn = Fraction(q) * n
        slack = Fraction(eps) * n
        below = sum(1 for x in xs if x < v)
        at = sum(1 for x in xs if x <= v)
        checked += 1
        if not (below <= qn + slack and at >= qn - slack):
            violations += 1
            if first is None:
                first = (t, kind, n, eps, q, v, below, at, float(qn), float(slack))
print(f"module={path} trials={trials} checked={checked} violations={violations}")
if first:
    print("first counterexample (trial, kind, n, eps, q, answer, below, at_or_below, qn, slack):", first)
