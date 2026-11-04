"""Which seeds fail the chi-square lag test for each chi-square sharing variant (round 8, slice d).

Variants are built from grader/reference.py exactly as the round-7 generator did (draw d reuses the chi-square
variable of an earlier draw under a stated condition). Each seed 0-49 runs the grader's own test
test_student_t_draws_do_not_share_chi_square with the run_graders workspace and flags. The lag-four mutant from
ledgers/M4/mutants is also run with the whole suite, to see which test fails.
Usage: python -I ledgers/M4/scripts/M4-d-r8/checks/chi_lag_r8.py
"""

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-M4-d")
GRADER = ROOT / "course/modules/M/M4/grader"
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import PYTEST_FLAGS, panel, workspace  # noqa: E402

OLD_LOOP = "    for _ in range(n_draws):\n"
OLD_CHI = "            chi_square = rng.gammavariate(nu / 2, 2.0)\n"
TMP = pathlib.Path(tempfile.mkdtemp(prefix="chi-r8-"))


def variant(name: str, cond: str | None, source: str | None) -> pathlib.Path:
    ref = (GRADER / "reference.py").read_text(encoding="utf-8")
    assert ref.count(OLD_LOOP) == 1 and ref.count(OLD_CHI) == 1
    if cond is None:
        path = GRADER / "reference.py"
        return path
    src = ref.replace(OLD_LOOP, "    chi_by_draw: dict[int, float] = {}\n    for d in range(n_draws):\n")
    new_chi = (
        "            if " + cond + ":\n"
        "                chi_square = " + source + "\n"
        "            else:\n"
        "                chi_square = rng.gammavariate(nu / 2, 2.0)\n"
        "            chi_by_draw[d] = chi_square\n"
    )
    out = TMP / f"{name}.py"
    out.write_text(src.replace(OLD_CHI, new_chi), encoding="utf-8")
    return out


def run(args):
    solution, name, seed, k_filter = args
    u = unit("M4")
    cfg = panel(u)
    work = workspace(u, solution, cfg)
    try:
        cmd = [sys.executable, "-m", "pytest", *PYTEST_FLAGS, cfg["suite"]]
        if k_filter:
            cmd += ["-k", k_filter]
        result = subprocess.run(
            cmd, cwd=work, capture_output=True, text=True, check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            timeout=600,
        )
        failed = sorted(set(part.split("::")[-1].split("[")[0] for part in
                            [line.split(" ")[1] for line in (result.stdout).splitlines() if line.startswith("FAILED ")]))
        return name, seed, result.returncode == 0, failed
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    variants = {
        "lag1_2k_2k1": variant("lag1_2k_2k1", "d % 2 == 1", "chi_by_draw[d - 1]"),
        "lag2_4j_4j2": variant("lag2_4j_4j2", "d % 4 == 2", "chi_by_draw[d - 2]"),
        "lag3_6j_6j3": variant("lag3_6j_6j3", "d % 6 == 3", "chi_by_draw[d - 3]"),
        "even_all_share": variant("even_all_share", "d % 2 == 0 and d > 0", "chi_by_draw[0]"),
    }
    jobs = []
    for name, path in variants.items():
        for s in range(50):
            jobs.append((path, name, s, "test_student_t_draws_do_not_share_chi_square"))
    lag4 = ROOT / "ledgers/M4/mutants/r7d_02_chi_square_shared_by_draws_four_apart_lag_four.py"
    for s in range(50):
        jobs.append((lag4, "r7d_02_lag4_full_suite", s, None))
    with ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(run, jobs))
    for name in variants:
        fails = [s for n, s, ok, _ in res if n == name and not ok]
        print(f"{name}: chi-square lag test fails on {len(fails)} of 50 seeds")
    lag4_res = [(s, ok, f) for n, s, ok, f in res if n == "r7d_02_lag4_full_suite"]
    print("r7d_02 lag-four mutant, full suite: seeds failing", sum(1 for _, ok, _ in lag4_res if not ok), "of 50")
    from collections import Counter
    c = Counter(t for _, ok, f in lag4_res for t in f)
    print("r7d_02 failing tests over seeds 0-49:", dict(c))
    print("r7d_02 seeds where the cross-term test is the only failure:",
          [s for s, ok, f in lag4_res if f and set(f) == {"test_student_t_cross_term_matches_matched_covariance"}])
    print("r7d_02 seeds passing the whole suite:", [s for s, ok, _ in lag4_res if ok])
