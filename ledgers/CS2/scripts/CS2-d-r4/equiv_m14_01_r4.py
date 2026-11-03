"""Round-4: randomized equality check of the m14_01 equivalent (rank target without clamp) against the reference."""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


ref = load(ROOT / "course/modules/CS/CS2/grader/reference.py", "ref_mod")
alt = load(ROOT / "ledgers/CS2/equivalent/rank_target_without_clamp.py", "alt_mod")
rng = random.Random(14)
qs = [0.0, 1e-9, 0.01, 0.05, 0.1, 0.25, 0.25000004, 0.5, 0.75, 0.9, 0.99, 1.0]
eps_values = [1e-6, 0.05, 0.1, 0.2, 0.5, 0.999999]
pairs = 0
mismatch = 0
for _ in range(400):
    stream = [round(rng.uniform(-5, 5), rng.choice([0, 1, 3])) for _ in range(rng.randint(1, 60))]
    eps = rng.choice(eps_values)
    a, b = ref.QuantileSketch(eps), alt.QuantileSketch(eps)
    for x in stream:
        a.add(x)
        b.add(x)
    for q in qs + [rng.random() for _ in range(3)]:
        pairs += 1
        if a.quantile(q) != b.quantile(q):
            mismatch += 1
print(f"(stream, eps, q) triples compared: {pairs}; mismatches: {mismatch}")
