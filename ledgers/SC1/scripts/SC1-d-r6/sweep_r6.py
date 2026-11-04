"""Verifier r4: run the browser suite (test_project.py, --assert=plain -W error) for a candidate over a seed range, in parallel.

Usage: sweep_r4.py <candidate.py> <seed-from> <seed-to-exclusive> [workers]
Prints the failing seeds and their last pytest line. Each run has its own scratch directory.
"""
import concurrent.futures as cf
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE6-SC1-d")
GRADER = ROOT / "course/modules/SC/SC1/grader"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
cand = Path(sys.argv[1]).resolve()
lo, hi = int(sys.argv[2]), int(sys.argv[3])
workers = int(sys.argv[4]) if len(sys.argv) > 4 else 16


def run(seed):
    work = Path(tempfile.mkdtemp(prefix="sc1d-r6-"))
    try:
        for name in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / name, work / name)
        shutil.copy(cand, work / "bm_checks.py")
        env = {**os.environ, "QF_SEED": str(seed)}
        try:
            p = subprocess.run([sys.executable, "-I", "-m", "pytest", *FLAGS, "test_project.py"],
                               cwd=work, env=env, capture_output=True, text=True, timeout=120)
            last = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr[-200:]
            return seed, p.returncode == 0, last
        except subprocess.TimeoutExpired:
            return seed, False, "TIMEOUT"
    finally:
        shutil.rmtree(work, ignore_errors=True)


bad = []
with cf.ThreadPoolExecutor(workers) as ex:
    for seed, ok, last in ex.map(run, range(lo, hi)):
        if not ok:
            bad.append((seed, last))
print(f"{cand.name}: {hi - lo - len(bad)}/{hi - lo} seeds pass; failing: {len(bad)}")
for seed, last in bad[:12]:
    print(f"   seed {seed}: {last}")
