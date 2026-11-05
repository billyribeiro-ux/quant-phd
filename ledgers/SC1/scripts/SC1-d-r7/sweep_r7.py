"""Round 7 (SC1-d): run the browser suite (test_project.py, --assert=plain -W error) for a candidate bm_checks.py over
a seed range, in parallel. Each run has its own scratch directory under /tmp, removed afterwards.

Usage (from the checkout root): .venv/bin/python -I ledgers/SC1/scripts/SC1-d-r7/sweep_r7.py <candidate.py> <seed-from> <seed-to-exclusive> [workers]
"""
import concurrent.futures as cf
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/SC/SC1/grader"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
cand = Path(sys.argv[1]).resolve()
lo, hi = int(sys.argv[2]), int(sys.argv[3])
workers = int(sys.argv[4]) if len(sys.argv) > 4 else 16


def run(seed):
    work = Path(tempfile.mkdtemp(prefix="sc1d-r7-"))
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
