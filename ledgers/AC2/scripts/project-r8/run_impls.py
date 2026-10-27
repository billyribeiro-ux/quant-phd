"""Run alternative correct implementations (and new mutants) through the AC2 grader panel, seeds 0-49."""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

u = unit("AC2")
cfg = panel(u)
seeds = parse_seeds("0-49")
for path in sys.argv[2:]:
    p = Path(path)
    work = workspace(u, p, cfg)
    failed = None
    try:
        for s in seeds:
            ok, output, _ = run_suite(work, cfg["suite"], s)
            if not ok:
                failed = s
                break
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)
    print(f"{'PASS' if failed is None else 'FAIL'} {p.name} seeds=50 first_fail_seed={failed}")
