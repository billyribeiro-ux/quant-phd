"""Verifier helper (round 17): build a grader workspace for a candidate solution and run the M7 suite on it."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD17-M7-d")
GRADER = ROOT / "course/modules/M/M7/grader"
PYTEST_FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def workspace(solution: Path) -> Path:
    work = Path(tempfile.mkdtemp(prefix="v17m7d-", dir="/private/tmp"))
    shutil.copy(GRADER / "test_project.py", work / "test_project.py")
    shutil.copy(GRADER / "instance.py", work / "instance.py")
    shutil.copy(solution, work / "constrained_allocator.py")
    return work


def run(solution: Path, seed: int, collect: bool = False) -> tuple[int, str]:
    work = workspace(solution)
    args = [sys.executable, "-I", "-m", "pytest", *PYTEST_FLAGS]
    if collect:
        args = [sys.executable, "-I", "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider"]
    args.append("test_project.py")
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
    res = subprocess.run(args, cwd=work, capture_output=True, text=True, env=env, check=False, timeout=600)
    shutil.rmtree(work, ignore_errors=True)
    return res.returncode, (res.stdout + res.stderr)


if __name__ == "__main__":
    sol = Path(sys.argv[1]).resolve()
    seeds = [int(s) for s in sys.argv[2].split(",")] if len(sys.argv) > 2 else [0]
    for s in seeds:
        code, out = run(sol, s)
        last = [ln for ln in out.splitlines() if ln.strip()][-1:]
        print(f"seed={s} exit={code} last={last}")
