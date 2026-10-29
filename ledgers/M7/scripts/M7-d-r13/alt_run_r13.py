"""Round 13 (M7-d): runs alternative correct implementations through the M7 suite, seeds 0-49, with the same workspace
and pytest flags as tools/run_graders.py. Usage: alt_run_r13.py <solution.py> [<solution.py> ...]"""
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyB13-M7-d")
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, run_suite, workspace  # noqa: E402

u = unit("M7")
cfg = panel(u)
failures = 0
for arg in sys.argv[1:]:
    src = Path(arg).resolve()
    work = workspace(u, src, cfg)
    rows = []
    try:
        for seed in range(50):
            ok, out, _ = run_suite(work, cfg["suite"], seed)
            rows.append(ok)
            if not ok:
                failures += 1
                print(f"{src.name} seed {seed}: FAILED")
                print(out[-600:])
                break
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)
    print(f"{src.name}: {sum(rows)}/50 seeds pass")
sys.exit(1 if failures else 0)
