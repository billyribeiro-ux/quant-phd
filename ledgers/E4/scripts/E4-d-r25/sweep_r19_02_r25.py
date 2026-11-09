"""Ruling 25 sweep: worst gap error of the equivalent variant mutant_r19_02 against the exact Proposition 3 gap.

Usage (from the repository root): .venv/bin/python -I ledgers/E4/scripts/E4-d-r25/sweep_r19_02_r25.py

The reference solver and the suite are copied into a scratch directory, the reference becomes solver.py, and the
suite's exact oracle prop3_gap_exact is used. The error metric is |gap - exact| / max(1, |exact|), the tolerance of
ruling 22 (1e-14). Two samples are drawn as in the round-19 verifier's scan_r19_02.py (seed 7, 20000 draws) and
scan2_r19_02.py (seed 99, 60000 draws); only points inside the interior region (0 < 2 exp(-4c) - 1 < 1 / (1 + 4 sd^2))
are counted. Output: one line per sample, plus the worst point.
"""

from __future__ import annotations

import importlib.util
import math
import random
import shutil
import sys
import tempfile
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/E/E4/grader"
MUTANT = ROOT / "ledgers/E4/equivalent/mutant_r19_02_price_denominator_drops_uninformed_posterior_precision.py"
TOL = 1e-14


def load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    work = Path(tempfile.mkdtemp(prefix="e4r25-"))
    try:
        shutil.copy(GRADER / "reference.py", work / "solver.py")
        shutil.copy(GRADER / "test_project.py", work / "test_project.py")
        shutil.copy(GRADER / "instance.py", work / "instance.py")
        sys.path.insert(0, str(work))
        import solver as ref  # type: ignore[import-not-found]
        import test_project as tp  # type: ignore[import-not-found]

        mut = load(MUTANT, "mutant_r19_02")
        for label, seed, draws, sd_lo, sd_hi, c_lo, c_hi in (
            ("sample A (seed 7, 20000 draws, sd 1e-8..10^-0.5, cost 0..0.2)", 7, 20000, -8.0, -0.5, 0.0, 0.2),
            ("sample B (seed 99, 60000 draws, sd 1e-6.5..10^-2.5, cost 0.03..0.12)", 99, 60000, -6.5, -2.5, 0.03, 0.12),
        ):
            rng = random.Random(seed)
            n = 0
            mut_fail = 0
            ref_fail = 0
            worst: tuple[float, ...] = (0.0,)
            for _ in range(draws):
                sd = 10 ** rng.uniform(sd_lo, sd_hi)
                cost = rng.uniform(c_lo, c_hi)
                t = 2 * math.exp(-4 * cost) - 1
                if not (0 < t < 1 / (1 + 4 * sd * sd)):
                    continue
                n += 1
                r = ref.solve_model(sd, cost)
                q = mut.solve_model(sd, cost)
                lam_m = q["informed_fraction"]
                lam_r = r["informed_fraction"]
                ex_m = float(tp.prop3_gap_exact(lam_m, sd, cost))
                ex_r = float(tp.prop3_gap_exact(lam_r, sd, cost))
                dm = abs(q["indifference_gap"] - ex_m) / max(1.0, abs(ex_m))
                dr = abs(r["indifference_gap"] - ex_r) / max(1.0, abs(ex_r))
                mut_fail += dm > TOL
                ref_fail += dr > TOL
                if dm > worst[0]:
                    worst = (dm, sd, cost, lam_m, q["indifference_gap"], ex_m, dr, r["indifference_gap"], ex_r)
            print(label)
            print(f"  interior points {n}; mutant above 1e-14: {mut_fail}; reference above 1e-14: {ref_fail}")
            w_rel, w_sd, w_cost, w_lam, w_gap, w_exact, r_rel, r_gap, r_exact = worst
            print(
                f"  worst mutant point: rel {w_rel:.3e} sd {w_sd!r} cost {w_cost!r} lam_mut {w_lam!r} "
                f"mut_gap {w_gap!r} exact {w_exact!r} | ref_rel {r_rel:.3e} ref_gap {r_gap!r} ref_exact {r_exact!r}"
            )
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
