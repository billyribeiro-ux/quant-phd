"""Run the verifier's round-2 alternatives A to C through the unchanged current project suite (verifier round 2).

Usage: .venv/bin/python -I ledgers/M4/scripts/M4-d-r2/run_alternatives_r2.py 0 49
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/M/M4/grader"
HERE = Path(__file__).resolve().parent
lo, hi = int(sys.argv[1]), int(sys.argv[2])
for alt in ("alt_r2_a", "alt_r2_b", "alt_r2_c"):
    fails = []
    for seed in range(lo, hi + 1):
        work = Path(tempfile.mkdtemp(prefix=f"m4alt-{alt}-"))
        try:
            shutil.copy(GRADER / "instance.py", work)
            shutil.copy(GRADER / "test_project.py", work)
            shutil.copy(HERE / f"{alt}.py", work / "tail_risk.py")
            env = dict(os.environ, QF_SEED=str(seed))
            r = subprocess.run(
                [str(ROOT / ".venv/bin/python"), "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider",
                 "--assert=plain", "-W", "error", "test_project.py"],
                cwd=work, env=env, capture_output=True, text=True,
            )
            if r.returncode != 0:
                fails.append((seed, [line for line in r.stdout.splitlines() if line.startswith("FAILED")][:3]))
        finally:
            shutil.rmtree(work, ignore_errors=True)
    print(f"{alt}: {hi - lo + 1 - len(fails)}/{hi - lo + 1} seeds pass; failures: {fails[:5]}")
