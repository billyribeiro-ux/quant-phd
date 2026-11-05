"""Round-11 verifier d: the test's cross-term statistic (100,000 draws, nu = 5, seeds 0-9) for the two round-8 and
round-9 cross-term mutants named in the test_project.py comment (lines 43-47), and the reference, to re-check the
comment's ranges 0.068-0.086 and 0.141-0.161 and the reference maximum over seeds 0-49 (0.024)."""

import importlib.util
import math
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
FILES = {
    "reference": ROOT / "course/modules/M/M4/grader/reference.py",
    "r8_03_first_asset_only": ROOT / "ledgers/M4/mutants/r8_03_student_t_matched_scale_on_first_asset_only.py",
    "r9_02_second_asset_own_chi_square": ROOT / "ledgers/M4/mutants/r9_02_student_t_second_asset_own_chi_square.py",
}


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fsum_var(xs):
    mean = math.fsum(xs) / len(xs)
    return math.fsum((x - mean) ** 2 for x in xs) / (len(xs) - 1)


def job(args):
    label, seed = args
    mod = load(FILES[label], "c_" + label.replace("-", "_"))
    w1, w2 = 1_000_000, 1_000_000
    cov = [[4e-4, 4.8e-4], [4.8e-4, 9e-4]]
    target = 4.0 * w1 * w2 * cov[0][1]
    plus = mod.simulate_losses([w1, w2], cov, 100_000, seed, "student_t", 5)
    minus = mod.simulate_losses([w1, -w2], cov, 100_000, seed, "student_t", 5)
    return label, seed, abs((fsum_var(plus) - fsum_var(minus)) / target - 1.0)


if __name__ == "__main__":
    work = [(lab, s) for lab in FILES for s in (range(10) if lab != "reference" else range(50))]
    with ProcessPoolExecutor(max_workers=12) as ex:
        rows = list(ex.map(job, work))
    for lab in FILES:
        vals = [e for l, s, e in rows if l == lab]
        seeds = 50 if lab == "reference" else 10
        print(f"{lab}: seeds 0-{seeds - 1}: min {min(vals):.4f} max {max(vals):.4f}")
