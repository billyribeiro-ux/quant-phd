"""Round-7 check of grader/instance.py over seeds 0-49: validity, label, and whether answers (not labels) differ."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("instance", ROOT / "course/modules/E/E2/grader/instance.py")
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
ref_spec = importlib.util.spec_from_file_location("reference", ROOT / "course/modules/E/E2/grader/reference.py")
assert ref_spec is not None and ref_spec.loader is not None
ref = importlib.util.module_from_spec(ref_spec)
ref_spec.loader.exec_module(ref)

answers = set()
bad = []
for seed in range(50):
    x = mod.make_instance(seed)
    n, k, v, b = x["n"], x["units"], x["values"], x["bids"]
    ok = x["label"] == "SIMULATED" and 2 <= n <= 5 and 1 <= k < n and len(v) == n == len(b)
    ok = ok and all(isinstance(a, int) and 0 <= a <= 10000 for a in v + b)
    if not ok:
        bad.append(seed)
    answers.add((n, k, ref.revenue("uniform", b, k), ref.revenue("discriminatory", b, k), ref.efficiency(v, b, k)))
print("invalid instances:", bad)
print("distinct (n,k,uniform rev,disc rev,efficiency) over seeds 0-49:", len(answers))
print("seed 0:", mod.make_instance(0))
print("seed 7:", mod.make_instance(7))
