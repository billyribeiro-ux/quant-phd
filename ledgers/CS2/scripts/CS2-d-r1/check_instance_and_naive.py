"""Verifier check (CS2-d round 1): instance offsets, distinct seeds, and the naive-variance mutant against the exact reference.

Usage: python -I check_instance_and_naive.py <checkout>
Prints the offset classes, the naive-formula failures per class, and the seed where the naive formula passes at offset 10,000.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "course/modules/CS/CS2/grader"))
from instance import make_instance  # noqa: E402

spec = importlib.util.spec_from_file_location("m01", root / "ledgers/CS2/mutants/m01_naive_sum_of_squares.py")
assert spec is not None and spec.loader is not None
naive_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(naive_mod)


def exact_sample_variance(values: list[float]) -> float:
    fr = [Fraction(x) for x in values]
    n = len(fr)
    mean = sum(fr) / n
    return float(sum((x - mean) ** 2 for x in fr) / (n - 1))


payloads = [make_instance(s)["payload"] for s in range(50)]
print("distinct payloads, seeds 0-49:", len(set(payloads)))
classes: dict[float, list[int]] = {}
passes_at_offset: list[tuple[int, float, float]] = []
for seed in range(50):
    values = [float(x) for x in json.loads(payloads[seed])["values"]]
    mean = sum(values) / len(values)
    offset = 0.0 if abs(mean) < 5000 else (10000.0 if abs(mean) < 500000 else 1000000.0)
    classes.setdefault(offset, []).append(seed)
    ev = exact_sample_variance(values)
    acc = naive_mod.WelfordAccumulator()
    for x in values:
        acc.update(x)
    a = acc.variance(1)
    ok = abs(a - ev) <= max(1e-9, 1e-9 * max(abs(a), abs(ev)))
    if offset > 0 and ok:
        passes_at_offset.append((seed, a, ev))
for offset in sorted(classes):
    seeds = classes[offset]
    print(f"offset class {offset:g}: {len(seeds)} seeds")
for seed, a, ev in passes_at_offset:
    print(f"naive variance passes the 1e-9 check at seed {seed}: naive {a!r}, exact {ev!r}, relative error {abs(a - ev) / ev:.3g}")
