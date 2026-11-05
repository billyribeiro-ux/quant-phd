"""Run each round-12 alternative (and the reference) through the SC1 suite on seeds 0-49 in a fresh workspace."""
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

u = unit("SC1")
cfg = panel(u)
files = sorted((root / "ledgers/SC1/scripts/SC1-d-r12/alternatives").glob("alt_r12_*.py"))
files.append(root / "course/modules/SC/SC1/grader/reference.py")
for f in files:
    work = workspace(u, f, cfg)
    failures = []
    try:
        for seed in parse_seeds("0-49"):
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                failures.append(seed)
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)
    print(f"{f.name}: {'PASS' if not failures else 'FAIL'} on 0-49 ({50 - len(failures)}/50 seeds pass)" + (f" first failing seeds {failures[:5]}" if failures else ""))
