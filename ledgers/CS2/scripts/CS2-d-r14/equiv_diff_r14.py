"""Differential check: ledgers/CS2/equivalent/rank_target_without_clamp.py against the reference on random streams.
The two must return identical answers for every (stream, epsilon, q). Usage: python -I equiv_diff_r14.py (checkout root)."""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load("ref_eq", ROOT / "course/modules/CS/CS2/grader/reference.py")
mut = load("mut_eq", ROOT / "ledgers/CS2/equivalent/rank_target_without_clamp.py")
rng = random.Random(77)
checks = diffs = 0
for trial in range(1500):
    eps = rng.choice([1e-6, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.9, 0.999999])
    n = rng.randint(1, 120)
    xs = [round(rng.uniform(-5, 5), rng.choice([0, 1, 6])) for _ in range(n)]
    a = ref.QuantileSketch(eps)
    b = mut.QuantileSketch(eps)
    for x in xs:
        a.add(x)
        b.add(x)
    for q in [0.0, 1e-9, 0.5, 1.0, *[rng.random() for _ in range(15)]]:
        checks += 1
        if a.quantile(q) != b.quantile(q):
            diffs += 1
print(f"equivalence differential: {checks} (stream, eps, q) checks, {diffs} differences")
sys.exit(1 if diffs else 0)
