#!/usr/bin/env python3
"""Run the M2 project suite against several implementation files, seed by seed, under the browser's pytest flags.

Mirrors tools/run_graders.py (workspace and run_suite) without importing it. Usage:

    python3 impl_runs.py --seeds 0-49 IMPL.py [IMPL.py ...]

Prints one line per implementation: passed seeds out of the total, and the first failing test name for a failure.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GRADER = Path("/tmp/quant-b2/course/modules/M/M2/grader")
PYTEST_FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def parse_seeds(text: str) -> list[int]:
    seeds: list[int] = []
    for chunk in text.split(","):
        lo, _, hi = chunk.partition("-")
        seeds.extend(range(int(lo), int(hi or lo) + 1))
    return seeds


def workspace(solution: Path) -> Path:
    work = Path(tempfile.mkdtemp(prefix="m2fix-"))
    for name in ("test_project.py", "instance.py"):
        shutil.copy(GRADER / name, work / name)
    shutil.copy(solution, work / "sensitivity_engine.py")
    return work


def run(work: Path, seed: int) -> tuple[bool, str]:
    result = subprocess.run(
        ["/tmp/quant-b2/.venv/bin/python", "-m", "pytest", *PYTEST_FLAGS, "test_project.py"],
        cwd=work,
        capture_output=True,
        text=True,
        check=False,
        env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
        timeout=300,
    )
    output = result.stdout[-2000:] + result.stderr[-2000:]
    return result.returncode == 0, output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="0-49")
    parser.add_argument("impls", nargs="+", type=Path)
    args = parser.parse_args()
    seeds = parse_seeds(args.seeds)
    for impl in args.impls:
        work = workspace(impl)
        passed = 0
        first_failure = ""
        try:
            for seed in seeds:
                ok, output = run(work, seed)
                if ok:
                    passed += 1
                elif not first_failure:
                    found = re.findall(r"FAILED \S+::(\S+)", output)
                    first_failure = f"seed {seed}: {found[0] if found else 'collection or import error'}"
        finally:
            shutil.rmtree(work, ignore_errors=True)
        verdict = "PASS" if passed == len(seeds) else "FAIL"
        print(f"{verdict} {impl.name}: {passed}/{len(seeds)} seeds {first_failure}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
