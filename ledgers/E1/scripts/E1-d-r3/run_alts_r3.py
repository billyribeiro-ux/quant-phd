"""Run each alternative correct implementation against the current E1 grader on seeds 0-49.

Usage: .venv/bin/python ledgers/E1/scripts/E1-d-r3/run_alts_r3.py <alt.py> [<alt.py> ...]
Each alternative is copied with the grader files into a fresh temporary directory; the suite runs
from there with QF_SEED set per seed. Prints PASS/FAIL per alternative and the first failing test.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GRADER = Path("/tmp/verifyB3-E1-d/course/modules/E/E1/grader")
PY = "/tmp/verifyB3-E1-d/.venv/bin/python"

for alt in sys.argv[1:]:
    src = Path(alt).resolve()
    work = Path(tempfile.mkdtemp(prefix="e1d-alt-"))
    for name in ("instance.py", "test_project.py"):
        shutil.copy(GRADER / name, work / name)
    shutil.copy(src, work / "market_structure.py")
    failures = []
    for seed in range(50):
        env = dict(os.environ, QF_SEED=str(seed))
        r = subprocess.run(
            [PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work, env=env, capture_output=True, text=True,
        )
        if r.returncode != 0:
            m = re.search(r"FAILED \S+::(\S+)", r.stdout)
            failures.append(f"seed {seed}: {m.group(1) if m else r.stdout[-200:]}")
            if len(failures) >= 3:
                break
    shutil.rmtree(work, ignore_errors=True)
    print(f"{src.name}: {'PASS' if not failures else 'FAIL'} on seeds 0-49" + ("" if not failures else " first: " + "; ".join(failures)))
