"""Cross-term tolerance and mutant measurements for project.html and test_project.py (round 8, slice d).

Re-creates the variants of the Student-t scale (a global scale factor on the reference, and the matched factor or
chi-square sharing on one asset) from the reference in the pinned checkout, and measures the cross-term relative error
exactly as test_student_t_cross_term_matches_matched_covariance does (same instance, same seed, same draw count).
Usage: python -I ledgers/M4/scripts/M4-d-r9/checks/cross_r9.py
"""

import importlib.util
import math
import pathlib
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD9-M4-d")
REF = ROOT / "course/modules/M/M4/grader/reference.py"
MUT = ROOT / "ledgers/M4/mutants"
TMP = pathlib.Path(tempfile.mkdtemp(prefix="cross-r8-"))


def load(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample_variance(xs):
    mean = math.fsum(xs) / len(xs)
    return math.fsum((x - mean) ** 2 for x in xs) / (len(xs) - 1)


def rel_err(path: pathlib.Path, seed: int) -> float:
    sol = load(path, f"sol_{path.stem}_{seed}")
    w1, w2 = 1_000_000, 1_000_000
    cov = [[4e-4, 4.8e-4], [4.8e-4, 9e-4]]
    target = 4.0 * w1 * w2 * cov[0][1]
    plus = sol.simulate_losses([w1, w2], cov, 100_000, seed, "student_t", 5)
    minus = sol.simulate_losses([w1, -w2], cov, 100_000, seed, "student_t", 5)
    return abs((sample_variance(plus) - sample_variance(minus)) / target - 1.0)


def scaled_variant(name: str, factor: float) -> pathlib.Path:
    ref = REF.read_text(encoding="utf-8")
    old = "            scale = math.sqrt(matched * nu / chi_square)\n"
    assert ref.count(old) == 1
    new = f"            scale = math.sqrt(matched * nu / chi_square) * math.sqrt({factor!r})\n"
    path = TMP / f"{name}.py"
    path.write_text(ref.replace(old, new), encoding="utf-8")
    return path


def job(args):
    path, seed = args
    return path.stem, seed, rel_err(path, seed)


if __name__ == "__main__":
    variants = {
        "reference": REF,
        "scale_minus_5pct": scaled_variant("scale_minus_5pct", 0.95),
        "scale_plus_5pct": scaled_variant("scale_plus_5pct", 1.05),
        "scale_plus_3pct": scaled_variant("scale_plus_3pct", 1.03),
    }
    seeds = range(50)
    jobs = [(p, s) for p in variants.values() for s in seeds]
    with ProcessPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(job, jobs))
    by = {}
    for name, seed, err in results:
        by.setdefault(name, {})[seed] = err
    ref_errs = by["reference"]
    print("reference max rel err seeds 0-49:", round(max(ref_errs.values()), 4),
          "argmax seed", max(ref_errs, key=ref_errs.get))
    for name in ("scale_plus_3pct", "scale_minus_5pct", "scale_plus_5pct"):
        errs = by[name]
        detected = sum(1 for e in errs.values() if e > 0.05)
        print(f"{name}: mean rel err {sum(errs.values())/50:.4f}; fails cross-term test (tol 0.05) on {detected} of 50 seeds")
    # mutants from the repo: first-asset-only matched factor, and a second-asset own chi-square variable
    m83 = load(MUT / "r8_03_student_t_matched_scale_on_first_asset_only.py", "m83")
    m92 = load(MUT / "r9_02_student_t_second_asset_own_chi_square.py", "m92")
    e83 = [rel_err(MUT / "r8_03_student_t_matched_scale_on_first_asset_only.py", s) for s in range(10)]
    e92 = [rel_err(MUT / "r9_02_student_t_second_asset_own_chi_square.py", s) for s in range(10)]
    print("r8_03 (matched factor first asset only) rel err seeds 0-9 min/max:", round(min(e83), 4), round(max(e83), 4))
    print("r9_02 (second asset own chi-square) rel err seeds 0-9 min/max:", round(min(e92), 4), round(max(e92), 4))
    print("module handles:", m83.__name__, m92.__name__, file=sys.stderr)
