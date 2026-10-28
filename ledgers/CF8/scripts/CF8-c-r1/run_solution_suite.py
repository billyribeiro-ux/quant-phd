"""Run the CF8 project suite (test_project.py) against one candidate treasury_forecast.py on a seed window.

Usage: .venv/bin/python ledgers/CF8/scripts/CF8-c-r1/run_solution_suite.py <solution.py> [seeds, default 0-49]

Copies test_project.py, instance.py and the candidate (as treasury_forecast.py) into a fresh scratch directory and runs
pytest with the browser's flags, once per seed. Prints one line per seed that fails, then a summary.
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
GRADER = ROOT / "course" / "modules" / "CF" / "CF8" / "grader"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def main() -> int:
    solution = Path(sys.argv[1]).resolve()
    lo, _, hi = (sys.argv[2] if len(sys.argv) > 2 else "0-49").partition("-")
    seeds = range(int(lo), int(hi or lo) + 1)
    work = Path(tempfile.mkdtemp(prefix="cf8-suite-"))
    try:
        for name in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / name, work / name)
        shutil.copy(solution, work / "treasury_forecast.py")
        failing: list[str] = []
        for seed in seeds:
            env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
            result = subprocess.run(
                [sys.executable, "-m", "pytest", *FLAGS, "test_project.py"],
                cwd=work, capture_output=True, text=True, check=False, env=env, timeout=300,
            )
            if result.returncode != 0:
                names = re.findall(r"FAILED \S+::(\S+)", result.stdout)
                failing.append(f"seed {seed}: {', '.join(names[:4]) or result.stdout[-300:]}")
        print(f"{solution.name}: {'PASS' if not failing else 'FAIL'} over {len(seeds)} seeds")
        for line in failing[:10]:
            print("  " + line)
        return 0 if not failing else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
