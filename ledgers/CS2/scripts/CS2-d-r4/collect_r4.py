"""Round-4: pytest --collect-only count of the CS2 suite on the reference, for seeds 0-49, in fresh workspaces."""

from __future__ import annotations

import collections
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/CS/CS2/grader"
PY = ROOT / ".venv/bin/python"
counts: collections.Counter[str] = collections.Counter()
for seed in range(50):
    work = Path(tempfile.mkdtemp(prefix="cs2col_"))
    try:
        shutil.copy(GRADER / "test_project.py", work / "test_project.py")
        shutil.copy(GRADER / "instance.py", work / "instance.py")
        shutil.copy(GRADER / "reference.py", work / "streamstats.py")
        proc = subprocess.run(
            [str(PY), "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "test_project.py"],
            cwd=work,
            env={**os.environ, "QF_SEED": str(seed)},
            capture_output=True,
            text=True,
            check=False,
        )
        m = re.search(r"(\d+) tests? collected", proc.stdout + proc.stderr)
        counts[m.group(1) if m else "NO-MATCH rc=%d" % proc.returncode] += 1
    finally:
        shutil.rmtree(work, ignore_errors=True)
print("collected counts over seeds 0-49:", dict(counts))
print("pytest:", subprocess.run([str(PY), "-m", "pytest", "--version"], capture_output=True, text=True).stdout.strip() or "")
print("python:", subprocess.run([str(PY), "--version"], capture_output=True, text=True).stdout.strip())
