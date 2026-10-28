"""Run each alternative implementation through the CF1 suite on seeds 0-49 (round 15, slice d)."""

import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, "/Users/billyribeiro/dev/quant-phd/tools")
from coursekit import unit  # noqa: E402
from run_graders import panel, run_suite, workspace  # noqa: E402

u = unit("CF1")
cfg = panel(u)
for p in sorted(Path(sys.argv[1]).glob("*.py")):
    failure = None
    for s in range(50):
        work = workspace(u, p, cfg)
        try:
            ok, out, _ = run_suite(work, cfg["suite"], s)
        finally:
            shutil.rmtree(work, ignore_errors=True)
        if not ok:
            m = re.search(r"FAILED \S+::(\S+)", out)
            failure = f"seed {s}: {m.group(1) if m else out[-160:]}"
            break
    print(p.name, "PASS 50/50 seeds" if failure is None else f"FAIL {failure}")
