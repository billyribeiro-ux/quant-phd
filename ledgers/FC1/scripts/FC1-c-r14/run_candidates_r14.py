"""Run candidate instruments.py files against the FC1 project suite on seeds 0-49 (round 14, FC1-c).

Usage: python -I ledgers/FC1/scripts/FC1-c-r14/run_candidates_r14.py <grader_dir> <seeds> <candidate.py> [...]
Each candidate is copied as instruments.py into a fresh scratch directory together with test_project.py and
instance.py, and pytest runs with the browser flags (--assert=plain -W error) once per seed (QF_SEED).
Prints one line per candidate: passing seeds, and the distinct failing test names with the first failing seed.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import OrderedDict
from pathlib import Path

PY = sys.executable
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def run_one(grader: Path, candidate: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="fc1c14-cand-"))
    try:
        shutil.copy(grader / "test_project.py", work / "test_project.py")
        shutil.copy(grader / "instance.py", work / "instance.py")
        shutil.copy(candidate, work / "instruments.py")
        env = dict(os.environ, QF_SEED=str(seed))
        proc = subprocess.run(
            [PY, "-m", "pytest", *FLAGS, "test_project.py"],
            cwd=work,
            env=env,
            capture_output=True,
            text=True,
            timeout=300,
        )
        out = proc.stdout + proc.stderr
        return proc.returncode == 0, out
    finally:
        shutil.rmtree(work, ignore_errors=True)


def parse_seeds(spec: str) -> list[int]:
    lo, _, hi = spec.partition("-")
    return list(range(int(lo), int(hi or lo) + 1))


def main() -> int:
    grader = Path(sys.argv[1]).resolve()
    seeds = parse_seeds(sys.argv[2])
    rc = 0
    for name in sys.argv[3:]:
        cand = Path(name).resolve()
        passed: list[int] = []
        failed: OrderedDict[str, int] = OrderedDict()
        for seed in seeds:
            ok, out = run_one(grader, cand, seed)
            if ok:
                passed.append(seed)
            else:
                names = re.findall(r"FAILED \S+::(\S+)", out) or ["<no FAILED line>: " + out.strip()[-300:]]
                for n in names:
                    failed.setdefault(n, seed)
        status = "ALL PASS" if len(passed) == len(seeds) else "FAILS"
        print(f"{cand.name}: {status} {len(passed)}/{len(seeds)} seeds")
        for n, s in failed.items():
            print(f"    failing: {n} (first seed {s})")
        if len(passed) != len(seeds):
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
