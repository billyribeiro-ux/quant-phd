"""Run the M6 project suite (grader/test_project.py) against one martingale_checks solution file.

Usage: run_variant.py SOLUTION.py SEEDS   (SEEDS like 0-49, the same syntax as tools/run_graders.py)
Copies the suite, instance.py and the solution into a fresh temp directory, then runs pytest with the browser flags
once per seed. Prints one line per seed: PASS or FAIL plus the first failing test name, and the collected test count
when --collect is given. The solution is never modified.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path("/Users/billyribeiro/.fanout/wt/verifyC4-M6-d")
GRADER = REPO / "course/modules/M/M6/grader"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def seeds_of(text: str) -> list[int]:
    lo, _, hi = text.partition("-")
    return list(range(int(lo), int(hi or lo) + 1))


def main() -> int:
    solution = Path(sys.argv[1]).resolve()
    args = sys.argv[2:]
    collect = "--collect" in args
    seeds = seeds_of([a for a in args if a != "--collect"][0]) if [a for a in args if a != "--collect"] else [0]
    work = Path(tempfile.mkdtemp(prefix="m6d-r4-"))
    try:
        shutil.copy(GRADER / "test_project.py", work / "test_project.py")
        shutil.copy(GRADER / "instance.py", work / "instance.py")
        shutil.copy(solution, work / "martingale_checks.py")
        failures = 0
        if collect:
            out = subprocess.run(
                [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "test_project.py"],
                cwd=work,
                capture_output=True,
                text=True,
                env={"PATH": os.environ.get("PATH", ""), "QF_SEED": "0", "PYTHONHASHSEED": "0"},
                check=False,
            )
            print("collect-only:", out.stdout.strip().splitlines()[-1] if out.stdout.strip() else out.stderr[-300:])
        for seed in seeds:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", *FLAGS, "test_project.py"],
                cwd=work,
                capture_output=True,
                text=True,
                env={"PATH": os.environ.get("PATH", ""), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
                check=False,
            )
            if result.returncode == 0:
                print(f"seed {seed}: PASS")
            else:
                failures += 1
                failed = re.findall(r"FAILED \S+::(\S+)", result.stdout)
                summary = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else result.stderr[-200:]
                print(f"seed {seed}: FAIL {failed[:3]} | {summary}")
        print(f"solution {solution.name}: {len(seeds) - failures}/{len(seeds)} seeds pass")
        return 1 if failures else 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
