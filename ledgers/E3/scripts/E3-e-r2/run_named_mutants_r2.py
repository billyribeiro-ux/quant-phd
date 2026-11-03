"""Run named mutant files against the E3 grader suite, seed by seed (verifier E3-e round 2).

Usage: python -I run_named_mutants_r2.py SEEDS MUTANT_PATH [MUTANT_PATH ...]
A mutant is KILLED when some seed in the window fails the suite; otherwise SURVIVED. The checkout's grader files
(test_project.py, instance.py) are copied into a scratch directory with the mutant as elicit.py.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD2-E3-e")
GRADER = ROOT / "course/modules/E/E3/grader"
PY = ROOT / ".venv/bin/python"


def seeds_of(text: str) -> list[int]:
    out: list[int] = []
    for chunk in text.split(","):
        lo, _, hi = chunk.partition("-")
        out.extend(range(int(lo), int(hi or lo) + 1))
    return out


seeds = seeds_of(sys.argv[1])
for raw in sys.argv[2:]:
    mutant = Path(raw)
    work = Path(tempfile.mkdtemp(prefix="e3m-"))
    killed = None
    try:
        for f in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / f, work / f)
        shutil.copy(mutant, work / "elicit.py")
        for seed in seeds:
            res = subprocess.run(
                [str(PY), "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                cwd=work,
                capture_output=True,
                text=True,
                check=False,
                env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
            )
            if res.returncode != 0:
                found = re.search(r"FAILED \S+::(\S+)", res.stdout)
                killed = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                break
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"{'KILLED' if killed else 'SURVIVED'} {mutant.name}: {killed}", flush=True)
