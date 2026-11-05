"""Scratch check behind the scratch paragraph of ledgers/CS2/equivalent/README.md.

Runs the reference sketch and the three sketch variants (d8_01, d8_02, d9_04) on 200 seeded streams of up to 60
values (random, heavy ties, sorted and reversed runs, values rounded to one decimal), with epsilon in
{0.05, 0.1, 0.2, 0.3}. After every add it checks the sum of the g values against n, the first tuple (g = 1,
Delta = 0), and both rank inequalities of Conventions at 41 probes q = k/40, with exact Fraction counts.

Usage (from the repository root): .venv/bin/python -I ledgers/CS2/scripts/CS2-d-r9/readme_guarantee_check.py
"""

from __future__ import annotations

import importlib.util
import random
from fractions import Fraction
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[4]
FILES = {
    "reference": ROOT / "course/modules/CS/CS2/grader/reference.py",
    "d8_01": ROOT / "ledgers/CS2/equivalent/d8_01_sketch_cap_counts_previous_value.py",
    "d8_02": ROOT / "ledgers/CS2/equivalent/d8_02_sketch_insert_bisect_left.py",
    "d9_04": ROOT / "ledgers/CS2/equivalent/d9_04_sketch_cap_without_plus_one.py",
}
PROBES = [Fraction(k, 40) for k in range(41)]


def load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stream_of(rng: random.Random) -> list[float]:
    kind = rng.choice(["random", "ties", "sorted", "rounded"])
    n = rng.randint(1, 60)
    if kind == "random":
        return [rng.uniform(-5, 5) for _ in range(n)]
    if kind == "ties":
        return [float(rng.randint(0, 4)) for _ in range(n)]
    if kind == "sorted":
        xs = sorted(rng.uniform(-5, 5) for _ in range(n))
        return xs if rng.random() < 0.5 else xs[::-1]
    return [round(rng.uniform(-5, 5), 1) for _ in range(n)]


def main() -> None:
    for name, path in FILES.items():
        module = load("check_" + name, path)
        rng = random.Random(1234)
        pairs = 0
        violations = 0
        bookkeeping = 0
        for _ in range(200):
            stream = stream_of(rng)
            eps = rng.choice([0.05, 0.1, 0.2, 0.3])
            sketch = module.QuantileSketch(eps)
            seen: list[float] = []
            for x in stream:
                sketch.add(x)
                seen.append(x)
                n = len(seen)
                if sum(sketch._g) != n or sketch._g[0] != 1 or sketch._delta[0] != 0:
                    bookkeeping += 1
                big_e = Fraction(eps) * n
                for q in PROBES:
                    v = sketch.quantile(float(q))
                    pairs += 1
                    qn = Fraction(float(q)) * n
                    below = sum(1 for y in seen if y < v)
                    at_most = sum(1 for y in seen if y <= v)
                    if not (below <= qn + big_e and at_most >= qn - big_e):
                        violations += 1
        print(f"{name}: adds-probe pairs {pairs}, rank violations {violations}, bookkeeping failures {bookkeeping}")


if __name__ == "__main__":
    main()
