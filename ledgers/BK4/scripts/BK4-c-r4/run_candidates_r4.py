"""Run candidate clearing_house.py files against the BK4 project suite, one seed per pytest process.

Usage: run_candidates_r4.py <checkout_root> <seeds_lo> <seeds_hi> <candidate.py> [...]
Each candidate is copied into a fresh temporary directory as clearing_house.py beside instance.py and test_project.py
(from <checkout_root>/course/modules/BK/BK4/grader), and the suite runs with QF_SEED set, under --assert=plain -W error.
Interpreter: the checkout's .venv python. Prints PASS/FAIL per candidate.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1])
lo, hi = (int(x) for x in sys.argv[2:4])
candidates = [Path(p) for p in sys.argv[4:]]
grader = root / "course/modules/BK/BK4/grader"
python = str(root / ".venv/bin/python")
for cand in candidates:
    fails: list[str] = []
    for seed in range(lo, hi + 1):
        work = Path(tempfile.mkdtemp(prefix="bk4cand4."))
        try:
            for f in ("instance.py", "test_project.py"):
                shutil.copy(grader / f, work / f)
            shutil.copy(cand, work / "clearing_house.py")
            env = dict(os.environ, QF_SEED=str(seed), PYTHONDONTWRITEBYTECODE="1")
            proc = subprocess.run(
                [python, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                cwd=work, env=env, capture_output=True, text=True, timeout=300,
            )
            if proc.returncode != 0:
                tail = (proc.stdout.strip().splitlines() or ["?"])[-1]
                fails.append(f"seed {seed}: {tail}")
        finally:
            shutil.rmtree(work, ignore_errors=True)
    status = "PASS" if not fails else f"FAIL ({len(fails)} seeds)"
    print(f"{cand}: {status}")
    for line in fails[:5]:
        print("   ", line)
