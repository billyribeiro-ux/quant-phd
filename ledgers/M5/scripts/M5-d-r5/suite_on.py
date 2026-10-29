"""Run the M5 project autograder (grader/test_project.py + instance.py) on a candidate solver.

usage: suite_on.py <solver.py> <seed-spec> [--collect]
Copies the suite and instance into a fresh temp dir, installs the candidate as contraction_solver.py,
and runs pytest with the browser flags (--assert=plain -W error) under QF_SEED for each seed.
Prints one line per seed: PASS/FAIL and the number of failing tests.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/tmp/verifyB5-M5-d")
GRADER = ROOT / "course/modules/M/M5/grader"
PY = ROOT / ".venv/bin/python"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def run(solver: Path, seed: int, collect: bool) -> str:
    work = Path(tempfile.mkdtemp(prefix="m5d5-"))
    try:
        shutil.copy(GRADER / "test_project.py", work)
        shutil.copy(GRADER / "instance.py", work)
        shutil.copy(solver, work / "contraction_solver.py")
        args = [str(PY), "-m", "pytest", *FLAGS, "test_project.py"]
        if collect:
            args = [str(PY), "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "test_project.py"]
        r = subprocess.run(args, cwd=work, capture_output=True, text=True, env={
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}, timeout=600)
        out = r.stdout + r.stderr
        last = out.strip().splitlines()[-1] if out.strip() else ""
        if collect:
            return f"seed {seed}: {last}"
        return f"seed {seed}: {'PASS' if r.returncode == 0 else 'FAIL'} | {last}"
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    solver = Path(sys.argv[1]).resolve()
    spec = sys.argv[2]
    collect = "--collect" in sys.argv
    if "-" in spec:
        a, b = spec.split("-")
        seeds = range(int(a), int(b) + 1)
    else:
        seeds = [int(spec)]
    for s in seeds:
        print(run(solver, s, collect))
