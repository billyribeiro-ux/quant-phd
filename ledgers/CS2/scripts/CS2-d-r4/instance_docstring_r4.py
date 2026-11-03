"""Round-4: re-derive the instance.py docstring counts (naive formula failures by offset) and the tie claim."""

from __future__ import annotations

import collections
import json
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "course/modules/CS/CS2/grader"))
from instance import OFFSETS, make_instance  # noqa: E402


def close(a: float, b: float) -> bool:
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= max(1e-9, 1e-9 * max(abs(a), abs(b)))


def exact_sample_var(values: list[float]) -> float:
    fr = [Fraction(x) for x in values]
    n = len(fr)
    mean = sum(fr, Fraction(0)) / n
    return float(sum(((x - mean) ** 2 for x in fr), Fraction(0)) / (n - 1))


fails: dict[float, list[int]] = collections.defaultdict(list)
totals: collections.Counter[float] = collections.Counter()
tie_by_decimals: dict[int, list[bool]] = collections.defaultdict(list)
for seed in range(50):
    rng = random.Random(seed)
    length = rng.randint(20, 400)
    offset = rng.choice(OFFSETS)
    decimals = rng.choice([1, 6])
    inst = make_instance(seed)
    payload = json.loads(inst["payload"])
    values = [float(x) for x in payload["values"]]
    assert len(values) == length
    s = 0.0
    ss = 0.0
    for x in values:
        s += x
        ss += x * x
    mean = s / len(values)
    naive = (ss - len(values) * mean * mean) / (len(values) - 1)
    totals[offset] += 1
    if not close(naive, exact_sample_var(values)):
        fails[offset].append(seed)
    tie_by_decimals[decimals].append(len(set(values)) < len(values))
for off in sorted(totals):
    print(f"offset {off:>10,.0f}: naive fails {len(fails[off])} of {totals[off]} seeds {fails[off]}")
for d in sorted(tie_by_decimals):
    t = tie_by_decimals[d]
    print(f"decimals {d}: streams {len(t)}, streams with a repeated value {sum(t)}")
