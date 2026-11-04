"""Probe: does a hand-built log whose running totals are stale kill the replay that copies them? (round 1, slice c)

Appends one candidate test to a copy of the public grader suite and runs it against the reference solution and against
the survivor mutant v04. The appended test is not added to the grader (the verifier never edits course files); it shows
which test would kill the survivor. The reference must pass it and v04 must fail it.

Usage (from the checkout root): .venv/bin/python ledgers/PC3/scripts/PC3-c-r1/probe_stale_totals.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/PC/PC3/grader"
MUT = ROOT / "ledgers/PC3/mutants/v04_replay_copies_last_running_totals.py"

PROBE = '''

def test_probe_replay_sums_fills_when_running_totals_are_stale() -> None:
    """Probe: one fill at the ask (a sale), then running totals that say zero cash and zero inventory."""
    turns = [turn_record(1, filled=True, arrival="uninformed-buy", price=10_010, inventory=-1, cash=10_010)]
    turns += [turn_record(t, size=0, inventory=0, cash=0) for t in range(2, HORIZON + 1)]
    log = hand_log(turns, 10_000)
    expect(
        sol.replay(log) == oracle(log),
        "the cash flow must be the sum of the fill cash flows, and the inventory the sum of the fills",
    )
'''


def run(candidate: Path) -> str:
    work = Path(tempfile.mkdtemp(prefix="pc3c-probe-"))
    try:
        for name in ("engine.py", "instance.py"):
            shutil.copy(GRADER / name, work / name)
        (work / "test_project.py").write_text(
            (GRADER / "test_project.py").read_text(encoding="utf-8") + PROBE, encoding="utf-8"
        )
        shutil.copy(candidate, work / "market_maker.py")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
             "test_project.py", "-k", "probe"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": "0", "PYTHONHASHSEED": "0"},
            timeout=300,
        )
        return "PASS" if result.returncode == 0 else "FAIL"
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> None:
    print("reference:", run(GRADER / "reference.py"))
    print("v04 survivor:", run(MUT))


if __name__ == "__main__":
    main()
