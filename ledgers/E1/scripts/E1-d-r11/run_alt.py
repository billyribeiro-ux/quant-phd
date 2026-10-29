import sys
from pathlib import Path
sys.path.insert(0, "tools")
from coursekit import unit
from run_graders import panel, workspace, run_suite, parse_seeds
u = unit("E1")
cfg = panel(u)
for src in sys.argv[1:]:
    results = []
    for seed in parse_seeds("0-9"):
        work = workspace(u, Path(src), cfg)
        try:
            ok, out, _ = run_suite(work, cfg["suite"], seed)
        finally:
            import shutil; shutil.rmtree(work, ignore_errors=True)
        results.append((seed, ok))
        if not ok:
            print(src, "FAILED seed", seed, out[-600:]); break
    print(src, "PASS all seeds" if all(ok for _, ok in results) else "FAIL", len(results))
