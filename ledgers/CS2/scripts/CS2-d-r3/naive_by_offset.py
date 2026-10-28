"""Verifier round 3: recount the instance docstring claims (offset groups, naive-formula failures) for seeds 0-49."""
import math
import random
import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1])
from instance import OFFSETS, make_instance  # noqa: E402

def offset_of(seed):
    rng = random.Random(seed)
    rng.randint(20, 400)
    return rng.choice(OFFSETS)

def close(a, b, rel=1e-9, absolute=1e-9):
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= max(absolute, rel * max(abs(a), abs(b)))

groups = {}
for seed in range(50):
    inst = make_instance(seed)
    import json
    vals = [float(x) for x in json.loads(inst["payload"])["values"]]
    off = offset_of(seed)
    n = len(vals)
    fr = [Fraction(x) for x in vals]
    mean_e = sum(fr) / n
    var_e = sum((x - mean_e) ** 2 for x in fr) / (n - 1)
    s = 0.0
    ss = 0.0
    for x in vals:
        s += x
        ss += x * x
    mean = s / n
    var_naive = (ss - n * mean * mean) / (n - 1)
    fails = not close(var_naive, float(var_e))
    g = groups.setdefault(off, [0, 0, []])
    g[0] += 1
    g[1] += fails
    if fails:
        g[2].append(seed)
    if seed == 41:
        print("seed 41 offset", off, "naive fails", fails)
for off, (tot, f, lst) in sorted(groups.items()):
    print(f"offset {off:g}: seeds {tot}, naive fails {f}, failing seeds {lst[:6]}...")
