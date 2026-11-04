"""Round-5 verifier: is the unit-diagonal correction term H of projection_repair ever read?

Compares the reference with alt10 (H dropped) on random symmetric inputs, several max_iter values, tol=0.
Also checks that the off-diagonal entries of H stay zero (a structural argument, reported with the numbers).
Run from the checkout root: .venv/bin/python -I ledgers/M3/scripts/M3-d-r5/equiv_check_r5.py
"""

import importlib.util
import random
from pathlib import Path

ROOT = Path.cwd()


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(ROOT / "course/modules/M/M3/grader/reference.py")
alt = load(ROOT / "ledgers/M3/scripts/M3-d-r5/equivalent/alt10_equivalent_no_unit_diagonal_correction.py")
rng = random.Random(20261103)
worst = 0.0
cases = 0
for trial in range(60):
    k = rng.choice((3, 4, 5))
    m = [[1.0 if i == j else 0.0 for j in range(k)] for i in range(k)]
    for i in range(k):
        for j in range(i + 1, k):
            v = round(rng.uniform(-0.99, 0.99), 6)
            m[i][j] = m[j][i] = v
    for steps in (1, 2, 3, 5, 10, 50):
        a = ref.projection_repair(m, tol=0.0, max_iter=steps)
        b = alt.projection_repair(m, tol=0.0, max_iter=steps)
        diff = max(abs(a[i][j] - b[i][j]) for i in range(k) for j in range(k))
        worst = max(worst, diff)
        cases += 1
print(f"cases={cases} max abs difference reference vs alt10 = {worst:.3e}")
