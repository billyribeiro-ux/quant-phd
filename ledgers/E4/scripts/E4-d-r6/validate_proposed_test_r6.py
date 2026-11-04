"""Validate the proposed unit-fraction test (with a positive cost) against the reference, the five alternatives, the
damped fixed-point candidate, and the two survivors. Usage: python -I validate_proposed_test_r6.py <checkout-root>.
The proposed test text is read from proposed_unit_fraction_positive_cost_test.txt in this folder; no course file is edited.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
here = Path(__file__).resolve().parent
grader = root / "course/modules/E/E4/grader"
text = (here / "proposed_unit_fraction_positive_cost_test.txt").read_text(encoding="utf-8")
body = text[text.index("def test_unit_fraction_is_reported_with_a_positive_cost"):]
candidates = [
    grader / "reference.py",
    root / "ledgers/E4/alternatives/alt_1.py",
    root / "ledgers/E4/alternatives/alt_2.py",
    root / "ledgers/E4/alternatives/alt_3.py",
    root / "ledgers/E4/alternatives/alt_4.py",
    root / "ledgers/E4/alternatives/alt_5.py",
    here / "candidates/damped_fixed_point_log_r6.py",
    root / "ledgers/E4/mutants/mutant_r6_06_cost_scales_whole_gap.py",
    root / "ledgers/E4/mutants/mutant_r6_07_unit_informativeness_discounted_by_cost.py",
]
for cand in candidates:
    work = Path(tempfile.mkdtemp(prefix="e4r6-prop-"))
    try:
        shutil.copy(grader / "instance.py", work / "instance.py")
        shutil.copy(grader / "test_project.py", work / "test_project.py")
        with (work / "test_project.py").open("a", encoding="utf-8") as fh:
            fh.write("\n\n" + body)
        shutil.copy(cand, work / "solver.py")
        marks = []
        for seed in range(10):
            env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
            res = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                 "test_project.py", "-k", "positive_cost"],
                cwd=work, env=env, capture_output=True, text=True, check=False,
            )
            marks.append("P" if res.returncode == 0 else "F")
        print(f"{cand.relative_to(root) if cand.is_relative_to(root) else cand.name}: {' '.join(marks)}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
