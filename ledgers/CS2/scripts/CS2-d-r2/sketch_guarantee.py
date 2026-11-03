"""Randomized and exhaustive-small check of the rank guarantee (project.html Conventions) for a QuantileSketch module.

Usage: python -I sketch_guarantee.py <path/to/streamstats_variant.py> [trials] [seed]
Checks the two inequalities with exact Fraction counts for every probe in a grid of k/100 plus random floats,
for epsilons in {0.01, 0.05, 0.1, 0.2, 0.3, 0.45, 0.7, 0.999}, on: random float streams, small-alphabet streams
with many ties, sorted and reversed streams, and every stream of length <= 7 over {0,1,2} (exhaustive).
Prints the number of streams, queries and violations, and the first violation if any.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from bisect import bisect_left, bisect_right
from fractions import Fraction
from pathlib import Path

path = Path(sys.argv[1]).resolve()
trials = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
spec = importlib.util.spec_from_file_location("variant", path)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
Sketch = mod.QuantileSketch

MODE = sys.argv[4] if len(sys.argv) > 4 else 'short'
EPSILONS = [0.01, 0.05, 0.1, 0.2, 0.3, 0.45, 0.7, 0.999]
rng = random.Random(seed)
streams_checked = 0
queries = 0
violations: list[str] = []


def check_stream(stream: list[float], eps: float, probes: list[float]) -> None:
    global streams_checked, queries
    sk = Sketch(eps)
    for x in stream:
        sk.add(x)
    srt = sorted(stream)
    n = len(stream)
    streams_checked += 1
    last = None
    for q in sorted(probes):
        v = sk.quantile(q)
        queries += 1
        below = bisect_left(srt, v)
        at_or_below = bisect_right(srt, v)
        qn = Fraction(q) * n
        slack = Fraction(eps) * n
        ok = below <= qn + slack and at_or_below >= qn - slack
        if last is not None and v < last:
            ok = False
        last = v
        if not ok and len(violations) < 5:
            violations.append(f"eps={eps} q={q!r} n={n} v={v!r} below={below} at_or_below={at_or_below} stream={stream}")


grid = [k / 100 for k in range(101)]
for _ in range(trials):
    n = rng.randint(1, 160) if MODE != 'big' else rng.randint(100, 400)
    kind = rng.choice(["float", "ties", "sorted", "reversed", "dec1"])
    if kind == "float":
        stream = [rng.uniform(-50, 50) for _ in range(n)]
    elif kind == "ties":
        stream = [float(rng.randint(0, 4)) for _ in range(n)]
    elif kind == "dec1":
        stream = [round(rng.uniform(-5, 5), 1) for _ in range(n)]
    elif kind == "sorted":
        stream = sorted(rng.uniform(0, 10) for _ in range(n))
    else:
        stream = sorted((rng.uniform(0, 10) for _ in range(n)), reverse=True)
    eps = rng.choice(EPSILONS)
    probes = grid + [rng.random() for _ in range(8)] + [0.0, 1.0]
    check_stream(stream, eps, probes)

# exhaustive over short streams on {0, 1, 2} with ties, every eps, every grid probe
for length in (range(1, 8) if MODE != 'big' else []):
    for combo in itertools.product([0.0, 1.0, 2.0], repeat=length):
        for eps in EPSILONS:
            check_stream(list(combo), eps, grid)

print(f"{path.name}: streams={streams_checked} queries={queries} violations={len(violations)}")
for line in violations:
    print("  VIOLATION", line)
