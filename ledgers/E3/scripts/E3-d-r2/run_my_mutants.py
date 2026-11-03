"""Run named mutants (ledgers/E3/mutants/<name>) against the E3 grader with the mutate_graders.py flags.

Usage: python3 run_my_mutants.py <seeds> <mutant file name>...
A mutant is KILLED when some seed in the window fails the suite; otherwise SURVIVED.
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
GRADER = ROOT / "course" / "modules" / "E" / "E3" / "grader"
PY = ROOT / ".venv" / "bin" / "python"


def seeds_of(text: str) -> list[int]:
    out: list[int] = []
    for chunk in text.split(","):
        lo, _, hi = chunk.partition("-")
        out.extend(range(int(lo), int(hi or lo) + 1))
    return out


seeds = seeds_of(sys.argv[1])
for name in sys.argv[2:]:
    mutant = ROOT / "ledgers" / "E3" / "mutants" / name
    work = Path(tempfile.mkdtemp(prefix="e3m-"))
    killed = None
    try:
        for f in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / f, work / f)
        shutil.copy(mutant, work / "elicit.py")
        for seed in seeds:
            res = subprocess.run(
                [str(PY), "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                 "test_project.py"],
                cwd=work, capture_output=True, text=True, check=False,
                env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            )
            if res.returncode != 0:
                found = re.search(r"FAILED \S+::(\S+)", res.stdout)
                killed = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                break
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"{'KILLED' if killed else 'SURVIVED'} {name}: {killed}", flush=True)
