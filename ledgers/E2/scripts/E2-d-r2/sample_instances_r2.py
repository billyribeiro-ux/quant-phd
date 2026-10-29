"""Verifier round 2: sample 20 seeds of the autograder instance, check validity, and show the answers differ.

Usage (repository root): .venv/bin/python -I ledgers/E2/scripts/E2-d-r2/sample_instances_r2.py
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

GRADER = Path(__file__).resolve().parents[4] / "course/modules/E/E2/grader"


def load(name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, GRADER / f"{name}.py")
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


inst = load("instance")
ref = load("reference")
seeds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
valid = 0
rows = set()
for s in seeds:
    d = inst.make_instance(s)
    n, k, vals, bids = d["n"], d["units"], d["values"], d["bids"]
    ok = (2 <= n <= 5 and 1 <= k < n and len(vals) == n and len(bids) == n
          and all(isinstance(x, int) and 0 <= x <= 10000 for x in vals + bids) and d["label"] == "SIMULATED")
    valid += ok
    rev_u = ref.revenue("uniform", bids, k)
    rev_d = ref.revenue("discriminatory", bids, k)
    eff = ref.efficiency(vals, bids, k)
    rows.add((rev_u, rev_d, eff))
    print(f"seed {s:2d}: n={n} k={k} valid={ok} uniform_rev={rev_u} disc_rev={rev_d} efficiency={eff[0]}/{eff[1]}")
print(f"valid instances: {valid}/20; distinct (uniform_rev, disc_rev, efficiency) triples: {len(rows)}")
