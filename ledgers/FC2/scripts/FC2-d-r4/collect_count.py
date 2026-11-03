"""Count pytest --collect-only checks of FC2 test_project.py per seed, with a given solution file as scanner.py.

Usage: python -I collect_count.py <grader_dir> <solution_file> <seeds_from> <seeds_to>
Prints one line per seed: seed, collected count, and the pytest return code.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

grader = Path(sys.argv[1]).resolve()
solution = Path(sys.argv[2]).resolve()
lo, hi = int(sys.argv[3]), int(sys.argv[4])
counts: dict[int, int] = {}
for seed in range(lo, hi + 1):
    work = Path(tempfile.mkdtemp(prefix="fc2-collect-"))
    for name in ("test_project.py", "instance.py"):
        shutil.copy(grader / name, work / name)
    shutil.copy(solution, work / "scanner.py")
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
    res = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
        cwd=work, capture_output=True, text=True, env=env, check=False,
    )
    m = re.search(r"(\d+) tests? collected", res.stdout + res.stderr)
    n = int(m.group(1)) if m else -1
    counts[seed] = n
    print(f"seed={seed} collected={n} rc={res.returncode}")
    shutil.rmtree(work)
print("distinct counts:", sorted(set(counts.values())))
