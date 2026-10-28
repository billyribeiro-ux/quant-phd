"""For each candidate file, collect the set of failing test names over seeds 0-49 (pytest, repo flags)."""

from __future__ import annotations

import collections
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

GRADER = Path("/tmp/quant-b2/course/modules/CS/CS2/grader")
PY = "/tmp/quant-b2/.venv/bin/python"
for arg in sys.argv[1:]:
    work = Path("/tmp/CS2-fix-names")
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    shutil.copy(arg, work / "streamstats.py")
    shutil.copy(GRADER / "instance.py", work)
    shutil.copy(GRADER / "test_project.py", work)
    names: collections.Counter[str] = collections.Counter()
    for seed in range(50):
        env = {**os.environ, "QF_SEED": str(seed)}
        out = subprocess.run(
            [PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work, env=env, capture_output=True, text=True,
        ).stdout
        for m in re.finditer(r"^FAILED test_project\.py::(\S+)", out, re.M):
            names[re.sub(r"\[.*", "", m.group(1))] += 1
    print(Path(arg).name, dict(names) if names else "no failures")
