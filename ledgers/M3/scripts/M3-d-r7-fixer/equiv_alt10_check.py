"""Randomized check: reference projection_repair versus the alt10 candidate (no unit-diagonal correction).

Compares the returned matrices bit for bit over random symmetric inputs, for several max_iter values and the
default run, and reports the largest absolute difference and the count of inputs where the outputs differ.
"""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path
from types import ModuleType

REPO = Path("/Users/billyribeiro/dev/quant-phd")


def load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def random_symmetric(rng: random.Random, n: int) -> list[list[float]]:
    m = [[0.0] * n for _ in range(n)]
    for i in range(n):
        m[i][i] = 1.0
        for j in range(i + 1, n):
            v = rng.uniform(-0.95, 0.95)
            m[i][j] = v
            m[j][i] = v
    return m


def main() -> int:
    ref = load("ref", REPO / "course/modules/M/M3/grader/reference.py")
    alt = load("alt10", REPO / "ledgers/M3/equivalent/alt10_no_unit_diagonal_correction.py")
    rng = random.Random(20260704)
    trials = 0
    differing = 0
    worst = 0.0
    for n in (2, 3, 4, 5, 6):
        for _ in range(400):
            a = random_symmetric(rng, n)
            for max_iter in (1, 2, 3, 5, 500):
                r = ref.projection_repair(a, tol=0.0, max_iter=max_iter)
                b = alt.projection_repair(a, tol=0.0, max_iter=max_iter)
                trials += 1
                diff = max(abs(r[i][j] - b[i][j]) for i in range(n) for j in range(n))
                worst = max(worst, diff)
                if r != b:
                    differing += 1
    print(f"trials {trials}: outputs differing {differing}; largest absolute entry difference {worst!r}")
    return 0 if differing == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
