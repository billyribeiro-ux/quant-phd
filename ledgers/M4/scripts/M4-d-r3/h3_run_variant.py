"""Run the M4 grader against one solution file on a seed window (same flags as tools/run_graders.py).

Usage: h3_run_variant.py <solution.py> <grader_dir> <seeds lo-hi>
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sol, grader, window = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
lo, _, hi = window.partition("-")
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
results = []
for seed in range(int(lo), int(hi or lo) + 1):
    work = Path(tempfile.mkdtemp(prefix="h3-var-"))
    try:
        for name in ("test_project.py", "instance.py"):
            shutil.copy(grader / name, work / name)
        shutil.copy(sol, work / "tail_risk.py")
        r = subprocess.run([sys.executable, "-m", "pytest", *FLAGS, "test_project.py"], cwd=work,
                           capture_output=True, text=True, check=False,
                           env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"})
        failed = re.findall(r"FAILED \S+::(\S+)", r.stdout)
        if r.returncode != 0:
            results.append((seed, ", ".join(failed) or "collection/import error"))
    finally:
        shutil.rmtree(work, ignore_errors=True)
print(f"{sol.name}: {'SURVIVES' if not results else 'KILLED'} on {int(hi or lo) - int(lo) + 1 - len(results)} of {int(hi or lo) - int(lo) + 1} seeds passing; failing seeds: {len(results)}")
for seed, names in results[:3]:
    print(f"   seed {seed}: {names}")
