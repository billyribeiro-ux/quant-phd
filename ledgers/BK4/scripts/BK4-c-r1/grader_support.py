"""Support runs for the BK4 grader (BK4-c r1): collect-only count, strict typecheck in layout, and starter output.

Usage:
  .venv/bin/python ledgers/BK4/scripts/BK4-c-r1/grader_support.py collect
  .venv/bin/python ledgers/BK4/scripts/BK4-c-r1/grader_support.py typecheck
  .venv/bin/python ledgers/BK4/scripts/BK4-c-r1/grader_support.py starter
Each mode copies the suite and instance.py into a fresh temporary directory, with the named solution as clearing_house.py.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "BK" / "BK4" / "grader"
PY = sys.executable


def workspace(solution: str) -> Path:
    work = Path(tempfile.mkdtemp(prefix="bk4c-support-"))
    shutil.copy(GRADER / "test_project.py", work / "test_project.py")
    shutil.copy(GRADER / "instance.py", work / "instance.py")
    shutil.copy(GRADER / solution, work / "clearing_house.py")
    return work


def main() -> int:
    mode = sys.argv[1]
    if mode == "collect":
        work = workspace("reference.py")
        result = subprocess.run([PY, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "test_project.py"],
                                cwd=work, capture_output=True, text=True, check=False)
        print(result.stdout.strip().splitlines()[-1])
        shutil.rmtree(work, ignore_errors=True)
        return result.returncode
    if mode == "typecheck":
        work = workspace("reference.py")
        result = subprocess.run([PY, "-m", "mypy", "--strict", "--no-incremental", "test_project.py", "instance.py",
                                 "clearing_house.py"], cwd=work, capture_output=True, text=True, check=False)
        print(result.stdout.strip())
        shutil.rmtree(work, ignore_errors=True)
        return result.returncode
    if mode == "starter":
        work = workspace("starter.py")
        result = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                                 "test_project.py"], cwd=work, capture_output=True, text=True, check=False,
                                env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": "0", "PYTHONHASHSEED": "0"})
        print(result.stdout)
        shutil.rmtree(work, ignore_errors=True)
        return 0
    raise SystemExit(f"unknown mode {mode}")


if __name__ == "__main__":
    sys.exit(main())
