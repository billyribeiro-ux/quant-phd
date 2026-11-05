"""Stage one candidate tail_risk.py with the grader's instance.py and test_project.py, run the suite per seed.

Usage: python harness_d11.py <candidate.py> <seed> [<seed> ...]
Prints one line per seed: seed, exit code, last pytest summary line. Runs in a fresh temp directory per call.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "M" / "M4" / "grader"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def main() -> int:
    candidate = Path(sys.argv[1]).resolve()
    seeds = [int(s) for s in sys.argv[2:]]
    for seed in seeds:
        work = Path(tempfile.mkdtemp(prefix="m4d11-"))
        shutil.copy(GRADER / "instance.py", work / "instance.py")
        shutil.copy(GRADER / "test_project.py", work / "test_project.py")
        shutil.copy(candidate, work / "tail_risk.py")
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        res = subprocess.run(
            [sys.executable, "-m", "pytest", *FLAGS, "test_project.py"],
            cwd=work,
            capture_output=True,
            text=True,
            env=env,
            timeout=600,
            check=False,
        )
        lines = [ln for ln in (res.stdout + res.stderr).splitlines() if ln.strip()]
        summary = lines[-1] if lines else "(no output)"
        print(f"seed {seed}: exit {res.returncode}: {summary}")
        shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
