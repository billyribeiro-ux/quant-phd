"""Run the CF1 suite on the round-18 mutants (seeds 0-9) and on the alternative engines (seeds 0-49).

Usage: run_new.py <checkout> mutants|alts <file>...
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, run_suite, workspace  # noqa: E402

u = unit("CF1")
cfg = panel(u)
mode = sys.argv[2]
seeds = range(10) if mode == "mutants" else range(50)
for name in sys.argv[3:]:
    p = Path(name)
    killed = None
    for s in seeds:
        work = workspace(u, p, cfg)
        try:
            ok, output, _ = run_suite(work, cfg["suite"], s)
        finally:
            import shutil

            shutil.rmtree(work, ignore_errors=True)
        if not ok:
            killed = f"seed {s}: {output[-300:]}"
            break
    status = "KILLED" if killed else ("PASSED_ALL_SEEDS" if mode == "alts" else "SURVIVED")
    print(p.name, status, killed or "", flush=True)
