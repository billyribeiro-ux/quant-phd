"""Re-derive the instance.py docstring counts: naive variance failures by offset, seeds 0-49 (exact Fraction reference).

Also prints each seed's offset group and whether the naive variance passes the suite's close() tolerance
(rel 1e-9, abs 1e-9). Run from the verifier checkout root with the grader directory on sys.path.
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from fractions import Fraction

sys.path.insert(0, "course/modules/CS/CS2/grader")
from instance import OFFSETS, make_instance  # type: ignore[import-not-found]  # the grader's own generator


def close(a: float, b: float, rel: float = 1e-9, absolute: float = 1e-9) -> bool:
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= max(absolute, rel * max(abs(a), abs(b)))


def exact_sample_variance(values: list[float]) -> Fraction:
    fr = [Fraction(x) for x in values]
    n = len(fr)
    mean = sum(fr, Fraction(0)) / n
    return sum(((x - mean) ** 2 for x in fr), Fraction(0)) / (n - 1)


def naive(values: list[float]) -> float:
    s = 0.0
    ss = 0.0
    for x in values:
        s += x
        ss += x * x
    n = len(values)
    mean = s / n
    return (ss - n * mean * mean) / (n - 1)


fails: Counter[float] = Counter()
total: Counter[float] = Counter()
passes_at_10000: list[int] = []
for seed in range(50):
    inst = make_instance(seed)
    payload = json.loads(inst["payload"])
    values = [float(v) for v in payload["values"]]
    offset = min(OFFSETS, key=lambda o: abs(o - (sum(values) / len(values))))
    ok = close(naive(values), float(exact_sample_variance(values)))
    total[offset] += 1
    if not ok:
        fails[offset] += 1
    if offset == 10_000.0 and ok:
        passes_at_10000.append(seed)
print("naive failures by offset:", {k: f"{fails[k]} of {total[k]}" for k in sorted(total)})
print("seeds at offset 10000 that pass:", passes_at_10000)
