"""Run the M5 project suite (round-2 checkout's test_project.py and instance.py) against one candidate solver.

Usage: python3 -I ledgers/M5/scripts/M5-d-r2/d2_run_candidate.py <candidate.py> <seeds e.g. 0-9>
Copies the candidate, instance.py and test_project.py into a fresh scratch directory under /tmp, runs pytest under the
browser flags, prints one line per seed: PASS/FAIL, the summary line and the first failing tests.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
GRADER = os.path.join(REPO, "course/modules/M/M5/grader")
PY = os.path.join(REPO, ".venv/bin/python")


def main() -> None:
    candidate = os.path.abspath(sys.argv[1])
    lo, hi = (int(x) for x in sys.argv[2].split("-"))
    for seed in range(lo, hi + 1):
        scratch = tempfile.mkdtemp(prefix="d2_cand_")
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
            check=False,
        )
        out = proc.stdout + proc.stderr
        failed = re.findall(r"^FAILED test_project.py::(\S+)", out, flags=re.M)
        summary = out.strip().splitlines()[-1] if out.strip() else ""
        status = "PASS" if proc.returncode == 0 else "FAIL"
        print(f"seed {seed}: {status} rc={proc.returncode} | {summary} | failed={len(failed)} first={failed[:3]}")
        shutil.rmtree(scratch)


if __name__ == "__main__":
    main()
