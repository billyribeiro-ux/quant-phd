"""Verifier round 2: do the grader's tests enforce the spec's 'no printing or warning' and 'standard library only'?

Builds two solutions from the reference: one that prints inside allocate, and one that imports a non-standard module
(numpy, only if installed; otherwise the import itself fails and the row is moot). Runs the suite on seed 0 for each.
Usage (repository root): .venv/bin/python -I ledgers/E2/scripts/E2-d-r2/constraint_survivors_r2.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/E/E2/grader"
REF = (GRADER / "reference.py").read_text(encoding="utf-8")


def run(solution_text: str, label: str) -> None:
    work = Path(tempfile.mkdtemp(prefix="e2-r2-print-"))
    try:
        for name in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / name, work / name)
        (work / "auction_sim.py").write_text(solution_text, encoding="utf-8")
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": "0", "PYTHONHASHSEED": "0"}
        r = subprocess.run([sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain",
                            "-W", "error", "test_project.py"], cwd=work, capture_output=True, text=True, env=env,
                           check=False)
        print(f"{label}: exit {r.returncode} | {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ''}")
    finally:
        shutil.rmtree(work, ignore_errors=True)


printing = REF.replace(
    "    winners = set(_ranking(bids)[:units])\n    return [i in winners for i in range(len(bids))]\n",
    "    winners = set(_ranking(bids)[:units])\n    print('allocate called')\n    return [i in winners for i in range(len(bids))]\n",
    1,
)
assert printing != REF
run(printing, "print-in-allocate (spec: no printing in the module)")
importing = REF.replace("import math\n", "import math\nimport numpy  # noqa: F401\n", 1)
assert importing != REF
run(importing, "numpy-import (spec: standard library only)")
