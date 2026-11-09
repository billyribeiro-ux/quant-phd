"""Round-13 BK4-c: run every alternative implementation (alt1..alt7) against the BK4 suite on seeds 0-49.

Each alternative is copied as clearing_house.py into its own scratch directory with test_project.py and instance.py.
Run from the checkout root: python3 -I ledgers/BK4/scripts/BK4-c-r13/run_alts_r13.py
"""

import glob
import os
import shutil
import subprocess
import sys

ROOT = os.getcwd()
PY = os.path.join(ROOT, ".venv", "bin", "python")
GRADER = os.path.join(ROOT, "course", "modules", "BK", "BK4", "grader")
SCRATCH = "/tmp/bk4c_r14/alts"
results = {}
for alt in sorted(glob.glob(os.path.join(ROOT, "ledgers", "BK4", "alternatives", "*.py"))):
    name = os.path.basename(alt)[:-3]
    d = os.path.join(SCRATCH, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    shutil.copy(alt, os.path.join(d, "clearing_house.py"))
    shutil.copy(os.path.join(GRADER, "test_project.py"), d)
    shutil.copy(os.path.join(GRADER, "instance.py"), d)
    passed, failed = [], []
    for seed in range(50):
        env = dict(os.environ, QF_SEED=str(seed))
        r = subprocess.run(
            [PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=d, env=env, capture_output=True, text=True,
        )
        (passed if r.returncode == 0 else failed).append(seed)
    results[name] = (len(passed), failed)
    print(f"{name}: {len(passed)}/50 seeds pass; failing seeds {failed}")
ok = all(not f for _, f in results.values())
print("ALTERNATIVES", "ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
