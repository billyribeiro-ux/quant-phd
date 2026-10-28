"""Run the M3 suite against one candidate module for seeds given as a range, under the browser flags.

Usage: sweep.py <candidate covariance_doctor.py> <grader dir> <lo> <hi>
Copies the candidate, test_project.py and instance.py into a fresh temporary directory per seed, runs pytest with
-q -p no:cacheprovider --assert=plain -W error, and prints the failing seeds with their failing tests and the pass count.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

cand, grader, lo, hi = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
failing = []
counts = []
for seed in range(lo, hi + 1):
    work = Path(tempfile.mkdtemp(prefix=f"m3r2-{seed}-"))
    shutil.copy(cand, work / "covariance_doctor.py")
    shutil.copy(grader / "test_project.py", work / "test_project.py")
    shutil.copy(grader / "instance.py", work / "instance.py")
    env = dict(os.environ, QF_SEED=str(seed))
    proc = subprocess.run(
        [sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
         "test_project.py"],
        cwd=work, env=env, capture_output=True, text=True,
    )
    last = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else proc.stderr[-300:]
    counts.append(last)
    if proc.returncode != 0:
        names = [ln for ln in proc.stdout.splitlines() if ln.startswith("FAILED")]
        failing.append((seed, names[:4], last))
    shutil.rmtree(work, ignore_errors=True)
print(f"{cand.name}: seeds {lo}-{hi}: {len(failing)} failing seeds of {hi - lo + 1}")
for seed, names, last in failing[:12]:
    print("  seed", seed, last, names)
print("  last pytest line for seed", lo, ":", counts[0] if counts else "none")
