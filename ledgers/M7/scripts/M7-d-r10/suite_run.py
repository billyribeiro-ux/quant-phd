"""Run the M7 project suite against one solution file over a list of seeds (verifier helper, round 10).

Usage: python -I ledgers/M7/scripts/M7-d-r10/suite_run.py <solution.py> <seeds e.g. 0-49> [collect]

Each seed runs in a fresh temporary workspace holding test_project.py, instance.py and the solution copied as
constrained_allocator.py, with the browser's pytest flags and QF_SEED set. With 'collect' the script only reports the
collected test count per seed. Prints one line per seed and a summary. The grader files are read from the checkout.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "M" / "M7" / "grader"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def seeds_of(text: str) -> list[int]:
    out: list[int] = []
    for chunk in text.split(","):
        lo, _, hi = chunk.partition("-")
        out.extend(range(int(lo), int(hi or lo) + 1))
    return out


def workspace(solution: Path) -> Path:
    work = Path(tempfile.mkdtemp(prefix="m7d-r10-"))
    shutil.copy(GRADER / "test_project.py", work / "test_project.py")
    shutil.copy(GRADER / "instance.py", work / "instance.py")
    shutil.copy(solution, work / "constrained_allocator.py")
    return work


def main() -> int:
    solution = Path(sys.argv[1]).resolve()
    seeds = seeds_of(sys.argv[2])
    collect = len(sys.argv) > 3 and sys.argv[3] == "collect"
    failures = 0
    counts: set[str] = set()
    for seed in seeds:
        work = workspace(solution)
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        try:
            if collect:
                cmd = [sys.executable, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "test_project.py"]
            else:
                cmd = [sys.executable, "-m", "pytest", *FLAGS, "test_project.py"]
            result = subprocess.run(cmd, cwd=work, capture_output=True, text=True, check=False, env=env, timeout=300)
            text = result.stdout + result.stderr
            if collect:
                match = re.search(r"(\d+) tests? collected", text) or re.search(r"(\d+) tests? collected", text)
                count = match.group(1) if match else f"? rc={result.returncode}"
                counts.add(count)
                print(f"seed {seed}: collected {count}")
            else:
                ok = result.returncode == 0
                failures += not ok
                summary = re.findall(r"^FAILED (\S+)", text, flags=re.M)
                tail = text.strip().splitlines()[-1] if text.strip() else ""
                print(f"seed {seed}: {'PASS' if ok else 'FAIL'} | {tail} | first_failed={summary[:3]}")
        finally:
            shutil.rmtree(work, ignore_errors=True)
    if collect:
        print(f"distinct collected counts: {sorted(counts)}")
    else:
        print(f"total seeds {len(seeds)} failing {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
