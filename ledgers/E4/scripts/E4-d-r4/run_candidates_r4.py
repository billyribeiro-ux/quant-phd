"""Run candidate solver files through the E4 project suite (grader/test_project.py) for the seeds given, in parallel.

Usage: python -I ledgers/E4/scripts/E4-d-r4/run_candidates_r4.py <repo-root> <seeds a-b> <candidate.py> [...]
Each candidate is copied as solver.py into a fresh temporary workspace with test_project.py and instance.py, and pytest
runs with the browser's flags (-q -p no:cacheprovider --assert=plain -W error) and QF_SEED set.
Prints one line per candidate: PASS/FAIL, the count of failing seeds, and the failing test names (no answers printed).
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root = Path(sys.argv[1])
lo, _, hi = sys.argv[2].partition("-")
seeds = list(range(int(lo), int(hi or lo) + 1))
grader = root / "course/modules/E/E4/grader"
cands = [Path(c) for c in sys.argv[3:]]


def run_one(args: tuple[Path, int]) -> tuple[str, int, list[str]]:
    src, seed = args
    work = Path(tempfile.mkdtemp(prefix="e4d4-cand-"))
    try:
        shutil.copy(grader / "test_project.py", work / "test_project.py")
        shutil.copy(grader / "instance.py", work / "instance.py")
        shutil.copy(src, work / "solver.py")
        res = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work,
            capture_output=True,
            text=True,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            timeout=600,
        )
        if res.returncode == 0:
            return src.name, seed, []
        found = re.findall(r"FAILED \S+::(\S+)", res.stdout)
        return src.name, seed, (found[:3] if found else ["<no FAILED line; exit %d>" % res.returncode])
    finally:
        shutil.rmtree(work, ignore_errors=True)


jobs = [(c, s) for c in cands for s in seeds]
with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(run_one, jobs))
for c in cands:
    rows = [r for r in results if r[0] == c.name]
    bad = [(s, t) for _, s, t in rows if t]
    status = "PASS" if not bad else "FAIL"
    tests = sorted({x for _, t in bad for x in t})
    print(f"{c.name}: {status} seeds {seeds[0]}-{seeds[-1]} failing_seeds={len(bad)} tests={tests[:6]}")
