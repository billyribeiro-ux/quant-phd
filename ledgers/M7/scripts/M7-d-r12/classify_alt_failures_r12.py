"""Classify every failing (alternative, seed, test) triple from alts_suite_r12.log by its failure kind.

Reads the per-alternative seed lists from the log, re-runs each failing test alone on its seed, and reports
'EXCEPTION <type>' (the solver raised) or 'ASSERT <message>' (the suite rejected a returned answer).
Usage: python -I -W error classify_alt_failures_r12.py <repo-root> <alts_suite_log> <alts-dir>
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
log = Path(sys.argv[2]).read_text(encoding="utf-8")
alts_dir = Path(sys.argv[3]).resolve()
grader = root / "course/modules/M/M7/grader"
current = None
jobs: list[tuple[str, int, str]] = []
for line in log.splitlines():
    m = re.match(r"^(alt_r12_\S+\.py): seeds passing", line)
    if m:
        current = m.group(1)
        continue
    m = re.match(r"^\s+seed (\d+): (\[.*\])$", line)
    if m and current:
        import ast

        for name in ast.literal_eval(m.group(2)):
            jobs.append((current, int(m.group(1)), name))
print(f"failing triples: {len(jobs)}")
for alt, seed, name in jobs:
    work = Path(tempfile.mkdtemp(prefix="m7r12-cls-"))
    shutil.copy(grader / "test_project.py", work / "test_project.py")
    shutil.copy(grader / "instance.py", work / "instance.py")
    shutil.copy(alts_dir / alt, work / "constrained_allocator.py")
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
    res = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "--tb=line",
         f"test_project.py::{name}"],
        cwd=work, capture_output=True, text=True, check=False, env=env, timeout=300,
    )
    shutil.rmtree(work, ignore_errors=True)
    kind = "EXCEPTION " + (re.search(r"(\w+Error): ([^\n]{0,70})", res.stdout) or ["", "?", "?"])[1] if "RuntimeError" in res.stdout or re.search(r"\w+Error:", res.stdout) and "AssertionError" not in res.stdout else ""
    if "AssertionError" in res.stdout:
        msg = re.search(r"AssertionError: ([^\n]{0,90})", res.stdout)
        kind = "ASSERT " + (msg.group(1) if msg else "?")
    if not kind:
        kind = "UNCLASSIFIED: " + res.stdout[-200:]
    print(f"{alt} seed {seed:2d} {name}: {kind}")
