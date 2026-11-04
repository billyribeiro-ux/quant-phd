"""Run the M4 project grader suite on one solution file for a list of seeds.

Usage: python -I ledgers/M4/scripts/M4-d-r8/checks/grade_one.py <solution.py> <seeds e.g. 0-9> [--count]
Uses the same workspace and pytest flags as tools/run_graders.py. Prints, per seed, the pytest summary line.
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("M4_ROOT", "/Users/billyribeiro/.fanout/wt/verifyD8-M4-d")).resolve()
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import PYTEST_FLAGS, panel, parse_seeds, workspace  # noqa: E402


def main() -> int:
    solution = Path(sys.argv[1]).resolve()
    seeds = parse_seeds(sys.argv[2])
    count_only = "--count" in sys.argv
    u = unit("M4")
    cfg = panel(u)
    work = workspace(u, solution, cfg)
    rc = 0
    try:
        for seed in seeds:
            flags = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
            if count_only:
                flags = ["-p", "no:cacheprovider", "--collect-only", "-q", "-W", "error"]
            result = subprocess.run(
                [sys.executable, "-m", "pytest", *flags, cfg["suite"]],
                cwd=work,
                capture_output=True,
                text=True,
                check=False,
                env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
                timeout=300,
            )
            out = result.stdout + result.stderr
            summary = [line for line in out.splitlines() if re.search(r"(passed|failed|error|collected|tests? )", line)]
            tail = summary[-1] if summary else out[-300:]
            failed = re.findall(r"FAILED \S+", out)
            print(f"seed {seed} rc {result.returncode}: {tail.strip()} {failed[:3]}")
            if result.returncode != 0:
                rc = 1
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
