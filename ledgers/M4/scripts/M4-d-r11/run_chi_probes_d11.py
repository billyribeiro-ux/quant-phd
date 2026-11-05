"""Round-11 verifier d: run the chi-square lag test (test_student_t_draws_do_not_share_chi_square) on seeds 0-49 for each
sharing probe. Probe solutions are the round-10 probe modules, unchanged, in ledgers/M4/scripts/M4-d-r10/probes/<mode>/
(tail_risk.py); instance.py and test_project.py are copied from the grader of this checkout. Prints PASS/FAIL per seed."""

import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
PY = sys.executable
GRADER = ROOT / "course/modules/M/M4/grader"
PROBES = ROOT / "ledgers/M4/scripts/M4-d-r10/probes"
MODES = ["ref", "lag1_pairs_2k_2k1", "lag2_pairs_4j_4j2", "lag3_pairs_6j_6j3", "even_all_share",
         "chain_lag4_4j_4j4", "disjoint_lag4_8j_8j4"]
TEST = "test_student_t_draws_do_not_share_chi_square"


def run(job: tuple[str, int]) -> tuple[str, int, str]:
    mode, seed = job
    work = Path(tempfile.mkdtemp(prefix="chi11"))
    shutil.copy(GRADER / "instance.py", work / "instance.py")
    shutil.copy(GRADER / "test_project.py", work / "test_project.py")
    src = PROBES / mode / "tail_risk.py"
    if not src.exists():
        src = PROBES / mode / "tail_risk.py"
    shutil.copy(src, work / "tail_risk.py")
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
    proc = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                           "-k", TEST, "test_project.py"], cwd=work, env=env, capture_output=True, text=True, check=False)
    shutil.rmtree(work, ignore_errors=True)
    verdict = {0: "PASS", 1: "FAIL"}.get(proc.returncode, "ERR")
    return mode, seed, verdict


if __name__ == "__main__":
    jobs = [(m, s) for m in MODES for s in range(50)]
    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(run, jobs))
    for mode in MODES:
        verdicts = [v for m, _, v in results if m == mode]
        failing = [s for m, s, v in results if m == mode and v == "FAIL"]
        print(f"{mode}: FAIL {len(failing)}/50 ERR {verdicts.count('ERR')} seeds {failing}")
    sys.stdout.flush()
