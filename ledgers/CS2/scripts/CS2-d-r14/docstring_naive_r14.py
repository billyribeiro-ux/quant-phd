"""Re-derives the instance.py docstring counts (naive formula, variance alone and mean alone) and the Lab 1 deque
operation count with an independent implementation. Usage: python -I docstring_naive_r14.py (checkout root)."""

from __future__ import annotations

import importlib.util
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("inst_r14c", ROOT / "course/modules/CS/CS2/grader/instance.py")
assert spec and spec.loader
inst = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inst)


def close(a: float, b: float) -> bool:
    return abs(a - b) <= max(1e-9, 1e-9 * max(abs(a), abs(b)))


groups: dict[float, list[int]] = {}
fails_var: dict[float, list[int]] = {}
fails_mean: dict[float, list[int]] = {}
for seed in range(50):
    d = inst.make_instance(seed)
    vals = [float(x) for x in json.loads(d["payload"])["values"]]
    # offset: the grader's own make_instance draw order, read from the first value's group (offset in OFFSETS)
    import random

    rng = random.Random(seed)
    rng.randint(20, 400)
    off = rng.choice(inst.OFFSETS)
    groups.setdefault(off, []).append(seed)
    fr = [Fraction(x) for x in vals]
    n = len(fr)
    mean_e = sum(fr) / n
    var_e = sum(((x - mean_e) ** 2 for x in fr), Fraction(0)) / (n - 1)
    s = 0.0
    ss = 0.0
    for x in vals:
        s += x
        ss += x * x
    naive_mean = s / n
    naive_var = (ss - n * naive_mean * naive_mean) / (n - 1)
    if not close(naive_var, float(var_e)):
        fails_var.setdefault(off, []).append(seed)
    if not close(naive_mean, float(mean_e)):
        fails_mean.setdefault(off, []).append(seed)
for off in sorted(groups):
    print(f"offset {off:g}: seeds {len(groups[off])}; naive variance fails {len(fails_var.get(off, []))}; naive mean fails {len(fails_mean.get(off, []))}")
print("seed 41 in offset-10000 group and variance-passing:", 41 in groups[10000.0], 41 not in fails_var.get(10000.0, []))

# Lab 1 deque operations, independent count (pushes and pops over both deques)
series = []
import random as _r

rr = _r.Random(12)
series = [rr.randint(0, 99) for _ in range(12)]
W = 4
mins: list[tuple[int, int]] = []
maxs: list[tuple[int, int]] = []
ops = 0
for i, x in enumerate(series):
    while mins and mins[-1][1] >= x:
        mins.pop(); ops += 1
    mins.append((i, x)); ops += 1
    while maxs and maxs[-1][1] <= x:
        maxs.pop(); ops += 1
    maxs.append((i, x)); ops += 1
    while mins and mins[0][0] <= i - W:
        mins.pop(0); ops += 1
    while maxs and maxs[0][0] <= i - W:
        maxs.pop(0); ops += 1
print("lab1 series", series, "deque ops", ops, "bound 4n", 4 * len(series))
