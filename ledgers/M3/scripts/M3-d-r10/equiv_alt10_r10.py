"""Round-10 verifier (M3 slice d): bit-for-bit check that ledgers/M3/equivalent/alt10_no_unit_diagonal_correction.py
equals the reference projection_repair on random symmetric matrices (sizes 2-6, several max_iter, tol 0 and 1e-10).
Run from the checkout root: python -I <this file>."""

import importlib.util
import random
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyD10-M3-d"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load("ref", f"{ROOT}/course/modules/M/M3/grader/reference.py")
alt = load("alt10", f"{ROOT}/ledgers/M3/equivalent/alt10_no_unit_diagonal_correction.py")
rng = random.Random(20261105)
trials = differing = 0
for _ in range(1000):
    n = rng.randint(2, 6)
    a = [[0.0] * n for _ in range(n)]
    for i in range(n):
        a[i][i] = 1.0
        for j in range(i + 1, n):
            v = rng.uniform(-0.99, 0.99)
            a[i][j] = a[j][i] = v
    for max_iter in (1, 2, 3, 5, 20):
        for tol in (0.0, 1e-10):
            trials += 1
            x = ref.projection_repair(a, tol=tol, max_iter=max_iter)
            y = alt.projection_repair(a, tol=tol, max_iter=max_iter)
            if x != y:  # exact float list equality: bitwise, since Python floats compare exactly
                differing += 1
print("trials", trials, "outputs differing", differing)
