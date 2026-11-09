"""Run every alternative correct implementation of E1-d against the current E1 grader on seeds 0-49.

Usage: <checkout>/.venv/bin/python <checkout>/ledgers/E1/scripts/E1-d-r4/run_alts_r4.py
Each alternative is copied with the grader files into a fresh temporary directory; the suite runs there with QF_SEED.
"""

import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHK = Path(sys.argv[1]).resolve()
GRADER = CHK / "course/modules/E/E1/grader"
PY = str(CHK / ".venv/bin/python")
alts: list[str] = []
for pat in ("ledgers/E1/scripts/E1-d-r2/alternatives/*.py", "ledgers/E1/scripts/E1-d-r3/alternatives/*.py",
            "ledgers/E1/scripts/E1-d-r4/alternatives/*.py", "ledgers/E1/scripts/E1-d-r1/alt/*.py"):
    alts += sorted(glob.glob(str(CHK / pat)))
for src_s in alts:
    src = Path(src_s)
    work = Path(tempfile.mkdtemp(prefix="e1d-alt-"))
    for name in ("instance.py", "test_project.py"):
        shutil.copy(GRADER / name, work / name)
    shutil.copy(src, work / "market_structure.py")
    failures = []
    for seed in range(50):
        env = dict(os.environ, QF_SEED=str(seed))
        r = subprocess.run(
            [PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work, env=env, capture_output=True, text=True,
        )
        if r.returncode != 0:
            m = re.search(r"FAILED \S+::(\S+)", r.stdout)
            failures.append(f"seed {seed}: {m.group(1) if m else r.stdout[-200:]}")
            if len(failures) >= 3:
                break
    shutil.rmtree(work, ignore_errors=True)
    rel = src.relative_to(CHK)
    print(f"{rel}: {'PASS' if not failures else 'FAIL'} on seeds 0-49" + ("" if not failures else " first: " + "; ".join(failures)))
