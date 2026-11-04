"""Run candidate clearing_house.py files against the BK4 suite, one seed per pytest process.

Usage: run_candidates.py <grader_dir> <seeds_lo> <seeds_hi> <candidate.py> [...]
Each candidate is copied into a fresh temporary directory as clearing_house.py, beside the grader files, and the suite
is run with QF_SEED set to each seed under the browser's flags (--assert=plain -W error). Prints PASS/FAIL per candidate.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PYTHON = "/Users/billyribeiro/.fanout/wt/verifyE3-BK4-c/.venv/bin/python"
grader_dir = Path(sys.argv[1])
lo, hi = (int(x) for x in sys.argv[2:4])
candidates = [Path(p) for p in sys.argv[4:]]
for cand in candidates:
    fails: list[str] = []
    for seed in range(lo, hi + 1):
        work = Path(tempfile.mkdtemp(prefix="bk4cand."))
        try:
            for f in ("instance.py", "test_project.py"):
                shutil.copy(grader_dir / f, work / f)
            shutil.copy(cand, work / "clearing_house.py")
            env = dict(os.environ, QF_SEED=str(seed), PYTHONDONTWRITEBYTECODE="1")
            proc = subprocess.run(
                [PYTHON, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                 "test_project.py"],
                cwd=work, env=env, capture_output=True, text=True, timeout=300,
            )
            if proc.returncode != 0:
                tail = (proc.stdout.strip().splitlines() or ["?"])[-1]
                fails.append(f"seed {seed}: {tail}")
        finally:
            shutil.rmtree(work, ignore_errors=True)
    status = "PASS" if not fails else f"FAIL ({len(fails)} seeds)"
    print(f"{cand.name}: {status}")
    for line in fails[:5]:
        print("   ", line)
