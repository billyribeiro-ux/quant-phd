"""Runs every candidate module through the BK4 suite on seeds 0-49, each in its own scratch directory.

Usage: run_candidates_r7.py <checkout> <candidate.py> [<candidate.py> ...]
Prints one line per candidate: the count of seeds passed out of 50, and the first failing test per failing seed.
The suite, instance and candidate are copied; nothing in the checkout is modified.
"""

from __future__ import annotations

import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(sys.argv[1])
PY = ROOT / ".venv/bin/python"
GRADER = ROOT / "course/modules/BK/BK4/grader"


def run(candidate: pathlib.Path) -> None:
    passed = 0
    failures: dict[str, int] = {}
    for seed in range(50):
        work = pathlib.Path(tempfile.mkdtemp(prefix="bk4cand7_"))
        try:
            shutil.copy(GRADER / "test_project.py", work)
            shutil.copy(GRADER / "instance.py", work)
            shutil.copy(candidate, work / "clearing_house.py")
            env = dict(os.environ, QF_SEED=str(seed), PYTHONDONTWRITEBYTECODE="1")
            proc = subprocess.run(
                [str(PY), "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                 "test_project.py"],
                cwd=work, env=env, capture_output=True, text=True, check=False,
            )
            if proc.returncode == 0:
                passed += 1
            else:
                names = re.findall(r"FAILED \S+::(\S+)", proc.stdout)
                for name in names[:1] or ["(no FAILED line)"]:
                    failures[name] = failures.get(name, 0) + 1
        finally:
            shutil.rmtree(work, ignore_errors=True)
    print(f"{candidate.name}: passed {passed}/50 seeds")
    for name, count in sorted(failures.items(), key=lambda kv: -kv[1]):
        print(f"  first failing test {name}: {count} seeds")


if __name__ == "__main__":
    for arg in sys.argv[2:]:
        run(pathlib.Path(arg))
