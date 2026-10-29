"""Verifier round 3 (E2-d): 20 sampled seeds of grader/instance.py are valid, and the answers differ across seeds.

Usage (repository root): .venv/bin/python -I ledgers/E2/scripts/E2-d-r3/sample_instances_r3.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("instance", ROOT / "course/modules/E/E2/grader/instance.py")
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sys.path.insert(0, str(ROOT / "course/modules/E/E2/grader"))
import reference as ref  # noqa: E402

seeds = [0, 1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 547272053, 7919]
answers = set()
for s in seeds:
    inst = mod.make_instance(s)
    n, k, v, b = inst["n"], inst["units"], inst["values"], inst["bids"]
    assert 2 <= n <= 5 and 1 <= k < n and len(v) == n == len(b), s
    assert all(0 <= x <= 10000 and isinstance(x, int) for x in v + b), s
    assert inst["label"] == "SIMULATED", s
    rev_u, rev_d = ref.revenue("uniform", b, k), ref.revenue("discriminatory", b, k)
    answers.add((n, k, tuple(ref.allocate(b, k)), rev_u, rev_d))
    print(s, "n", n, "k", k, "uniform rev", rev_u, "discr rev", rev_d, "won", ref.efficiency(v, b, k))
print("distinct answer tuples:", len(answers), "of", len(seeds))
