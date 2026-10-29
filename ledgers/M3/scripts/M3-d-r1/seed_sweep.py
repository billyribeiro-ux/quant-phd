"""Run the M3 project suite (grader/test_project.py) on one candidate module over a seed range.

Usage: seed_sweep.py <candidate.py> <first_seed> <last_seed>
Copies the grader files and the candidate into a fresh scratch directory, runs pytest with the same flags the
browser uses, and prints one line per seed with the pass count and the failing test names.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHECKOUT = Path(__file__).resolve().parents[4]
GRADER = CHECKOUT / "course" / "modules" / "M" / "M3" / "grader"


def main() -> int:
    candidate = Path(sys.argv[1]).resolve()
    first, last = int(sys.argv[2]), int(sys.argv[3])
    py = str(CHECKOUT / ".venv" / "bin" / "python")
    failures = 0
    for seed in range(first, last + 1):
        work = Path(tempfile.mkdtemp(prefix="m3d-", dir="/tmp/m3-v/d"))
        shutil.copy(GRADER / "test_project.py", work)
        shutil.copy(GRADER / "instance.py", work)
        shutil.copy(candidate, work / "covariance_doctor.py")
        env = {**os.environ, "QF_SEED": str(seed)}
        run = subprocess.run(
            [py, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work,
            env={**env, "PYTHONPATH": str(work)},
            capture_output=True,
            text=True,
        )
        last_line = run.stdout.strip().splitlines()[-1] if run.stdout.strip() else "no output"
        if run.returncode != 0:
            failures += 1
            failed = [ln.split("::", 1)[1].split(" ")[0] for ln in run.stdout.splitlines() if ln.startswith("FAILED")]
            print(f"seed {seed}: FAIL {last_line} :: {failed[:4]}")
        else:
            print(f"seed {seed}: PASS {last_line}")
        shutil.rmtree(work, ignore_errors=True)
    print(f"{candidate.name}: {failures} failing seed(s) of {last - first + 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
