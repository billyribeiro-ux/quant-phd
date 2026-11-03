"""Run each alternative solver through the whole suite on seeds 0-49 (over-constraint test).

usage: run_alts_r3v.py <checkout-root> <out-dir> <alt-file> [<alt-file> ...]
Each alternative is copied in as constrained_allocator.py beside the unmodified grader files; the suite runs with the
browser flags, one pytest process per seed, four processes at a time. Writes <out-dir>/<name>_0-49.log.
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
out = Path(sys.argv[2])
grader = root / "course/modules/M/M7/grader"
py = root / ".venv/bin/python"
out.mkdir(parents=True, exist_ok=True)
for alt in map(Path, sys.argv[3:]):
    name = alt.stem
    ws = Path(f"/tmp/m7d-r3-run-{name}")
    shutil.rmtree(ws, ignore_errors=True)
    ws.mkdir(parents=True)
    shutil.copy(grader / "test_project.py", ws / "test_project.py")
    shutil.copy(grader / "instance.py", ws / "instance.py")
    shutil.copy(alt, ws / "constrained_allocator.py")

    def run(seed: int) -> str:
        env = dict(os.environ, QF_SEED=str(seed))
        try:
            proc = subprocess.run(
                [str(py), "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                 "test_project.py"],
                cwd=ws, env=env, capture_output=True, text=True, check=False, timeout=float(os.environ.get("SEED_TIMEOUT", "240")))
        except subprocess.TimeoutExpired:
            return f"seed {seed}: TIMEOUT (no finish within the per-seed limit)"
        tail = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else proc.stderr[-200:]
        first = re.findall(r"FAILED \S+::(\S+)", proc.stdout)
        status = "PASS" if proc.returncode == 0 else "FAIL"
        return f"seed {seed}: {status} | {tail} | {first[:3]}"

    with ThreadPoolExecutor(max_workers=4) as pool:
        lines = list(pool.map(run, range(50)))
    passed = sum(1 for line in lines if ": PASS" in line)
    (out / f"{name}_0-49.log").write_text("\n".join(lines) + f"\n{name}: {passed}/50 seeds pass\n", encoding="utf-8")
    print(f"{name}: {passed}/50 seeds pass", flush=True)
