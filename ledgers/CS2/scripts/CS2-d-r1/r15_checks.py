"""Verifier r1 checks of the three moved mutants (r15_04, r15_06, r15_07) against the page's stated behaviour.

Reads only files in the verifier checkout. Run as: python -I this.py <checkout>.
"""

import importlib.util
import math
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


ref = load("ref", "course/modules/CS/CS2/grader/reference.py")
m04 = load("m04", "ledgers/CS2/equivalent/r15_04_sketch_interior_delta_without_minus_one.py")
m06 = load("m06", "ledgers/CS2/equivalent/r15_06_sketch_interior_delta_is_floor_2en.py")
m07 = load("m07", "ledgers/CS2/equivalent/r15_07_welford_nan_checked_after_state_change.py")

print("== A. r15_07 Welford: NaN refused after state change")
for label, mod in (("reference", ref), ("r15_07", m07)):
    acc = mod.WelfordAccumulator()
    acc.update(5.0)
    try:
        acc.update(float("nan"))
        print(label, "update(nan) did not raise")
    except ValueError as e:
        print(label, "update(nan) raised ValueError:", e)
    print(label, "count", acc.count, "mean", acc.mean())
    try:
        v = acc.variance(1)
        print(label, "variance(1) with one value added returned", v)
    except ValueError as e:
        print(label, "variance(1) with one value added raised ValueError:", e)
    try:
        v0 = acc.variance(0)
        print(label, "variance(0) with one value added returned", v0)
    except ValueError as e:
        print(label, "variance(0) raised ValueError:", e)

print("== B. sketch rank guarantee after EVERY prefix (exact Fraction counts)")


def check_stream(mod, values, eps):
    sk = mod.QuantileSketch(eps)
    seen = []
    eps_exact = Fraction(eps)
    viol = 0
    probes = [Fraction(k, 40) for k in range(41)]
    for n, x in enumerate(values, start=1):
        sk.add(x)
        insort(seen, float(x))
        last = None
        for qf in probes:
            v = sk.quantile(float(qf))
            lo = bisect_left(seen, v)  # values strictly below v
            le = bisect_right(seen, v)  # values at or below v
            if not (lo <= qf * n + eps_exact * n and le >= qf * n - eps_exact * n):
                viol += 1
            if last is not None and v < last:
                viol += 1
            last = v
    return viol


def streams(rng, count):
    out = []
    for t in range(count):
        n = rng.randint(20, 120)
        kind = t % 5
        if kind == 0:
            vals = [round(rng.uniform(-1, 1), 1) for _ in range(n)]
        elif kind == 1:
            vals = sorted(round(rng.gauss(0, 1), 6) for _ in range(n))
        elif kind == 2:
            vals = sorted((round(rng.gauss(0, 1), 1) for _ in range(n)), reverse=True)
        elif kind == 3:
            vals = [float(rng.randint(0, 4)) for _ in range(n)]
        else:
            vals = [float(i // 3) + rng.choice([0.0, 0.5]) for i in range(n)]
        out.append(vals)
    return out


rng = random.Random(20260101)
data = streams(rng, 250)
for eps in (0.05, 0.1, 0.2):
    totals = {}
    for label, mod in (("reference", ref), ("r15_04", m04), ("r15_06", m06)):
        totals[label] = sum(check_stream(mod, vals, eps) for vals in data)
    print("eps", eps, "streams", len(data), "prefix-violations", totals)
