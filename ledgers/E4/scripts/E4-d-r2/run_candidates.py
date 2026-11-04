"""Run candidate solver files through the E4 project suite (grader/test_project.py) on seeds given.

Usage: python -I ledgers/E4/scripts/E4-d-r2/run_candidates.py <repo-root> <seeds a-b> <candidate.py> [...]
Each candidate is copied as solver.py into a fresh temporary workspace together with test_project.py and instance.py,
then pytest runs with the browser's flags (-q -p no:cacheprovider --assert=plain -W error) and QF_SEED set.
Prints PASS/FAIL per candidate with the first failing seed and the failing test name (no answers are printed).
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1])
lo, _, hi = sys.argv[2].partition("-")
seeds = range(int(lo), int(hi or lo) + 1)
grader = root / "course/modules/E/E4/grader"
for cand in sys.argv[3:]:
    src = Path(cand)
    failures = []
    for seed in seeds:
        work = Path(tempfile.mkdtemp(prefix="e4d-cand-"))
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
                timeout=300,
            )
            if res.returncode != 0:
                found = re.findall(r"FAILED \S+::(\S+)", res.stdout)
                failures.append((seed, found[:3] if found else res.stdout[-300:]))
        finally:
            shutil.rmtree(work, ignore_errors=True)
    status = "PASS" if not failures else "FAIL"
    print(f"{src.name}: {status} seeds {seeds.start}-{seeds.stop-1} failing={len(failures)}", failures[:3])
