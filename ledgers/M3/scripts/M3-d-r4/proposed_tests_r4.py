"""Round-4 verifier: proposed grader tests for the two surviving mutant classes, run in a scratch copy only.

Usage: .venv/bin/python -I ledgers/M3/scripts/M3-d-r4/proposed_tests_r4.py <candidate.py> [<candidate.py> ...]
Copies the suite into a scratch directory, appends the proposed tests to test_project.py there, and runs seeds 0-9.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
GRADER = ROOT / "course/modules/M/M3/grader"
EXTRA = '''

def test_clip_repair_rescales_a_positive_definite_matrix_whose_diagonal_is_not_one() -> None:
    m = [[1.0004, 0.3], [0.3, 1.0]]
    y = as_matrix(sol.clip_repair(m), 2)
    assert all(abs(y[i][i] - 1.0) <= 1e-9 for i in range(2)), "clip_repair must rescale its output to unit diagonal"
'''


def run(candidate: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="m3prop-"))
    shutil.copy(candidate, work / "covariance_doctor.py")
    shutil.copy(GRADER / "instance.py", work / "instance.py")
    (work / "test_project.py").write_text((GRADER / "test_project.py").read_text(encoding="utf-8") + EXTRA, encoding="utf-8")
    env = {"PATH": os.environ["PATH"], "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
    res = subprocess.run(
        [sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
        cwd=work, capture_output=True, text=True, env=env, timeout=300,
    )
    shutil.rmtree(work, ignore_errors=True)
    return res.returncode == 0, (res.stdout.strip().splitlines() or [""])[-1]


for arg in sys.argv[1:]:
    cand = Path(arg).resolve()
    fails = [s for s in range(10) if not run(cand, s)[0]]
    print(("PASS" if not fails else "FAIL"), cand.name, "failing seeds 0-9:", fails)
