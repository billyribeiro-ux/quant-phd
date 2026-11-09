"""Run candidate market_maker.py modules against the PC3 suite (checkout grader files), one scratch dir each.

Usage: .venv/bin/python ledgers/PC3/scripts/PC3-c-r14/run_candidates.py <checkout-root> <candidate.py> [...]
Each candidate is copied to a fresh scratch directory as market_maker.py, next to the checkout's engine.py,
instance.py and test_project.py. pytest runs with QF_SEED=0 (the suite covers seeds 0-49 regardless).
Prints PASS/FAIL, the pass and fail counts and the first failing test id.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1])
grader = root / "course/modules/PC/PC3/grader"
for cand in sys.argv[2:]:
    work = Path(tempfile.mkdtemp(prefix="pc3c-r14-"))
    try:
        for name in ("engine.py", "instance.py", "test_project.py"):
            shutil.copy(grader / name, work / name)
        shutil.copy(cand, work / "market_maker.py")
        env = dict(os.environ, QF_SEED="0")
        r = subprocess.run(
            [str(root / ".venv/bin/python"), "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work, env=env, capture_output=True, text=True,
        )
        out = r.stdout + r.stderr
        summary = out.strip().splitlines()[-1] if out.strip() else "(no output)"
        failed = re.findall(r"FAILED (\S+)", out)
        status = "PASS" if r.returncode == 0 else "FAIL"
        first = failed[0] if failed else "-"
        print(f"{status} {Path(cand).name}: {summary} | first={first}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
