"""Run each alternative and the not_accepted files through the M5 suite on seeds 0-49 (round 4, slice d).

Each candidate is copied into a fresh scratch workspace under /tmp as contraction_solver.py, next to the
grader's test_project.py and instance.py, and pytest is run with QF_SEED set, as in the page's local command.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(sys.argv[1])
G = REPO / "course/modules/M/M5/grader"
ALT = REPO / "ledgers/M5/alternatives"
PY = REPO / ".venv/bin/python"
cands = sorted(ALT.glob("*.py")) + sorted((ALT / "not_accepted").glob("*.py"))
for cand in cands:
    passed = 0
    first_fail = None
    for seed in range(50):
        work = Path(tempfile.mkdtemp(prefix="m5alt_", dir="/tmp/m5d5/tmp"))
        try:
            shutil.copy(G / "test_project.py", work / "test_project.py")
            shutil.copy(G / "instance.py", work / "instance.py")
            shutil.copy(cand, work / "contraction_solver.py")
            env = {"QF_SEED": str(seed), "PATH": "/usr/bin:/bin"}
            r = subprocess.run(
                [str(PY), "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                cwd=work, env=env, capture_output=True, text=True,
            )
            if r.returncode == 0:
                passed += 1
            elif first_fail is None:
                last = [ln for ln in r.stdout.splitlines() if ln.startswith("FAILED")]
                first_fail = (seed, last[:1])
        finally:
            shutil.rmtree(work, ignore_errors=True)
    print(f"{cand.relative_to(REPO)}: {passed}/50 seeds pass; first failure {first_fail}")
