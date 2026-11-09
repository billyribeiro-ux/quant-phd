"""Re-run the three round-14 mutants (w14d_*) through the suite on seeds 0-9 after their docstrings were reformatted.

Run: python -I ledgers/M7/scripts/M7-d-r14/recheck_new_mutants_r14.py <repo_root>
Prints, per mutant, the first seed whose suite run fails and the first failing test.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
grader = root / "course/modules/M/M7/grader"
for mutant in sorted((root / "ledgers/M7/mutants").glob("w14d_*.py")):
    killed = None
    for seed in range(10):
        work = Path(tempfile.mkdtemp(prefix="m7w14d-"))
        try:
            shutil.copy(grader / "test_project.py", work / "test_project.py")
            shutil.copy(grader / "instance.py", work / "instance.py")
            shutil.copy(mutant, work / "constrained_allocator.py")
            res = subprocess.run(
                [sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                cwd=work, capture_output=True, text=True, check=False,
                env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            )
            if res.returncode != 0:
                found = re.search(r"FAILED \S+::(\S+)", res.stdout)
                killed = (seed, found.group(1) if found else "?")
                break
        finally:
            shutil.rmtree(work, ignore_errors=True)
    print(mutant.name, "KILLED at seed", killed[0], "by", killed[1] if killed else None, "" if killed else "SURVIVED 0-9")
