"""Run alternative correct M7 solvers through the suite on seeds 0-49 (over-constraint test, round 3).

Usage: .venv/bin/python run_alts_r3.py <checkout-root> <scratch-dir>
Each alternative is installed as constrained_allocator.py with the grader files; alt_core.py routes 1-5 are appended
as allocate = allocate_altK so the file stays standard-library only and self-contained.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
py = str(root / ".venv/bin/python")
grader = root / "course/modules/M/M7/grader"
alts = root / "ledgers/M7/scripts"
sources: dict[str, str] = {}
for k in range(1, 6):
    reference = (root / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
    text = (alts / "M7-d-r1/alt_core.py").read_text(encoding="utf-8")
    sources[f"core_route{k}"] = reference + "\n\n" + text + f"\n\nallocate = allocate_alt{k}\n"
sources["bland"] = (alts / "M7-d-r2/alt_bland.py").read_text(encoding="utf-8")
sources["exact_order"] = (alts / "M7-d-r2/alt_exact.py").read_text(encoding="utf-8")
sources["first_order"] = (alts / "M7-d-r2/alt_first.py").read_text(encoding="utf-8")
sources["float_arithmetic"] = (alts / "M7-d-r3/alternatives/alt_float_r3.py").read_text(encoding="utf-8")


def run_one(ws: Path, seed: int) -> str | None:
    env = dict(os.environ, QF_SEED=str(seed))
    proc = subprocess.run(
        [py, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
        cwd=ws, env=env, capture_output=True, text=True, check=False,
    )
    if proc.returncode == 0:
        return None
    found = re.search(r"FAILED \S+::(\S+)", proc.stdout)
    return f"seed {seed}: {found.group(1) if found else proc.stdout[-300:]}"


for name, source in sources.items():
    ws = scratch / name
    shutil.rmtree(ws, ignore_errors=True)
    ws.mkdir(parents=True)
    shutil.copy(grader / "test_project.py", ws / "test_project.py")
    shutil.copy(grader / "instance.py", ws / "instance.py")
    (ws / "constrained_allocator.py").write_text(source, encoding="utf-8")
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(lambda seed: run_one(ws, seed), range(50)))
    failed = [r for r in results if r is not None]
    print(f"{name}: {50 - len(failed)}/50 seeds pass", flush=True)
    for line in failed[:4]:
        print("   ", line, flush=True)
