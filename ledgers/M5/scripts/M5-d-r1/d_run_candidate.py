"""Run the M5 project suite against one candidate contraction_solver.py for a range of seeds.

Usage: python3 -I ledgers/M5/scripts/M5-d-r1/d_run_candidate.py <candidate.py> <seeds e.g. 0-9>
Copies the candidate, instance.py and test_project.py into a fresh scratch directory (outside the repo),
runs pytest under the browser flags, and prints one line per seed: PASS or FAIL plus the first failing test name.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = "/Users/billyribeiro/.fanout/wt/verifyS1-M5-d"
GRADER = os.path.join(REPO, "course/modules/M/M5/grader")
PY = os.path.join(REPO, ".venv/bin/python")


def main() -> None:
    candidate = os.path.abspath(sys.argv[1])
    lo, hi = (int(x) for x in sys.argv[2].split("-"))
    for seed in range(lo, hi + 1):
        scratch = tempfile.mkdtemp(prefix="d_cand_")
        shutil.copy(candidate, os.path.join(scratch, "contraction_solver.py"))
        shutil.copy(os.path.join(GRADER, "instance.py"), scratch)
        shutil.copy(os.path.join(GRADER, "test_project.py"), scratch)
        env = {"QF_SEED": str(seed), "PATH": os.environ.get("PATH", ""), "HOME": os.environ.get("HOME", "")}
        proc = subprocess.run(
            [PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=scratch,
            env=env,
            capture_output=True,
            text=True,
            timeout=600,
        )
        out = proc.stdout + proc.stderr
        failed = re.findall(r"^FAILED test_project.py::(\S+)", out, flags=re.M)
        summary = out.strip().splitlines()[-1] if out.strip() else ""
        status = "PASS" if proc.returncode == 0 else "FAIL"
        print(f"seed {seed}: {status} rc={proc.returncode} | {summary} | failed={len(failed)} first={failed[:3]}")
        shutil.rmtree(scratch)


if __name__ == "__main__":
    main()
