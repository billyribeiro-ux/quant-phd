"""Run each round-13 alternative (and the reference) through the SC1 suite on seeds 0-49 in a fresh workspace each."""

import shutil
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

u = unit("SC1")
cfg = panel(u)
files = sorted((root / "ledgers/SC1/scripts/SC1-d-r13/alternatives").glob("alt_r13_*.py"))
files.append(root / "course/modules/SC/SC1/grader/reference.py")
for f in files:
    work = workspace(u, f, cfg)
    failures = []
    try:
        for seed in parse_seeds("0-49"):
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                failures.append((seed, output.strip().splitlines()[-1] if output.strip() else ""))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"{f.name}: {'PASS' if not failures else 'FAIL'} on 0-49 ({50 - len(failures)}/50 seeds pass)")
    for seed, last in failures[:5]:
        print(f"    seed {seed}: {last}")
