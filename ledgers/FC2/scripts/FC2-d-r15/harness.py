"""Stage the FC2 grader in a scratch directory per seed and run the suite (or collect-only) against one solution.

Usage: harness.py <solution.py> <collect|run> <seed-range e.g. 0-49>
Prints one line per seed: seed, mode, pytest summary line. Never touches the course tree.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GRADER = Path("/Users/billyribeiro/.fanout/wt/verifyD15-FC2-d/course/modules/FC/FC2/grader")
PY = "/Users/billyribeiro/.fanout/wt/verifyD15-FC2-d/.venv/bin/python"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def seeds_of(spec: str) -> list[int]:
    lo, _, hi = spec.partition("-")
    return list(range(int(lo), int(hi or lo) + 1))


def main() -> int:
    solution = Path(sys.argv[1]).resolve()
    mode = sys.argv[2]
    rc = 0
    for seed in seeds_of(sys.argv[3]):
        work = Path(tempfile.mkdtemp(prefix=f"fc2d-r15-s{seed}-"))
        shutil.copy(GRADER / "test_project.py", work / "test_project.py")
        shutil.copy(GRADER / "instance.py", work / "instance.py")
        shutil.copy(solution, work / "scanner.py")
        env = dict(os.environ, QF_SEED=str(seed))
        if mode == "collect":
            cmd = [PY, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "test_project.py"]
        else:
            cmd = [PY, "-m", "pytest", *FLAGS, "test_project.py"]
        res = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True, timeout=300)
        lines = [ln for ln in (res.stdout + res.stderr).splitlines() if ln.strip()]
        summary = lines[-1] if lines else "(no output)"
        print(f"seed={seed} mode={mode} exit={res.returncode} :: {summary}")
        if mode == "collect" and res.returncode != 0:
            rc = 1
        if mode == "run" and res.returncode != 0:
            rc = 1
        shutil.rmtree(work, ignore_errors=True)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
