# ruff: noqa (verifier scratch code: style is not gated; see the fragment)
"""Run the AC2 project suite (the course's test_project.py and instance.py, unchanged) on candidate solutions.

Usage (from the repository root):
    .venv/bin/python ledgers/AC2/scripts/project-r1/run_candidates.py SEEDS CANDIDATE [CANDIDATE ...]

Each CANDIDATE is a path to a fundamentals.py module. The module is copied to a fresh workspace as
atlas/fundamentals.py, next to the unchanged grader files, and the suite runs under the browser's flags
(-q --assert=plain -W error) for each seed. Prints one line per (candidate, seed) with the pass count and the
names of failing tests. Nothing is written outside the scratch workspaces, which are removed afterwards.
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
GRADER = ROOT / "course" / "modules" / "AC" / "AC2" / "grader"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def parse_seeds(text: str) -> list[int]:
    out: list[int] = []
    for chunk in text.split(","):
        lo, _, hi = chunk.partition("-")
        out.extend(range(int(lo), int(hi or lo) + 1))
    return out


def run(candidate: Path, seed: int) -> tuple[int, int, list[str], str]:
    work = Path(tempfile.mkdtemp(prefix="ac2-cand-"))
    try:
        shutil.copy(GRADER / "test_project.py", work / "test_project.py")
        shutil.copy(GRADER / "instance.py", work / "instance.py")
        (work / "atlas").mkdir()
        (work / "atlas" / "__init__.py").write_text("", encoding="utf-8")
        shutil.copy(candidate, work / "atlas" / "fundamentals.py")
        result = subprocess.run(
            [sys.executable, "-I", "-m", "pytest", *FLAGS, "test_project.py"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            timeout=300,
        )
        tail = result.stdout[-1500:] + result.stderr[-500:]
        failed = sorted(set(re.findall(r"FAILED \S+::(\S+)", result.stdout)))
        summary = re.search(r"(\d+) failed", result.stdout)
        passed = re.search(r"(\d+) passed", result.stdout)
        n_failed = int(summary.group(1)) if summary else 0
        n_passed = int(passed.group(1)) if passed else 0
        if result.returncode not in (0, 1) or (n_passed + n_failed) == 0:
            return -1, -1, [], tail
        return n_passed, n_failed, failed, ""
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    seeds = parse_seeds(sys.argv[1])
    worst = 0
    for raw in sys.argv[2:]:
        candidate = Path(raw).resolve()
        for seed in seeds:
            passed, failed, names, tail = run(candidate, seed)
            if passed < 0:
                print(f"{candidate.parent.parent.name} seed {seed}: SUITE DID NOT RUN\n{tail}")
                worst = 1
                continue
            label = "PASS" if failed == 0 else "FAIL"
            print(f"{candidate.parent.parent.name} seed {seed}: {label} passed={passed} failed={failed} {names[:12]}")
            worst = max(worst, 1 if failed else 0)
    return worst


if __name__ == "__main__":
    sys.exit(main())
