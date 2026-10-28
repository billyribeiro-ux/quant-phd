"""Run each alternative implementation through the AC4 autograder on seeds 0-9 and 25."""
import sys
from pathlib import Path
sys.path.insert(0, "/tmp/verify9-AC4-e/tools")
from coursekit import unit
from run_graders import panel, workspace, run_suite
u = unit("AC4")
cfg = panel(u)
for name in sys.argv[1:]:
    src = Path(name)
    results = []
    for seed in list(range(10)) + [25]:
        work = workspace(u, src, cfg)
        ok, out, _ = run_suite(work, cfg["suite"], seed)
        last = out.strip().splitlines()[-1] if out.strip() else ""
        results.append((seed, ok, last[-60:]))
    fails = [r for r in results if not r[1]]
    print(src.name, "PASS all" if not fails else f"FAIL {fails[:2]}", results[0][2])
