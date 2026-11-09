"""Check the QuantileSketch docstring invariants of grader/reference.py on random and tie-heavy streams (python -I)."""
import importlib.util
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

spec = importlib.util.spec_from_file_location("ref", Path(sys.argv[1]))
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)

checked_streams = 0
violations = {"sum_g": 0, "sorted": 0, "cap": 0, "rank_window": 0}
example = None
rng = random.Random(12345)
for trial in range(400):
    eps = rng.choice([0.05, 0.1, 0.2, 0.3, 0.5, 0.9])
    n_len = rng.randint(1, 120)
    kind = trial % 3
    if kind == 0:
        stream = [rng.uniform(-50, 50) for _ in range(n_len)]
    elif kind == 1:
        stream = [float(rng.randint(0, 4)) for _ in range(n_len)]
    else:
        stream = [round(rng.gauss(1e4, 3), 1) for _ in range(n_len)]
    s = ref.QuantileSketch(eps)
    seen = []
    for x in stream:
        s.add(x)
        seen.append(x)
        n = len(seen)
        vals, gs, ds = s._values, s._g, s._delta
        if sum(gs) != n:
            violations["sum_g"] += 1
        if any(vals[i] > vals[i + 1] for i in range(len(vals) - 1)):
            violations["sorted"] += 1
        cap = math.floor(2 * Fraction(eps) * n) + 1
        if any(g + d > cap for g, d in zip(gs, ds)):
            violations["cap"] += 1
        # each stored value: some copy's sorted 1-based rank lies in [S_i, S_i + delta_i], S_i = running sum of g
        running = 0
        for i, v in enumerate(vals):
            running += gs[i]
            lo = sum(1 for y in seen if y < v) + 1
            hi = sum(1 for y in seen if y <= v)
            if not (max(lo, running) <= min(hi, running + ds[i])):
                violations["rank_window"] += 1
                if example is None:
                    example = (eps, stream[:trial and 0] or None, i, v, running, ds[i], lo, hi, n)
                break
    checked_streams += 1
print("streams", checked_streams, "violations", violations)
print("first rank_window example (eps, _, index, value, S_i, delta_i, lo, hi, n):", example)
