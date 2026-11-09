"""Run candidate clearing_house.py files against the BK4 grader on seeds (round 15 verifier).

Usage: python -I run_candidates.py <seeds e.g. 0-49> <candidate.py> [<candidate.py> ...]
Each candidate is copied to a fresh scratch workspace as clearing_house.py beside the grader's
test_project.py and instance.py (copied unchanged from the pin), run under the browser's pytest flags
with QF_SEED set. Prints one line per candidate: pass/fail counts and the first failing test names.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PIN = Path("/Users/billyribeiro/.fanout/wt/verifyE15-BK4-c")
GRADER = PIN / "course/modules/BK/BK4/grader"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def seeds_of(text: str) -> list[int]:
    lo, _, hi = text.partition("-")
    return list(range(int(lo), int(hi or lo) + 1))


def run_one(candidate: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="bk4c-r15-"))
    for name in ("test_project.py", "instance.py"):
        shutil.copy(GRADER / name, work / name)
    shutil.copy(candidate, work / "clearing_house.py")
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
    result = subprocess.run(
        [sys.executable, "-I", "-m", "pytest", *FLAGS, "test_project.py"],
        cwd=work, capture_output=True, text=True, check=False, env=env, timeout=300,
    )
    shutil.rmtree(work, ignore_errors=True)
    failed = re.findall(r"^FAILED test_project.py::(\w+)", result.stdout, flags=re.M)
    summary = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else result.stderr[-300:]
    return result.returncode == 0, (failed[0] if failed else summary)


def main() -> None:
    seeds = seeds_of(sys.argv[1])
    for raw in sys.argv[2:]:
        candidate = Path(raw).resolve()
        passes, fails = 0, []
        for seed in seeds:
            ok, detail = run_one(candidate, seed)
            if ok:
                passes += 1
            else:
                fails.append(f"seed {seed}: {detail}")
        print(f"{candidate.name}: {passes}/{len(seeds)} seeds pass")
        for line in fails[:5]:
            print("   ", line)


if __name__ == "__main__":
    main()
