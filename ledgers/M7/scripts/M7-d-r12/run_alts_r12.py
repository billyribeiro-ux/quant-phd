"""Run each alternative solver through the M7 grader (test_project.py + instance.py) on seeds 0-49.

Usage: python -I -W error ledgers/M7/scripts/M7-d-r12/run_alts_r12.py <repo-root> [alt-file ...]
Each alternative is copied into a fresh scratch directory as constrained_allocator.py, with the same pytest flags the
browser uses. Prints PASS/FAIL per seed and the names of failing tests.
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
alts = [Path(a) for a in sys.argv[2:]] or sorted((root / "ledgers/M7/scripts/M7-d-r12/alts").glob("*.py"))
flags = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
for alt in alts:
    passed = 0
    failing: dict[int, list[str]] = {}
    for seed in range(50):
        work = Path(tempfile.mkdtemp(prefix="m7r12-"))
        shutil.copy(grader / "test_project.py", work / "test_project.py")
        shutil.copy(grader / "instance.py", work / "instance.py")
        shutil.copy(alt, work / "constrained_allocator.py")
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        res = subprocess.run(
            [sys.executable, "-m", "pytest", *flags, "test_project.py"],
            cwd=work, capture_output=True, text=True, check=False, env=env, timeout=600,
        )
        shutil.rmtree(work, ignore_errors=True)
        if res.returncode == 0:
            passed += 1
        else:
            names = re.findall(r"^FAILED test_project.py::(\S+)", res.stdout, re.M)
            failing[seed] = names[:5] or [res.stdout[-300:]]
    print(f"{alt.name}: seeds passing {passed}/50")
    for seed, names in list(failing.items())[:10]:
        print(f"   seed {seed}: {names}")
    sys.stdout.flush()
