"""Run the FC1 project suite on one solution file in a fresh scratch directory (outside the repository).

Usage: python -I ledgers/FC1/scripts/FC1-c-r10/suite_run.py <solution.py> <seed> [<seed> ...]
Prints one line per seed: SEED <n> RESULT <pytest summary line>. Exit 0 only if every seed passes.
The grader files are copied from the checkout's course/modules/FC/FC1/grader/, so the run uses the pinned suite.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
GRADER = REPO / "course" / "modules" / "FC" / "FC1" / "grader"


def main(argv: list[str]) -> int:
    solution = Path(argv[1]).resolve()
    seeds = argv[2:]
    failed = False
    for seed in seeds:
        scratch = Path(tempfile.mkdtemp(prefix="fc1suite-"))
        try:
            for name in ("test_project.py", "instance.py"):
                shutil.copy(GRADER / name, scratch / name)
            shutil.copy(solution, scratch / "instruments.py")
            env = {**os.environ, "QF_SEED": seed, "PYTHONDONTWRITEBYTECODE": "1"}
            proc = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    "-m",
                    "pytest",
                    "-q",
                    "-p",
                    "no:cacheprovider",
                    "--assert=plain",
                    "-W",
                    "error",
                    "test_project.py",
                ],
                cwd=scratch,
                env=env,
                capture_output=True,
                text=True,
                timeout=300,
            )
            lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
            summary = lines[-1] if lines else "(no output)"
            print(f"SEED {seed} RESULT {summary}")
            if proc.returncode != 0:
                failed = True
        finally:
            shutil.rmtree(scratch, ignore_errors=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
