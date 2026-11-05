"""Run the BK4 project suite (grader/test_project.py) against each implementation on seeds 0-49.

Usage: python3 -I run_impls.py <checkout> <scratch_dir> <implementation file>...
Each implementation is copied to clearing_house.py in its own scratch directory beside copies of the suite and
instance.py, and pytest runs once per seed with QF_SEED set. Prints one line per implementation with the pass count.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

checkout = Path(sys.argv[1])
scratch = Path(sys.argv[2])
impls = [Path(p) for p in sys.argv[3:]]
grader = checkout / "course/modules/BK/BK4/grader"
py = str(checkout / ".venv/bin/python")
for impl in impls:
    work = scratch / impl.stem
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    shutil.copy(grader / "test_project.py", work / "test_project.py")
    shutil.copy(grader / "instance.py", work / "instance.py")
    shutil.copy(impl, work / "clearing_house.py")
    passed, failed = [], []
    for seed in range(50):
        env = dict(os.environ, QF_SEED=str(seed))
        proc = subprocess.run(
            [py, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        (passed if proc.returncode == 0 else failed).append(seed)
    print(f"{impl.name}: pass {len(passed)}/50 seeds; failing seeds {failed}")
