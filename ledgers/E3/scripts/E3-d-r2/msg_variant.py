"""Builds a correct engine whose ValueError messages avoid the page's wording (the condition named in other words)
for the conditions the exception table does not quote, then runs the suite on seeds 0 to 2.

Usage: python3 msg_variant.py  (writes into a temporary directory; prints the pytest tail per seed)
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "E" / "E3" / "grader"
REPLACEMENTS = {
    'raise ValueError("need at least one response, and mixed-sign lotteries, to identify loss aversion")': 'raise ValueError("no answers given")',
    'raise ValueError("need mixed-sign lotteries to identify loss aversion")': 'raise ValueError("no lottery pays both a gain and a loss")',
}


def main() -> int:
    source = (GRADER / "reference.py").read_text(encoding="utf-8")
    for old, new in REPLACEMENTS.items():
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    work = Path(tempfile.mkdtemp(prefix="e3-msgvar-"))
    try:
        for f in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / f, work / f)
        (work / "elicit.py").write_text(source, encoding="utf-8")
        for seed in (0, 1, 2):
            r = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                 "test_project.py"],
                cwd=work, capture_output=True, text=True, check=False,
                env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            )
            print(f"seed {seed}: rc {r.returncode}; {r.stdout.strip().splitlines()[-1]}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
