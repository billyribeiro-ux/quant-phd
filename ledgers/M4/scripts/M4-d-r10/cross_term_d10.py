"""Round-10 verifier D: the Student-t cross-term check (test_student_t_cross_term_matches_matched_covariance) on seeds 0-49.

For each module, the script reproduces the test's statistic exactly: 100,000 draws at nu = 5, plus and minus second-position
losses, sample variances by math.fsum, relative error against 4 w1 w2 Sigma_12 with TOL_CROSS_TERM = 0.05.
Modules: the reference, the reference with the second Cholesky row scaled by (1 + eps) for eps in +/-0.03 and +/-0.05
(a cross-term error of eps), and the two round-8 and round-9 Student-t mutants of this check.
Output: per module, the relative errors min/max over seeds 0-49 and the count of seeds where the test fails (error > 0.05).
"""

import importlib.util
import math
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD10-M4-d")
REF = ROOT / "course/modules/M/M4/grader/reference.py"
MUTANTS = {
    "r8_03_matched_scale_first_asset_only": ROOT / "ledgers/M4/mutants/r8_03_student_t_matched_scale_on_first_asset_only.py",
    "r9_02_second_asset_own_chi_square": ROOT / "ledgers/M4/mutants/r9_02_student_t_second_asset_own_chi_square.py",
}
EPS = {"ref": 0.0, "eps+0.03": 0.03, "eps-0.03": -0.03, "eps+0.05": 0.05, "eps-0.05": -0.05}
W1, W2 = 1_000_000, 1_000_000
COV = [[4e-4, 4.8e-4], [4.8e-4, 9e-4]]
TARGET = 4.0 * W1 * W2 * COV[0][1]
SEEDS = range(50)
DRAWS = 100_000
NU = 5


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scaled_module(eps: float):
    """reference.py with the Cholesky factor's [1][0] entry multiplied by (1 + eps)."""
    text = REF.read_text(encoding="utf-8")
    old = "    return factor\n"
    assert text.count(old) == 1
    text = text.replace(old, f"    if len(factor) == 2:  # the two-position case only\n        factor[1][0] *= {1.0 + eps!r}\n" + old)
    path = ROOT / "ledgers/M4/scripts/M4-d-r10/probes" / f"cross_eps_{eps:+.2f}.py"
    path.write_text(text, encoding="utf-8")
    return load(path, f"cross_{eps:+.2f}".replace("+", "p").replace("-", "m").replace(".", "_"))


def sample_variance(xs):
    mean = math.fsum(xs) / len(xs)
    return math.fsum((x - mean) ** 2 for x in xs) / (len(xs) - 1)


def rel_error(module, seed: int) -> float:
    plus = module.simulate_losses([W1, W2], COV, DRAWS, seed, "student_t", NU)
    minus = module.simulate_losses([W1, -W2], COV, DRAWS, seed, "student_t", NU)
    measured = sample_variance(plus) - sample_variance(minus)
    return abs(measured / TARGET - 1.0)


def job(args):
    label, path, seed = args
    return label, seed, rel_error(load(path, label), seed)


if __name__ == "__main__":
    paths = {}
    for label, eps in EPS.items():
        if eps:
            scaled_module(eps)
            paths[label] = ROOT / "ledgers/M4/scripts/M4-d-r10/probes" / f"cross_eps_{eps:+.2f}.py"
        else:
            paths[label] = REF
    for label, path in MUTANTS.items():
        paths[label] = path
    work = [(label, paths[label], seed) for label in paths for seed in SEEDS]
    with ProcessPoolExecutor(max_workers=12) as ex:
        results = list(ex.map(job, work))
    for label in paths:
        errs = [e for lab, _, e in results if lab == label]
        seeds_failing = sum(1 for e in errs if e > 0.05)
        print(f"{label}: rel error min {min(errs):.4f} max {max(errs):.4f}; seeds failing (error > 0.05): {seeds_failing}/50")
    print("per-seed errors for mutants (seeds 0-9):")
    for label in MUTANTS:
        print(label, [round(e, 4) for lab, s, e in results if lab == label and s < 10])
    sys.stdout.flush()
