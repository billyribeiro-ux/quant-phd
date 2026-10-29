"""Run the five verifier alternatives through the M7 suite on seeds 0-49 (over-constraint test).

Usage: .venv/bin/python ledgers/M7/scripts/M7-d-r1/run_alts.py <scratch-dir> <checkout-root>
Prints, per alternative, the seeds that failed and the first failing test name.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

scratch = Path(sys.argv[1])
root = Path(sys.argv[2])
py = str(root / ".venv/bin/python")
grader = root / "course/modules/M/M7/grader"
def run_one(ws: Path, seed: int) -> str | None:
    env = dict(os.environ, QF_SEED=str(seed))
    proc = subprocess.run(
        [py, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
        cwd=ws, env=env, capture_output=True, text=True, check=False,
    )
    if proc.returncode == 0:
        return None
    found = re.search(r"FAILED \S+::(\S+)", proc.stdout)
    return f"seed {seed}: {found.group(1) if found else proc.stdout[-200:]}"


for k in range(1, 6):
    ws = scratch / f"alt{k}"
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda seed: run_one(ws, seed), range(50)))
    failed = [r for r in results if r is not None]
    print(f"alt{k}: {50 - len(failed)}/50 seeds pass", flush=True)
    for line in failed[:5]:
        print("   ", line, flush=True)
