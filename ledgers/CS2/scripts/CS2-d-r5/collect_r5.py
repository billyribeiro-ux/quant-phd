"""Round-5 verifier (CS2-d): collect-only count of the CS2 autograder on the reference, seeds 0-49.

Each seed gets a fresh workspace (reference.py copied as streamstats.py, grader files copied by run_graders.workspace).
Prints the collected count per seed and the set of distinct counts.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, workspace  # noqa: E402

u = unit("CS2")
cfg = panel(u)
counts: Counter[int] = Counter()
for seed in range(50):
    work = workspace(u, u.directory / "grader" / "reference.py", cfg)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", cfg["suite"]],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
        )
        match = re.search(r"(\d+) tests? collected", result.stdout + result.stderr)
        n = int(match.group(1)) if match else -1
        counts[n] += 1
    finally:
        shutil.rmtree(work, ignore_errors=True)
print("seeds 0-49 collected counts:", dict(counts))
print("python", sys.version.split()[0])
