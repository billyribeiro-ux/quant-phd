"""Round-11 probe: equivalent mutant ledgers/M3/equivalent/alt10_no_unit_diagonal_correction.py versus the reference,
compared bit for bit (float.hex of every entry) on random symmetric matrices, sizes 2 to 6, with tol in {0, 1e-10} and
max_iter in {1, 2, 3, 5, 20}. Run from the checkout root."""

import importlib.util
import random
import sys
from pathlib import Path

ROOT = Path.cwd()


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


ref = load("ref", ROOT / "course/modules/M/M3/grader/reference.py")
mut = load("mut", ROOT / "ledgers/M3/equivalent/alt10_no_unit_diagonal_correction.py")
rng = random.Random(1111)
trials = 0
bad = 0
for _ in range(1000):
    k = rng.randint(2, 6)
    m = [[0.0] * k for _ in range(k)]
    for i in range(k):
        m[i][i] = rng.uniform(0.2, 1.8)
        for j in range(i + 1, k):
            v = rng.uniform(-1.5, 1.5)
            m[i][j] = v
            m[j][i] = v
    for tol in (0.0, 1e-10):
        for mi in (1, 2, 3, 5, 20):
            trials += 1
            a = ref.projection_repair(m, tol=tol, max_iter=mi)
            b = mut.projection_repair(m, tol=tol, max_iter=mi)
            ha = [[x.hex() for x in row] for row in a]
            hb = [[x.hex() for x in row] for row in b]
            if ha != hb:
                bad += 1
print(f"bitwise differing outputs: {bad} of {trials}")
