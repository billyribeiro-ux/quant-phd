"""Verifier round-1 instance check (project.html Grading mode; grader/instance.py docstring).

(1) Every instance for seeds 0-1999 is valid: 2 or 3 positions, whole cents in [1000.00, 50000.00] (the docstring's
range), covariance symmetric and positive definite (Cholesky pivots above zero), nu in {3..8}, n_draws in the fixed set
with none a multiple of 100 and none above 19987.
(2) For seeds 0-19 the answers change, not only the labels: the reference's Gaussian 99% loss, Student-t 99% loss and
the sample variance of the Gaussian losses are printed per seed, with the number of distinct values.
Run from the checkout root: .venv/bin/python -I ledgers/M4/scripts/M4-d-r1/verifyD1_instances.py
"""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/M/M4/grader"
sys.path.insert(0, str(GRADER))
from instance import make_instance  # noqa: E402

spec = importlib.util.spec_from_file_location("reference", GRADER / "reference.py")
assert spec is not None and spec.loader is not None
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)

DRAWS = {6_003, 8_001, 9_997, 12_011, 15_013, 19_987}


def valid(inst: dict) -> list[str]:
    problems: list[str] = []
    n = inst["n_assets"]
    if n not in (2, 3):
        problems.append("n_assets")
    pos = inst["positions_cents"]
    if len(pos) != n or any(type(w) is not int or not (100_000 <= w <= 5_000_000) for w in pos):
        problems.append("positions")
    cov = inst["cov"]
    if any(cov[i][j] != cov[j][i] for i in range(n) for j in range(n)):
        problems.append("symmetry")
    try:
        ref._cholesky(cov, n)
    except ValueError:
        problems.append("positive definite")
    if not (3 <= inst["nu"] <= 8):
        problems.append("nu")
    if inst["n_draws"] not in DRAWS or inst["n_draws"] % 100 == 0 or inst["n_draws"] > 19_987:
        problems.append("n_draws")
    return problems


def main() -> int:
    bad = {}
    for seed in range(2000):
        problems = valid(make_instance(seed))
        if problems:
            bad[seed] = problems
    print(f"instances seeds 0-1999: {2000 - len(bad)} valid, {len(bad)} invalid {dict(list(bad.items())[:5])}")
    gauss, student, variances = [], [], []
    for seed in range(20):
        inst = make_instance(seed)
        losses_g = ref.simulate_losses(inst["positions_cents"], inst["cov"], inst["n_draws"], seed, "gaussian", None)
        losses_t = ref.simulate_losses(
            inst["positions_cents"], inst["cov"], inst["n_draws"], seed, "student_t", inst["nu"]
        )
        q_g = ref.quantile_99(losses_g)
        q_t = ref.quantile_99(losses_t)
        mean = sum(losses_g) / len(losses_g)
        var = sum((x - mean) ** 2 for x in losses_g) / (len(losses_g) - 1)
        gauss.append(q_g)
        student.append(q_t)
        variances.append(round(var))
        print(
            f"seed {seed:2d}: assets {inst['n_assets']} nu {inst['nu']} draws {inst['n_draws']:6d} "
            f"gaussian q99 {q_g:9d} student_t q99 {q_t:9d} gaussian var {var:.4g}"
        )
    print(f"distinct gaussian q99 over seeds 0-19: {len(set(gauss))} of 20; distinct student_t q99: {len(set(student))} of 20")
    print(f"min/max gaussian q99: {min(gauss)} / {max(gauss)}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
