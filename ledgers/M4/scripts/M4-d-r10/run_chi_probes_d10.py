"""Round-10 verifier D: run the M4 chi-square lag test (test_student_t_draws_do_not_share_chi_square) on seeds 0-49 for each sharing probe.

Each probe directory under ledgers/M4/scripts/M4-d-r10/probes/ holds tail_risk.py (the reference with one chi-square owner rule),
instance.py and test_project.py. Output: one line per (probe, seed) with PASS or FAIL, then a count per probe.
"""

import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD10-M4-d")
PY = str(ROOT / ".venv/bin/python")
PROBES = ROOT / "ledgers/M4/scripts/M4-d-r10/probes"
MODES = [
    "ref",
    "lag1_pairs_2k_2k1",
    "lag2_pairs_4j_4j2",
    "lag3_pairs_6j_6j3",
    "even_all_share",
    "chain_lag4_4j_4j4",
    "disjoint_lag4_8j_8j4",
]
TEST = "test_student_t_draws_do_not_share_chi_square"


def run(job: tuple[str, int]) -> tuple[str, int, str]:
    mode, seed = job
    env = dict(os.environ, QF_SEED=str(seed))
    proc = subprocess.run(
        [PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "-k", TEST, "test_project.py"],
        cwd=PROBES / mode,
        env=env,
        capture_output=True,
        text=True,
    )
    last = (proc.stdout.strip().splitlines() or ["(no output)"])[-1]
    verdict = {0: "PASS", 1: "FAIL"}.get(proc.returncode, "ERR")
    return mode, seed, f"{verdict} rc={proc.returncode} [{last}]"


def main() -> None:
    jobs = [(m, s) for m in MODES for s in range(50)]
    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(run, jobs))
    for mode, seed, line in results:
        print(mode, seed, line)
    for mode in MODES:
        fails = sum(1 for m, _, line in results if m == mode and line.startswith("FAIL"))
        errs = sum(1 for m, _, line in results if m == mode and line.startswith("ERR"))
        print(f"SUMMARY {mode}: fails {fails}/50 errors {errs}")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
