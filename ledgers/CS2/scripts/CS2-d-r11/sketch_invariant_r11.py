"""Round 11: check the reference.py docstring invariants of QuantileSketch on random streams (exact Fraction bounds).

Claims checked (course/modules/CS/CS2/grader/reference.py:95-100): (a) the g values sum to n; (b) g + delta never
exceeds floor(2 * epsilon * n) + 1 after every add; (c) for each stored tuple i, some copy of its value has exact rank r
with G_i <= r <= G_i + delta_i, where G_i is the running sum of g up to i and ranks count copies (1-based).
Usage: sketch_invariant_r11.py <solution.py> <trials>
"""
from __future__ import annotations

import importlib.util
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

path = Path(sys.argv[1]).resolve()
trials = int(sys.argv[2])
spec = importlib.util.spec_from_file_location("sol", path)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
rng = random.Random(11)
sum_bad = cap_bad = rank_bad = checked = 0
for _ in range(trials):
    eps = rng.choice([0.05, 0.1, 0.2, 0.3, 0.5, 0.9])
    n_total = rng.randint(1, 120)
    vals = [round(rng.uniform(0, 10), rng.choice([0, 1])) for _ in range(n_total)]
    sk = mod.QuantileSketch(eps)
    for n, x in enumerate(vals, start=1):
        sk.add(x)
        g, d, v = sk._g, sk._delta, sk._values
        checked += 1
        if sum(g) != n:
            sum_bad += 1
        cap = math.floor(2 * Fraction(eps) * n) + 1
        if any(gi + di > cap for gi, di in zip(g, d)):
            cap_bad += 1
        G = 0
        ok = True
        for i, (vi, gi, di) in enumerate(zip(v, g, d)):
            G += gi
            # exact copies of vi in the stream so far (ranks 1-based among sorted values)
            ss = sorted(vals[:n])
            lo = ss.index(vi) + 1
            hi = lo + ss.count(vi) - 1
            if not any(G <= r <= G + di for r in range(lo, hi + 1)):
                ok = False
        if not ok:
            rank_bad += 1
print(f"{path.name}: trials {trials}, adds checked {checked}, sum(g)!=n {sum_bad}, g+delta>cap {cap_bad}, rank-window breaks {rank_bad}")
