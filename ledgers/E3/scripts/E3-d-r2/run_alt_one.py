"""Runs one alternative correct implementation (from ledgers/E3/scripts/run_alternatives.py) on the named seeds.

Usage: python3 run_alt_one.py <alt1..alt5> <first seed> <last seed>. Prints one line per seed: PASS or FAIL with the
first failing test name. The alternative is built from grader/reference.py; the suite is run unchanged.
"""

from __future__ import annotations

import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "E" / "E3" / "grader"
spec = importlib.util.spec_from_file_location("run_alternatives", ROOT / "ledgers" / "E3" / "scripts" / "run_alternatives.py")
assert spec is not None and spec.loader is not None
ra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ra)


def main() -> int:
    name, first, last = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    work = Path(tempfile.mkdtemp(prefix=f"e3-{name}-"))
    try:
        for f in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / f, work / f)
        (work / "elicit.py").write_text(ra.build(name), encoding="utf-8")
        for seed in range(first, last + 1):
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                 "test_project.py"],
                cwd=work, capture_output=True, text=True, check=False,
                env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            )
            if result.returncode == 0:
                print(f"{name} seed {seed} PASS", flush=True)
            else:
                found = re.search(r"FAILED \S+::(\S+)", result.stdout)
                print(f"{name} seed {seed} FAIL {found.group(1) if found else 'collection error'}", flush=True)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
