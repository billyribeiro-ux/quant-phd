"""Run the SC1 suite (grader test_project.py, browser flags) on one solution for given seeds, printing failed test ids.

Usage: python run_seed_suite_r3.py <repo-root> <solution.py> <comma-separated seeds>
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root, solution = Path(sys.argv[1]), Path(sys.argv[2])
grader = root / "course/modules/SC/SC1/grader"
for seed in (int(x) for x in sys.argv[3].split(",")):
    work = Path(tempfile.mkdtemp(prefix="sc1d-r3-suite-"))
    try:
        for name in ("test_project.py", "instance.py"):
            shutil.copy(grader / name, work / name)
        shutil.copy(solution, work / "bm_checks.py")
        proc = subprocess.run(
            [sys.executable, "-I", "-m", "pytest", "-q", "-rf", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
             "test_project.py"],
            cwd=work, env={**os.environ, "QF_SEED": str(seed)}, capture_output=True, text=True, timeout=240,
        )
        lines = proc.stdout.strip().splitlines()
        failed = [ln.split(" - ")[0].replace("FAILED ", "") for ln in lines if ln.startswith("FAILED")]
        print(f"seed {seed}: {lines[-1]} {failed}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
