"""Runs the grader suite on the given mutant files for seeds 0-9 (same workspace and flags as tools/mutate_graders.py)."""
import sys, pathlib
ROOT = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "tools"))
from pathlib import Path
from coursekit import unit
from run_graders import panel, workspace, run_suite

u = unit("E3")
cfg = panel(u)
for m in sys.argv[2:]:
    mutant = Path(m).resolve()
    killed_by = None
    for seed in range(10):
        work = workspace(u, mutant, cfg)
        ok, out, secs = run_suite(work, cfg["suite"], seed)
        if not ok:
            killed_by = (seed, [l for l in out.splitlines() if "FAILED" in l or "Failed" in l][:2] or out.strip().splitlines()[-1:])
            break
    print(mutant.name, "KILLED on seed %s: %s" % (killed_by[0], killed_by[1]) if killed_by else "SURVIVED seeds 0-9", flush=True)
