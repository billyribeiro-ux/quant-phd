"""Run the FC2 grader suite (test_project.py, instance.py) against each alternative implementation on seeds 0-49.

Usage: python3 run_alts.py <checkout> <scratch_dir> <python>
Each alternative is copied to scratch/<name>/scanner.py beside the grader files, then pytest runs with the
browser flags (-q -p no:cacheprovider --assert=plain -W error) once per seed.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

checkout, scratch, python = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
grader = checkout / "course/modules/FC/FC2/grader"
alts = sorted((checkout / "ledgers/FC2/scripts/FC2-d-r14/alts").glob("*.py"))
for alt in alts:
    work = scratch / alt.stem
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    shutil.copy(grader / "instance.py", work / "instance.py")
    shutil.copy(grader / "test_project.py", work / "test_project.py")
    shutil.copy(alt, work / "scanner.py")
    failed: list[int] = []
    for seed in range(50):
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        res = subprocess.run(
            [python, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work, env=env, capture_output=True, text=True, check=False,
        )
        if res.returncode != 0:
            failed.append(seed)
            if len(failed) == 1:
                first_fail_tail = "\n".join(res.stdout.splitlines()[-4:])
    status = "PASS" if not failed else f"FAIL on {len(failed)} seeds (first {failed[:5]})"
    print(f"{alt.stem}: {status}")
    if failed:
        print("   first failure tail:", first_fail_tail.replace("\n", " | "))
