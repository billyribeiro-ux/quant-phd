"""Run candidate instruments.py modules against the FC1 project suite on seeds 0-49 (round 17, FC1-c, delta verifier).

Usage: python -I v17_alt_run.py <checkout> <candidate.py> [<candidate.py> ...]
Each candidate is copied as instruments.py into a fresh scratch directory together with the suite and instance.
The suite is run with the browser's flags: --assert=plain -W error. Prints one line per candidate.
"""

import os
import shutil
import subprocess
import sys
import tempfile

checkout, candidates = sys.argv[1], sys.argv[2:]
grader = os.path.join(checkout, "course/modules/FC/FC1/grader")
python = os.path.join(checkout, ".venv/bin/python")
for cand in candidates:
    failing: list[int] = []
    first_failure = ""
    for seed in range(50):
        work = tempfile.mkdtemp(prefix="fc1c16-alt-")
        try:
            shutil.copy(os.path.join(grader, "test_project.py"), work)
            shutil.copy(os.path.join(grader, "instance.py"), work)
            shutil.copy(cand, os.path.join(work, "instruments.py"))
            env = dict(os.environ, QF_SEED=str(seed))
            run = subprocess.run(
                [python, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                 "test_project.py"],
                cwd=work, env=env, capture_output=True, text=True, timeout=120,
            )
            if run.returncode != 0:
                failing.append(seed)
                if not first_failure:
                    first_failure = [l for l in run.stdout.splitlines() if l.startswith("FAILED")][:1].__repr__()
        finally:
            shutil.rmtree(work, ignore_errors=True)
    status = "PASS" if not failing else "FAIL"
    print(f"{status} {os.path.basename(cand)}: failing seeds {len(failing)}/50 {failing[:10]} {first_failure}")
