"""Run every correct alternative (round-12 alts plus the earlier ledgers/M4/scripts/alt_*.py) and the reference through
the M4 suite on seeds 0-9, under the browser's pytest flags. Prints one line per (implementation, seed)."""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD12-M4-d")
GRADER = ROOT / "course/modules/M/M4/grader"
SOLS = [GRADER / "reference.py"]
SOLS += sorted((ROOT / "ledgers/M4/scripts/M4-d-r12/alts").glob("alt_r12_*.py"))
SOLS += sorted((ROOT / "ledgers/M4/scripts").glob("alt_*.py"))
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
PY = str(ROOT / ".venv/bin/python")
bad = 0
for sol in SOLS:
    results = []
    for seed in range(10):
        work = Path(tempfile.mkdtemp(prefix="m4-r12-"))
        try:
            for name in ("test_project.py", "instance.py"):
                shutil.copy(GRADER / name, work / name)
            shutil.copy(sol, work / "tail_risk.py")
            r = subprocess.run([PY, "-m", "pytest", *FLAGS, "test_project.py"], cwd=work, capture_output=True, text=True,
                               check=False, env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed),
                                                 "PYTHONHASHSEED": "0"}, timeout=300)
            failed = re.findall(r"FAILED \S+::(\S+)", r.stdout)
            results.append((seed, r.returncode, ", ".join(failed)[:300] or r.stdout.strip().splitlines()[-1]))
        finally:
            shutil.rmtree(work, ignore_errors=True)
    ok = all(rc == 0 for _, rc, _ in results)
    bad += not ok
    print(("PASS" if ok else "FAIL"), sol.relative_to(ROOT), "seeds 0-9:", sum(rc == 0 for _, rc, _ in results), "/ 10")
    for seed, rc, msg in results:
        if rc != 0:
            print("   seed", seed, msg)
print("implementations failing:", bad)
