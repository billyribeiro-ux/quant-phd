"""Recompute the instance.py docstring claim: naive variance failures by offset, seeds 0-49."""
import sys
sys.path.insert(0, "/tmp/verifyB5-CS2-d/course/modules/CS/CS2/grader")
import json
from fractions import Fraction
from collections import Counter
from instance import make_instance, OFFSETS
import random

def offset_of(seed):
    rng = random.Random(seed)
    rng.randint(20, 400)
    return rng.choice(OFFSETS)

def naive(values):
    s = 0.0; ss = 0.0
    for x in values:
        s += x; ss += x * x
    n = len(values); mean = s / n
    return (ss - n * mean * mean) / (n - 1), mean

def exact(values):
    fr = [Fraction(x) for x in values]; n = len(fr)
    mean = sum(fr, Fraction(0)) / n
    return float(sum(((x - mean) ** 2 for x in fr), Fraction(0)) / (n - 1)), float(mean)

def close(a, b):
    return abs(a - b) <= max(1e-9, 1e-9 * max(abs(a), abs(b)))

groups = {}
for seed in range(50):
    inst = make_instance(seed)
    p = json.loads(inst["payload"])
    vals = [float(x) for x in p["values"]]
    off = offset_of(seed)
    assert off == OFFSETS[OFFSETS.index(off)]
    nv, nm = naive(vals)
    ev, em = exact(vals)
    fail = not close(nv, ev)
    groups.setdefault(off, []).append((seed, fail))
for off in OFFSETS:
    rows = groups.get(off, [])
    print(f"offset {off:g}: seeds {len(rows)}, naive fails {sum(f for _, f in rows)}, passes {[s for s, f in rows if not f]}")
