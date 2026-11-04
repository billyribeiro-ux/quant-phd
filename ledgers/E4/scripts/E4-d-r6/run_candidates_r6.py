"""Run candidate solvers (alternatives, mutants, reference) against the E4 project suite over a seed range.

Usage: python -I ledgers/E4/scripts/E4-d-r6/run_candidates_r6.py <checkout-root> <seeds-lo> <seeds-hi> <file> [<file> ...]
Each file is copied into a fresh workspace as solver.py beside the grader's suite and support files (the helpers of
tools/run_graders.py), and the suite is run once per seed with QF_SEED set to that seed.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tools"))
lo, hi = int(sys.argv[2]), int(sys.argv[3])
files = [Path(p).resolve() for p in sys.argv[4:]]

from coursekit import unit  # noqa: E402
from run_graders import panel, run_suite, workspace  # noqa: E402

u = unit("E4")
cfg = panel(u)
for f in files:
    work = workspace(u, f, cfg)
    failed: list[int] = []
    try:
        for seed in range(lo, hi + 1):
            ok, _output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                failed.append(seed)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    verdict = "PASS" if not failed else "FAIL"
    print(f"{f.name}: {verdict} ({hi - lo + 1 - len(failed)}/{hi - lo + 1} seeds pass; failing seeds: {failed[:10]})")
