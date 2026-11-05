"""Seed sweep behind the comment at grader/test_project.py lines 31-39 (round 8, slice d).

For seeds 0-1999 it builds the instance with make_instance, simulates the reference and a variant with the matched
factor left out (scale sqrt(nu / W) instead of sqrt((nu - 2) / W), so the variance is inflated by nu / (nu - 2)), and
records the relative error of the sample variance of the losses against w' Sigma w, exactly as
test_student_t_loss_variance_matches_matched_covariance measures it. Prints, per nu: the number of seeds, the largest
reference error, the number of seeds whose reference error exceeds TOL_T_VARIANCE 0.30, and the number of seeds where the
variant fails the same check. It also reports seed 1093 (nu = 3) for the reference.
Usage: python -I ledgers/M4/scripts/M4-d-r9/checks/variance_sweep_r9.py
"""

import importlib.util
import math
import pathlib
import tempfile
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD9-M4-d")
GRADER = ROOT / "course/modules/M/M4/grader"
TMP = pathlib.Path(tempfile.mkdtemp(prefix="var-r8-"))
TOL = 0.30


def load(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_variant() -> pathlib.Path:
    ref = (GRADER / "reference.py").read_text(encoding="utf-8")
    old = "            scale = math.sqrt(matched * nu / chi_square)\n"
    assert ref.count(old) == 1, "reference scale line changed"
    path = TMP / "no_matched_factor.py"
    path.write_text(ref.replace(old, "            scale = math.sqrt(nu / chi_square)\n"), encoding="utf-8")
    return path


REF = GRADER / "reference.py"
VARIANT = make_variant()


def sample_variance(xs):
    mean = math.fsum(xs) / len(xs)
    return math.fsum((x - mean) ** 2 for x in xs) / (len(xs) - 1)


def errors(seed: int):
    inst_mod = load(GRADER / "instance.py", "instance_mod")
    inst = inst_mod.make_instance(seed)
    pos, cov, nu, n = inst["positions_cents"], inst["cov"], inst["nu"], inst["n_draws"]
    n_assets = len(pos)
    target = math.fsum(pos[i] * pos[j] * cov[i][j] for i in range(n_assets) for j in range(n_assets))
    ref = load(REF, f"ref_{seed}")
    var = load(VARIANT, f"var_{seed}")
    ref_losses = ref.simulate_losses(pos, cov, n, seed, "student_t", nu)
    var_losses = var.simulate_losses(pos, cov, n, seed, "student_t", nu)
    e_ref = abs(sample_variance(ref_losses) / target - 1.0)
    e_var = abs(sample_variance(var_losses) / target - 1.0)
    return seed, nu, e_ref, e_var


if __name__ == "__main__":
    seeds = list(range(2000))
    with ProcessPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(errors, seeds, chunksize=8))
    by_nu = defaultdict(list)
    for seed, nu, e_ref, e_var in rows:
        by_nu[nu].append((seed, e_ref, e_var))
    for nu in sorted(by_nu):
        items = by_nu[nu]
        max_ref = max(e for _, e, _ in items)
        n_ref_fail = sum(1 for _, e, _ in items if e > TOL)
        n_var_fail = sum(1 for _, _, v in items if v > TOL)
        print(f"nu={nu}: seeds={len(items)} max_ref_rel_err={max_ref:.4f} ref_fail(>0.30)={n_ref_fail} "
              f"no_matched_factor_fail(>0.30)={n_var_fail} of {len(items)}")
    print("total seeds:", len(rows))
    s1093 = errors(1093)
    print(f"seed 1093: nu={s1093[1]} ref_rel_err={s1093[2]:.4f} (fails 0.30: {s1093[2] > TOL}) no_matched_rel_err={s1093[3]:.4f}")
