"""Run alternative implementations through the CS2 grader suite on a list of seeds (same flags as run_graders).

Usage: python -I run_alts.py <repo_root> <seeds e.g. 0-49> <file.py> [file.py ...]
Imports tools/ from the checkout (coursekit, run_graders) and reuses workspace() and run_suite() unchanged.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

seeds = parse_seeds(sys.argv[2])
u = unit("CS2")
cfg = panel(u)
for name in sys.argv[3:]:
    path = Path(name).resolve()
    failures: list[str] = []
    for seed in seeds:
        work = workspace(u, path, cfg)
        try:
            ok, output, _ = run_suite(work, cfg["suite"], seed)
        finally:
            shutil.rmtree(work, ignore_errors=True)
        if not ok:
            found = re.search(r"FAILED \S+::(\S+)", output)
            failures.append(f"seed {seed}: {found.group(1) if found else 'error'}")
            if len(failures) >= 3:
                break
    verdict = "PASS" if not failures else "FAIL"
    print(f"{verdict} {path.name} seeds={len(seeds)} " + ("; ".join(failures) if failures else ""))
