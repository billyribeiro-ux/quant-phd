"""Proposed extra test (not applied to the repository): exact integer shares above 2**53 (BK4-c r1 evidence).

Writes a scratch copy of test_project.py with one added test, then runs it against the reference and the float mutant.
Run: .venv/bin/python ledgers/BK4/scripts/BK4-c-r1/probe_large_cents_test.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "BK" / "BK4" / "grader"
MUTANT = ROOT / "ledgers" / "BK4" / "mutants" / "vc10_float_arithmetic.py"

EXTRA = '''

def test_large_cent_shares_are_floored_in_integers() -> None:
    """Survivor shares are exact integer floors even above 2**53 cents, with the leftover cent to the first survivor."""
    result = sol.waterfall(6_585_696_953_829_388, 3, {1: 0, 2: 0, 3: 0}, {1: 6_692_931_089_932_558, 2: 585_467_024_498_971, 3: 0}, 0)
    check_waterfall(result, (0, 0, 0, {1: 6_055_950_114_045_320, 2: 529_746_839_784_068}, 0), "large cents")
'''


def run(candidate: Path, label: str) -> None:
    work = Path(tempfile.mkdtemp(prefix="bk4c-probe-"))
    try:
        test_text = (GRADER / "test_project.py").read_text(encoding="utf-8") + EXTRA
        (work / "test_project.py").write_text(test_text, encoding="utf-8")
        shutil.copy(GRADER / "instance.py", work / "instance.py")
        shutil.copy(candidate, work / "clearing_house.py")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": "0", "PYTHONHASHSEED": "0"},
        )
        print(f"{label}: exit {result.returncode}; last line: {result.stdout.strip().splitlines()[-1]}")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    run(GRADER / "reference.py", "reference")
    run(MUTANT, "vc10_float_arithmetic")
