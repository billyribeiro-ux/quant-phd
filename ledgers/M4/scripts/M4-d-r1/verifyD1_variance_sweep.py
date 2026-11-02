"""Verifier round-1 sweep: the numbers quoted in test_project.py lines 31-39 (variance tolerance and its kill counts).

For seeds 0 to 1999 (make_instance) it computes, with the suite's own statistic (sample_variance of the losses against
portfolio_variance(), relative error, TOL_T_VARIANCE = 0.30):
  * the reference's relative error for the Student-t variance, grouped by nu, and the maximum per nu;
  * for the variant with NO matched factor at all (sqrt(nu / W) instead of sqrt((nu - 2) / W)): whether the check fails,
    grouped by nu (the comment's "fails on every seed tested at nu = 5 and 6 (347 and 317 seeds) ...");
  * the reference at seed 1093 (nu = 3), which the comment says fails.
Writes one line per seed to a CSV-like list in the scratch directory given as argv[1] and prints the summary.
Run from the checkout root: .venv/bin/python -I ledgers/M4/scripts/M4-d-r1/verifyD1_variance_sweep.py /tmp/M4-d-r1/sweep
"""

from __future__ import annotations

import importlib.util
import math
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/M/M4/grader"
sys.path.insert(0, str(GRADER))
from instance import make_instance  # noqa: E402

spec = importlib.util.spec_from_file_location("reference", GRADER / "reference.py")
assert spec is not None and spec.loader is not None
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)

TOL = 0.30


def sample_variance(xs: list[int]) -> float:
    mean = math.fsum(xs) / len(xs)
    return math.fsum((x - mean) ** 2 for x in xs) / (len(xs) - 1)


def no_matched(positions: list[int], cov: list[list[float]], n_draws: int, seed: int, nu: int) -> list[int]:
    """Reference model with the matched factor omitted (scale = sqrt(nu / W))."""
    n = len(positions)
    factor = ref._cholesky(cov, n)
    rng = random.Random(seed)
    out: list[int] = []
    for _ in range(n_draws):
        z = [rng.gauss(0.0, 1.0) for _ in range(n)]
        chi = rng.gammavariate(nu / 2, 2.0)
        scale = math.sqrt(nu / chi)
        total = 0.0
        for i in range(n):
            total += positions[i] * (scale * sum(factor[i][k] * z[k] for k in range(i + 1)))
        out.append(round(-total))
    return out


import random  # noqa: E402


def main() -> int:
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    ref_err: dict[int, list[float]] = defaultdict(list)
    nomatch_fail: dict[int, list[bool]] = defaultdict(list)
    lines = []
    for seed in range(2000):
        inst = make_instance(seed)
        nu = inst["nu"]
        if nu < 5:
            # The suite skips the variance check for nu of 3 and 4; the sweep still records it for the comment's numbers.
            pass
        target = sum(
            inst["positions_cents"][i] * inst["positions_cents"][j] * inst["cov"][i][j]
            for i in range(inst["n_assets"])
            for j in range(inst["n_assets"])
        )
        losses = ref.simulate_losses(inst["positions_cents"], inst["cov"], inst["n_draws"], seed, "student_t", nu)
        err = abs(sample_variance(losses) / target - 1.0)
        ref_err[nu].append(err)
        losses_nm = no_matched(inst["positions_cents"], inst["cov"], inst["n_draws"], seed, nu)
        fail_nm = abs(sample_variance(losses_nm) / target - 1.0) > TOL
        nomatch_fail[nu].append(fail_nm)
        lines.append(f"{seed},{nu},{inst['n_draws']},{err:.6f},{int(fail_nm)}")
    (out_dir / "sweep.csv").write_text("seed,nu,n_draws,ref_rel_err,nomatch_fails\n" + "\n".join(lines) + "\n")
    for nu in sorted(ref_err):
        seeds = len(ref_err[nu])
        print(
            f"nu={nu}: seeds {seeds}; reference max relative error {max(ref_err[nu]):.4f}; "
            f"no-matched variant fails on {sum(nomatch_fail[nu])} of {seeds} seeds"
        )
    inst1093 = make_instance(1093)
    t1093 = sum(
        inst1093["positions_cents"][i] * inst1093["positions_cents"][j] * inst1093["cov"][i][j]
        for i in range(inst1093["n_assets"])
        for j in range(inst1093["n_assets"])
    )
    l1093 = ref.simulate_losses(
        inst1093["positions_cents"], inst1093["cov"], inst1093["n_draws"], 1093, "student_t", inst1093["nu"]
    )
    e1093 = abs(sample_variance(l1093) / t1093 - 1.0)
    print(f"seed 1093: nu {inst1093['nu']}, reference relative error {e1093:.4f} (fails at 0.30: {e1093 > TOL})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
