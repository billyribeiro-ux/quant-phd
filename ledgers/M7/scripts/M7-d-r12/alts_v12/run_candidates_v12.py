"""Run candidate solutions through the M7 grader (test_project.py, instance.py) with the browser's pytest flags.

Usage: python -I -W error run_candidates_v12.py <repo_root> <first_seed> <last_seed> <candidate.py> [...]
Prints, per candidate, the seeds that pass, and for the first failing seed the first failing test names.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
first, last = int(sys.argv[2]), int(sys.argv[3])
grader = root / "course/modules/M/M7/grader"
flags = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
for cand in (Path(c) for c in sys.argv[4:]):
    passed = []
    first_fail = None
    for seed in range(first, last + 1):
        work = Path(tempfile.mkdtemp(prefix="m7v12-"))
        shutil.copy(grader / "test_project.py", work / "test_project.py")
        shutil.copy(grader / "instance.py", work / "instance.py")
        shutil.copy(cand, work / "constrained_allocator.py")
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        res = subprocess.run([sys.executable, "-m", "pytest", *flags, "test_project.py"],
                             cwd=work, capture_output=True, text=True, check=False, env=env, timeout=600)
        shutil.rmtree(work, ignore_errors=True)
        if res.returncode == 0:
            passed.append(seed)
        elif first_fail is None:
            names = re.findall(r"^FAILED test_project.py::(\S+)", res.stdout, re.M)
            first_fail = (seed, names[:4] or [res.stdout[-200:]])
    print(f"{cand.name}: passes {len(passed)}/{last - first + 1} seeds; first failing: {first_fail}")
    sys.stdout.flush()
