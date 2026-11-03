"""Count pytest checks collected for seeds 0..49 with the reference solution as scanner.py (scratch copy in /tmp)."""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])  # checkout root (absolute)
GRADER = ROOT / "course/modules/FC/FC2/grader"
counts: dict[int, int] = {}
for seed in range(50):
    work = Path(f"/tmp/fc2d-r3-ind/collect_{seed}")
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    for name in ("test_project.py", "instance.py"):
        shutil.copy(GRADER / name, work / name)
    shutil.copy(GRADER / "reference.py", work / "scanner.py")
    env = dict(os.environ, QF_SEED=str(seed))
    out = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "test_project.py"],
        cwd=work, env=env, capture_output=True, text=True,
    ).stdout
    n = len([line for line in out.splitlines() if re.search(r"::", line)])
    counts[seed] = n
print("distinct counts:", sorted(set(counts.values())))
print("seeds:", len(counts), "min", min(counts.values()), "max", max(counts.values()))
