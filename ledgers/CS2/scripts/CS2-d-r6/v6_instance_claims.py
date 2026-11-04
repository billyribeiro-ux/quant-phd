"""Round-6 check of the numeric claims in grader/instance.py (docstring): offset groups over seeds 0-49, naive formula
failures against the exact Fraction reference with the grader's tolerance, and the Welford pass count."""

import json
import math
import random
import sys
from collections import Counter
from fractions import Fraction

sys.path.insert(0, sys.argv[1])
from instance import OFFSETS, make_instance  # noqa: E402


def close(a: float, b: float, rel: float = 1e-9, absolute: float = 1e-9) -> bool:
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= max(absolute, rel * max(abs(a), abs(b)))


def exact_sample_var(vals):
    fr = [Fraction(x) for x in vals]
    n = len(fr)
    mean = sum(fr, Fraction(0)) / n
    return float(sum(((x - mean) ** 2 for x in fr), Fraction(0)) / (n - 1)), float(mean)


def naive(vals):
    n = len(vals)
    s = 0.0
    ss = 0.0
    for x in vals:
        s += x
        ss += x * x
    mean = s / n
    return (ss - n * mean * mean) / (n - 1)


def welford(vals):
    count, mean, m2 = 0, 0.0, 0.0
    for x in vals:
        count += 1
        delta = x - mean
        mean += delta / count
        m2 += delta * (x - mean)
    return m2 / (count - 1)


offset_count = Counter()
naive_fail = Counter()
naive_pass_seeds = []
welford_fail = []
offset_of = {}
for seed in range(50):
    inst = make_instance(seed)
    payload = json.loads(inst["payload"])
    vals = [float(x) for x in payload["values"]]
    # the offset drawn by make_instance: replay the rng calls exactly as make_instance does
    rng = random.Random(seed)
    rng.randint(20, 400)
    off = rng.choice(OFFSETS)
    offset_of[seed] = off
    offset_count[off] += 1
    exact_var, _ = exact_sample_var(vals)
    if not close(naive(vals), exact_var):
        naive_fail[off] += 1
    else:
        naive_pass_seeds.append((seed, off))
    if not close(welford(vals), exact_var):
        welford_fail.append(seed)

print("seeds per offset:", dict(sorted(offset_count.items())))
print("naive variance failures per offset:", dict(sorted(naive_fail.items())))
print("naive passing seeds (seed, offset):", naive_pass_seeds)
print("welford failing seeds:", welford_fail)
