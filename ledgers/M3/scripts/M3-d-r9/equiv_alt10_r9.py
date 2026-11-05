"""Round-9 verifier (M3 slice d): bitwise comparison of the reference projection_repair with the equivalent mutant in
ledgers/M3/equivalent/alt10_no_unit_diagonal_correction.py, on random symmetric matrices of sizes 2 to 6.
Run: .venv/bin/python -I ledgers/M3/scripts/M3-d-r9/equiv_alt10_r9.py
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path.cwd()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(ROOT / "course/modules/M/M3/grader/reference.py", "ref")
alt = load(ROOT / "ledgers/M3/equivalent/alt10_no_unit_diagonal_correction.py", "alt10")
rng = random.Random(9)
trials = differ = 0
for _ in range(2000):
    n = rng.randint(2, 6)
    m = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            v = rng.uniform(-1, 1)
            m[i][j] = m[j][i] = v
    for max_iter in (1, 2, 3, 5, 500):
        for tol in (0.0, 1e-10):
            trials += 1
            a = ref.projection_repair(m, tol=tol, max_iter=max_iter)
            b = alt.projection_repair(m, tol=tol, max_iter=max_iter)
            if a != b:
                differ += 1
print(f"trials {trials}, outputs differing {differ}")
