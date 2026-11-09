"""Round 1 (M5 slice d, closing delta): run each accepted alternative and each not_accepted file through the
M5 project grader on seeds 0-49. Each candidate is copied into a fresh scratch workspace beside the grader's
test_project.py and instance.py as contraction_solver.py; pytest runs with QF_SEED set.

Usage: alt_seeds_r1.py <repo-root> <scratch-dir>   (run with the repo's .venv python, -I)
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(sys.argv[1])
SCRATCH = Path(sys.argv[2])
G = REPO / "course/modules/M/M5/grader"
ALT = REPO / "ledgers/M5/alternatives"
PY = REPO / ".venv/bin/python"
cands = sorted(ALT.glob("alt*.py")) + sorted((ALT / "not_accepted").glob("*.py"))
for cand in cands:
    passed = 0
    first_fail = None
    for seed in range(50):
        work = Path(tempfile.mkdtemp(prefix="m5d1_", dir=SCRATCH))
        try:
            shutil.copy(G / "test_project.py", work / "test_project.py")
            shutil.copy(G / "instance.py", work / "instance.py")
            shutil.copy(cand, work / "contraction_solver.py")
            env = {"QF_SEED": str(seed), "PATH": "/usr/bin:/bin"}
            r = subprocess.run(
                [
                    str(PY),
                    "-I",
                    "-m",
                    "pytest",
                    "-q",
                    "-p",
                    "no:cacheprovider",
                    "--assert=plain",
                    "-W",
                    "error",
                    "test_project.py",
                ],
                cwd=work,
                env=env,
                capture_output=True,
                text=True,
            )
            if r.returncode == 0:
                passed += 1
            elif first_fail is None:
                failed = [ln for ln in r.stdout.splitlines() if ln.startswith("FAILED")]
                first_fail = (seed, failed[:1])
        finally:
            shutil.rmtree(work, ignore_errors=True)
    print(f"{cand.relative_to(REPO)}: {passed}/50 seeds pass; first failure {first_fail}")
