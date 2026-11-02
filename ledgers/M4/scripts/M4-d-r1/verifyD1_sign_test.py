"""Verifier round-1: candidate sign test that works only if the Gaussian stream order is frozen (NOT added to the grader).

The candidate freezes the stream: the Gaussian family draws n normals per draw from random.Random(seed).gauss(0, 1) in
position order, and the first loss must equal round(-sum_i w_i (L z)_i). It is run against the reference, the mutant
m11 (loss sign flipped) and the five alternatives. Expected: it kills m11, passes the reference and any implementation
that uses the frozen stream, and fails the implementations that change the Gaussian stream (alt_1 Box-Muller, alt_2 polar).
Run from the checkout root: .venv/bin/python -I ledgers/M4/scripts/M4-d-r1/verifyD1_sign_test.py <solution.py> ...
"""

from __future__ import annotations

import importlib.util
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/M/M4/grader"
sys.path.insert(0, str(GRADER))
from instance import make_instance  # noqa: E402


def load(path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location("solution_under_test", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def frozen_first_loss(positions: list[int], cov: list[list[float]], seed: int) -> int:
    n = len(positions)
    # Cholesky by hand for the 2 x 2 and 3 x 3 covariances of the instance (row by row, as in the reference).
    factor = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            inner = sum(factor[i][k] * factor[j][k] for k in range(j))
            if i == j:
                factor[i][i] = math.sqrt(cov[i][i] - inner)
            else:
                factor[i][j] = (cov[i][j] - inner) / factor[j][j]
    rng = random.Random(seed)
    z = [rng.gauss(0.0, 1.0) for _ in range(n)]
    total = sum(positions[i] * sum(factor[i][k] * z[k] for k in range(i + 1)) for i in range(n))
    return round(-total)


def sign_test(sol) -> bool:  # type: ignore[no-untyped-def]
    ok = True
    for seed in range(10):
        inst = make_instance(seed)
        losses = sol.simulate_losses(inst["positions_cents"], inst["cov"], 5, seed, "gaussian", None)
        if losses[0] != frozen_first_loss(inst["positions_cents"], inst["cov"], seed):
            ok = False
    return ok


def main() -> int:
    for path in (Path(p) for p in sys.argv[1:]):
        print(f"{path.name}: frozen-stream sign test {'PASS' if sign_test(load(path)) else 'FAIL'} (seeds 0-9)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
