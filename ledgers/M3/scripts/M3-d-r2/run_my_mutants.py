"""Run the M3 grader suite against each file given on the command line over seeds 0-9; prints PASS/FAIL strings."""
import shutil
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD2-M3-d")
sys.path.insert(0, str(ROOT / "tools"))

from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

import os
SEEDS = os.environ.get("SEEDS", "0-9")
u = unit("M3")
cfg = panel(u)
for arg in sys.argv[1:]:
    src = Path(arg)
    results = []
    for seed in parse_seeds(SEEDS):
        work = workspace(u, src, cfg)
        try:
            ok, output, _ = run_suite(work, cfg["suite"], seed)
        finally:
            shutil.rmtree(work, ignore_errors=True)
        results.append("P" if ok else "F")
    print(f"{src.name}: {''.join(results)}", flush=True)
