"""Run the E4 grader suite (test_project.py, unchanged) against candidate solvers, seed by seed (round 13).

Usage: python -I run_candidates.py <grader_dir> <seeds a-b> <candidate.py> [<candidate.py> ...]
Each candidate is copied to a fresh scratch directory as solver.py next to instance.py and test_project.py.
Prints one line per candidate: PASS/FAIL counts over the seeds and the first failing test names.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PYTEST_FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def run_one(grader: Path, candidate: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="e4cand-"))
    try:
        for name in ("instance.py", "test_project.py"):
            shutil.copy(grader / name, work / name)
        shutil.copy(candidate, work / "solver.py")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", *PYTEST_FLAGS, "test_project.py"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            timeout=600,
        )
        out = result.stdout + result.stderr
        failed = re.findall(r"FAILED test_project.py::(\S+)", out)
        return result.returncode == 0, ";".join(failed[:3])
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    grader = Path(sys.argv[1])
    lo, hi = (int(x) for x in sys.argv[2].split("-"))
    for cand in sys.argv[3:]:
        path = Path(cand)
        passed = 0
        failures: list[str] = []
        for seed in range(lo, hi + 1):
            ok, names = run_one(grader, path, seed)
            if ok:
                passed += 1
            else:
                failures.append(f"seed{seed}:{names or 'import/collection error'}")
        total = hi - lo + 1
        status = "PASS" if passed == total else "FAIL"
        print(f"{status} {path.name}: {passed}/{total} seeds pass; first failures: {failures[:3]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
