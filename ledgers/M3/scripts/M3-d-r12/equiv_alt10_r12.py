"""Round-12 verifier (M3 slice d): randomized bitwise check that ledgers/M3/equivalent/alt10_no_unit_diagonal_correction.py
returns exactly the reference's projection_repair output, for max_iter in {1, 2, 3, 5, 500} with tol = 0 and for the
default arguments. Loads both files from the checkout (the working directory), not from another checkout. Run from the
checkout root with python -I."""

import importlib.util
import os
import random
import sys
from types import ModuleType

ROOT = os.getcwd()


def load(name: str, rel: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
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


ref = load("ref", "course/modules/M/M3/grader/reference.py")
alt = load("alt10", "ledgers/M3/equivalent/alt10_no_unit_diagonal_correction.py")
rng = random.Random(20261105)
trials = 0
differing = 0
per_size = int(sys.argv[1]) if len(sys.argv) > 1 else 40
for n in (2, 3, 4, 5, 6):
    for _ in range(per_size):
        a = random_symmetric(rng, n)
        runs = [dict(tol=0.0, max_iter=k) for k in (1, 2, 3, 5, 500)] + [dict()]
        for kw in runs:
            r = ref.projection_repair(a, **kw)
            b = alt.projection_repair(a, **kw)
            trials += 1
            if r != b:
                differing += 1
print(f"trials {trials}: outputs differing {differing} (per size {per_size}, sizes 2-6, runs: tol=0 with max_iter 1,2,3,5,500 and defaults)")
sys.exit(0 if differing == 0 else 1)
