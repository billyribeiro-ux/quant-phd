"""Round-8 verifier (M3 slice d): bitwise check of the equivalent mutant ledgers/M3/equivalent/alt10_no_unit_diagonal_correction.py
against grader/reference.py, plus a control: a mutant that is NOT equivalent must differ somewhere.

Random symmetric matrices of sizes 2 to 6 (seeded), max_iter in {1, 2, 3, 5, 500}, tol in {0.0, 1e-10}.
Run from the checkout root: .venv/bin/python -I ledgers/M3/scripts/M3-d-r8/equiv_alt10_r8.py
"""

import importlib.util
import random
from pathlib import Path

ROOT = Path.cwd()


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(ROOT / "course/modules/M/M3/grader/reference.py", "ref_m3")
eq = load(ROOT / "ledgers/M3/equivalent/alt10_no_unit_diagonal_correction.py", "eq_m3")
rng = random.Random(20261104)
trials = 0
differ = 0
bits_differ = 0
for n in range(2, 7):
    for _ in range(400):
        a = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                v = rng.uniform(-1.5, 1.5)
                a[i][j] = v
                a[j][i] = v
        for max_iter in (1, 2, 3, 5, 500):
            for tol in (0.0, 1e-10):
                trials += 1
                x = ref.projection_repair(a, tol=tol, max_iter=max_iter)
                y = eq.projection_repair(a, tol=tol, max_iter=max_iter)
                if x != y:
                    differ += 1
                if [repr(v) for row in x for v in row] != [repr(v) for row in y for v in row]:
                    bits_differ += 1
print("trials", trials, "outputs differing (==)", differ, "outputs differing (repr)", bits_differ)
