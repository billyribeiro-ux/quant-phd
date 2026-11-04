"""Run the BK4 suite (grader/test_project.py) against one candidate clearing_house.py for a seed range.

Usage: .venv/bin/python ledgers/BK4/scripts/BK4-c-r1/grade_candidate.py <candidate.py> <lo>-<hi>
Each seed runs in a fresh temporary workspace with the same pytest flags as the browser and tools/run_graders.py.
Prints one line per seed: PASS or FAIL with the first failing test name, and a summary line.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "BK" / "BK4" / "grader"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def run(candidate: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="bk4c-cand-"))
    try:
        for name in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / name, work / name)
        shutil.copy(candidate, work / "clearing_house.py")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", *FLAGS, "test_project.py"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            timeout=300,
        )
        output = result.stdout + result.stderr
        if result.returncode == 0:
            return True, output.strip().splitlines()[-1] if output.strip() else ""
        found = re.findall(r"FAILED \S+::(\S+)", output)
        return False, ",".join(found[:3]) or "collection/import error"
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    candidate = Path(sys.argv[1]).resolve()
    lo, _, hi = sys.argv[2].partition("-")
    seeds = range(int(lo), int(hi or lo) + 1)
    passed = 0
    for seed in seeds:
        ok, detail = run(candidate, seed)
        passed += ok
        print(f"{candidate.name} seed {seed}: {'PASS' if ok else 'FAIL'} {'' if ok else detail}")
    print(f"SUMMARY {candidate.name}: {passed}/{len(seeds)} seeds pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
