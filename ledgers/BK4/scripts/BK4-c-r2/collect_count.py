"""Collect-only count of the BK4 suite on the reference, and on the starter (verifier BK4-c, round 2).

Usage (from the checkout root): .venv/bin/python ledgers/BK4/scripts/BK4-c-r2/collect_count.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))

from coursekit import unit  # noqa: E402
from run_graders import panel, workspace  # noqa: E402

u = unit("BK4")
cfg = panel(u)
for label, src in (("reference", u.directory / "grader/reference.py"), ("starter", u.directory / "grader/starter.py")):
    work = workspace(u, src, cfg)
    res = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
         "--collect-only", cfg["suite"]],
        cwd=work, capture_output=True, text=True, env={"QF_SEED": "0", "PATH": "/usr/bin:/bin"}, check=False,
    )
    tail = [ln for ln in res.stdout.splitlines() if "collected" in ln or "tests collected" in ln or "test" in ln][-2:]
    print(label, "exit", res.returncode, tail)
    n = sum(1 for ln in res.stdout.splitlines() if "::test_" in ln)
    print(label, "test ids listed:", n)
    print(res.stdout.strip().splitlines()[-1])
