"""Round 14, FC1-c: does the proposed fix kill the two surviving round-14 mutants, and does the reference still pass?

Appends two probe tests to a scratch copy of grader/test_project.py (the repository file is not edited) and runs the
reference and the two survivors with QF_SEED=0. Usage: python -I ledgers/FC1/scripts/FC1-c-r14/probe_fix_r14.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/FC/FC1/grader"
MUT = ROOT / "ledgers/FC1/mutants"
PROBE = '''

def test_probe_sell_side_refusals() -> None:
    must_raise(lambda: sol.CashTrade(0, 9_850, -1, 2).events(), "quantity < 1, sell")
    must_raise(lambda: sol.CashTrade(10, -1, -1, 2).events(), "price_cents < 0, sell")
    must_raise(lambda: sol.CashTrade(10, 9_850, -1, 0).events(), "settlement_day < 1, sell")


def test_probe_zero_coupon_refusals() -> None:
    must_raise(lambda: sol.Bond(10_000, 0, 0).events(), "periods < 1, zero coupon")
    must_raise(lambda: sol.Bond(0, 0, 3).events(), "face_cents <= 0, zero coupon")
'''
CANDIDATES = {
    "reference.py": GRADER / "reference.py",
    "r14n01_sale_skips_quantity_and_settlement_checks.py": MUT / "r14n01_sale_skips_quantity_and_settlement_checks.py",
    "r14n05_bond_periods_and_face_checked_only_with_a_coupon.py": MUT / "r14n05_bond_periods_and_face_checked_only_with_a_coupon.py",
}
for name, path in CANDIDATES.items():
    work = Path(tempfile.mkdtemp(prefix="fc1c14-probe-"))
    try:
        shutil.copy(GRADER / "instance.py", work / "instance.py")
        (work / "test_project.py").write_text((GRADER / "test_project.py").read_text(encoding="utf-8") + PROBE, encoding="utf-8")
        shutil.copy(path, work / "instruments.py")
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work, env=dict(os.environ, QF_SEED="0"), capture_output=True, text=True, check=False,
        )
        failed = [line.split("::")[1].split(" ")[0] for line in proc.stdout.splitlines() if line.startswith("FAILED")]
        print(f"{name}: exit {proc.returncode}; failing probe/tests: {failed or 'none'}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
