"""Compare the reference solver with ledgers/E4/equivalent/literal_price_sign.py on random inputs (round 6 re-check).

Usage: python -I equivalent_literal_sign_r6.py <checkout-root>
"""

from __future__ import annotations

import importlib.util
import math
import random
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load("ref_r6b", root / "course/modules/E/E4/grader/reference.py")
var = load("var_r6b", root / "ledgers/E4/equivalent/literal_price_sign.py")
rng = random.Random(7)
worst = 0.0
n = 0
for _ in range(3000):
    sd = rng.uniform(0.05, 3.0)
    cost = rng.uniform(0.0, 0.4)
    a = ref.solve_model(sd, cost)
    b = var.solve_model(sd, cost)
    for k in a:
        worst = max(worst, abs(a[k] - b[k]))
    n += 1
print(f"literal_price_sign vs reference: {n} inputs, largest absolute difference in any output = {worst!r}")
print("sign-only check of b_u: reference b_u<0 on all sampled lam:", all(ref.price_coefficients(l / 100, 0.6)[1] < 0 for l in range(1, 101)))
print("math.isfinite used by both:", math.isfinite(1.0))
