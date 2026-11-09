"""Round 17 helper: builds a scratch workspace (outside the checkout) holding the suite's test_project.py and
instance.py and a candidate solver.py, and returns its path. Used by oracle_gap_precision.py and
mutant_v17_02_probe.py so that the grader's own oracle (test_project.oracle_gap) can be called."""
import os
import shutil
import sys
import tempfile
from pathlib import Path


def make_workspace(checkout: str, solver_path: str) -> Path:
    grader = Path(checkout) / "course/modules/E/E4/grader"
    work = Path(tempfile.mkdtemp(prefix="e4oracle-"))
    shutil.copy(grader / "test_project.py", work / "test_project.py")
    shutil.copy(grader / "instance.py", work / "instance.py")
    shutil.copy(solver_path, work / "solver.py")
    os.environ.setdefault("QF_SEED", "0")
    sys.path.insert(0, str(work))
    return work
