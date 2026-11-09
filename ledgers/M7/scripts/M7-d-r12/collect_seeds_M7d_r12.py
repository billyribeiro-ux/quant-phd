"""Collect-only count of the M7 project suite for each seed, in a scratch copy with the reference as the solution.

Usage: python -I collect_seeds_M7d_r12.py <repo_root> <first_seed> <last_seed>
Runs pytest --collect-only with the page's flags (--assert=plain -W error) and prints 'seed N collected K'.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
first, last = int(sys.argv[2]), int(sys.argv[3])
grader = repo / "course" / "modules" / "M" / "M7" / "grader"
python = repo / ".venv" / "bin" / "python"
for seed in range(first, last + 1):
    work = Path(tempfile.mkdtemp(prefix="m7d-collect-"))
    try:
        for name in ("test_project.py", "instance.py"):
            shutil.copy(grader / name, work / name)
        shutil.copy(grader / "reference.py", work / "constrained_allocator.py")
        env = dict(os.environ, QF_SEED=str(seed))
        proc = subprocess.run(
            [str(python), "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
             "--collect-only", "test_project.py"],
            cwd=work, env=env, capture_output=True, text=True,
        )
        tail = [line for line in proc.stdout.splitlines() if line.strip()][-1:]
        print(f"seed {seed} exit {proc.returncode} tail: {tail}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
