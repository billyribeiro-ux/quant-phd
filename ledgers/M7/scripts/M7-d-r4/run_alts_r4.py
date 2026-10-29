"""Run every alternative solver through the current M7 suite on seeds 0-49 (over-constraint check).

Usage: python3 run_alts_r4.py <alts-root> <checkout-root>
<alts-root> holds one directory per alternative, each with constrained_allocator.py.
The suite and instance come from <checkout-root>/course/modules/M/M7/grader.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

alts_root = Path(sys.argv[1])
grader = Path(sys.argv[2]) / "course/modules/M/M7/grader"
py = str(Path(sys.argv[2]) / ".venv/bin/python")


def run_one(work: Path, seed: int) -> str | None:
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
    try:
        proc = subprocess.run(
            [py, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work, env=env, capture_output=True, text=True, check=False, timeout=120,
        )
    except subprocess.TimeoutExpired:
        return f"seed {seed}: TIMEOUT after 120 s"
    if proc.returncode == 0:
        return None
    found = re.search(r"FAILED \S+::(\S+)", proc.stdout)
    return f"seed {seed}: {found.group(1) if found else proc.stdout[-160:]}"


for alt in sorted(p for p in alts_root.iterdir() if (p / "constrained_allocator.py").exists()):
    work = Path(tempfile.mkdtemp(prefix=f"alt-{alt.name}-"))
    shutil.copy(grader / "test_project.py", work)
    shutil.copy(grader / "instance.py", work)
    shutil.copy(alt / "constrained_allocator.py", work)
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda seed: run_one(work, seed), range(50)))
    failed = [r for r in results if r is not None]
    print(f"{alt.name}: {50 - len(failed)}/50 seeds pass", flush=True)
    for line in failed[:3]:
        print("   ", line, flush=True)
    shutil.rmtree(work, ignore_errors=True)
