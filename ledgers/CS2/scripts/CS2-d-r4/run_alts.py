"""Run candidate streamstats.py files against the CS2 suite on a range of seeds (verifier round 4).

Usage: python ledgers/CS2/scripts/CS2-d-r4/run_alts.py <seeds, e.g. 0-49> <candidate.py> [<candidate.py> ...]

Each candidate is copied into a fresh temporary workspace as streamstats.py, together with the grader's
test_project.py and instance.py, and the suite is run with the browser's flags for QF_SEED=<seed>. Prints one
line per candidate: the number of seeds it passes, and the first failing test names on the first failing seed.
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
GRADER = ROOT / "course" / "modules" / "CS" / "CS2" / "grader"
PYTHON = ROOT / ".venv" / "bin" / "python"


def parse(spec: str) -> list[int]:
    lo, _, hi = spec.partition("-")
    return list(range(int(lo), int(hi or lo) + 1))


def run(candidate: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="cs2r4_"))
    try:
        shutil.copy(GRADER / "test_project.py", work / "test_project.py")
        shutil.copy(GRADER / "instance.py", work / "instance.py")
        shutil.copy(candidate, work / "streamstats.py")
        env = {**os.environ, "QF_SEED": str(seed)}
        proc = subprocess.run(
            [str(PYTHON), "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work,
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        out = proc.stdout + proc.stderr
        return proc.returncode == 0, out
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    seeds = parse(sys.argv[1])
    for name in sys.argv[2:]:
        candidate = Path(name).resolve()
        passed = 0
        first_fail = ""
        for seed in seeds:
            ok, out = run(candidate, seed)
            if ok:
                passed += 1
            elif not first_fail:
                failed = re.findall(r"FAILED \S+::(\S+)", out)
                first_fail = f"seed {seed}: {failed[:4] if failed else out.strip().splitlines()[-1:]}"
        print(f"{candidate.name}: passes {passed}/{len(seeds)} seeds. {first_fail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
