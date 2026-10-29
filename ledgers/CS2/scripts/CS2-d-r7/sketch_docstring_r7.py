"""Round-7 verifier script: check the reference QuantileSketch docstring's claims on random streams.

Claim (reference.py, QuantileSketch docstring): with n values added, the tuples hold the stored values in sorted
order, the g values sum to n, g + delta <= floor(2 eps n) + 1, and for each stored value some copy of it has an exact
rank between the running sum of g up to it and that sum plus its delta (ranks 1-based, over the n values added).
Also checks the two rank inequalities of the page for every probe after every add on the same streams.
"""

import random
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "course/modules/CS/CS2/grader"))
import reference as ref  # noqa: E402

rng = random.Random(7)
streams = adds = docstring_fail = guarantee_fail = invariant_fail = 0
for trial in range(300):
    eps = rng.choice([0.05, 0.1, 0.2, 0.5, 0.9, 1e-3])
    size = rng.randint(1, 200)
    kind = trial % 4
    if kind == 0:
        vals = [round(rng.uniform(-5, 5), 1) for _ in range(size)]  # ties
    elif kind == 1:
        vals = sorted(rng.uniform(0, 1) for _ in range(size))
    elif kind == 2:
        vals = [float(rng.randint(0, 3)) for _ in range(size)]
    else:
        vals = [rng.random() * 1e6 + 1e9 for _ in range(size)]
    sk = ref.QuantileSketch(eps)
    seen = []
    streams += 1
    for x in vals:
        sk.add(x)
        seen.append(x)
        adds += 1
        n = len(seen)
        ex = sk._exact_epsilon
        if sum(sk._g) != n:
            invariant_fail += 1
        cap = 2 * ex * n
        if any(g + d > (int(cap) if cap == int(cap) else int(cap)) + 1 for g, d in zip(sk._g, sk._delta)):
            invariant_fail += 1
        # docstring: for each stored value, some copy has rank in [G_i, G_i + delta_i]
        run = 0
        srt = sorted(seen)
        for v, g, d in zip(sk._values, sk._g, sk._delta):
            run += g
            ranks = [r for r in range(1, n + 1) if srt[r - 1] == v]
            if not any(run <= r <= run + d for r in ranks):
                docstring_fail += 1
                break
        # the page's guarantee after this add, for probes 0, 0.01, ..., 1 and a few more
        for q in [0.0, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1.0, rng.random()]:
            v = sk.quantile(q)
            below = sum(1 for z in seen if z < v)
            at_or_below = sum(1 for z in seen if z <= v)
            if not (below <= Fraction(q) * n + ex * n and at_or_below >= Fraction(q) * n - ex * n):
                guarantee_fail += 1
print("streams", streams, "adds", adds)
print("invariant failures (sum g = n, g + delta <= floor(2 eps n)+1):", invariant_fail)
print("docstring rank-interval failures:", docstring_fail)
print("guarantee failures at probes after every add:", guarantee_fail)
