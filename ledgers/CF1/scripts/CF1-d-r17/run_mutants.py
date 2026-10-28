"""Run the CF1 suite on each mutant given as argv[2:] with seeds 0-9 (the mutate_graders procedure)."""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1] + "/tools")
from coursekit import unit  # noqa: E402
from run_graders import panel, run_suite, workspace  # noqa: E402

u = unit("CF1")
cfg = panel(u)
for name in sys.argv[2:]:
    p = Path(name)
    killed = None
    for s in range(10):
        work = workspace(u, p, cfg)
        try:
            ok, output, _ = run_suite(work, cfg["suite"], s)
        finally:
            shutil.rmtree(work, ignore_errors=True)
        if not ok:
            killed = f"seed {s}: {output[-400:]}"
            break
    print(p.name, "KILLED" if killed else "SURVIVED", killed or "")
