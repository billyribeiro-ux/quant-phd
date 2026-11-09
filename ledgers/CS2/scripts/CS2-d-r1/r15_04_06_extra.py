"""Verifier r1: extra prefix-guarantee search for r15_04 and r15_06, with the reference as control.

Probes are the exact rationals of the floats the sketch receives, as the autograder computes them.
"""

import importlib.util
import itertools
import random
import sys
from bisect import bisect_left, bisect_right, insort
from fractions import Fraction

root = sys.argv[1]


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, f"{root}/{rel}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mods = {
    "reference": load("ref", "course/modules/CS/CS2/grader/reference.py"),
    "r15_04": load("m04", "ledgers/CS2/equivalent/r15_04_sketch_interior_delta_without_minus_one.py"),
    "r15_06": load("m06", "ledgers/CS2/equivalent/r15_06_sketch_interior_delta_is_floor_2en.py"),
}
PROBE_FLOATS = [k / 40 for k in range(41)]


def violations(mod, values, eps):
    sk = mod.QuantileSketch(eps)
    seen = []
    ee = Fraction(eps)
    bad = 0
    for n, x in enumerate(values, start=1):
        sk.add(x)
        insort(seen, float(x))
        last = None
        for qf in PROBE_FLOATS:
            v = sk.quantile(qf)
            q = Fraction(qf)
            if not (bisect_left(seen, v) <= q * n + ee * n and bisect_right(seen, v) >= q * n - ee * n):
                bad += 1
            if last is not None and v < last:
                bad += 1
            last = v
    return bad


for name, mod in mods.items():
    total = 0
    cases = 0
    for eps in (0.3, 0.2):
        for length in range(1, 8):
            for seq in itertools.product((0.0, 1.0, 2.0, 3.0), repeat=length):
                cases += 1
                total += violations(mod, list(seq), eps)
    print(name, "exhaustive small streams", cases, "violations", total)

rng = random.Random(7)
for name, mod in mods.items():
    total = 0
    cases = 0
    for t in range(120):
        eps = rng.choice((0.3, 0.2, 0.1))
        n = rng.randint(60, 160)
        vals = [round(rng.random() * 10, rng.choice((0, 1))) for _ in range(n)]
        if t % 3 == 0:
            vals = sorted(vals, reverse=bool(t % 2))
        cases += 1
        total += violations(mod, vals, eps)
    print(name, "random long streams", cases, "violations", total)
