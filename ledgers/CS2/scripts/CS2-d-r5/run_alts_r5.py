"""Round-5 verifier (CS2-d): run each correct alternative and each listed mutant through the CS2 autograder.

Usage: python -I ledgers/CS2/scripts/CS2-d-r5/run_alts_r5.py <seeds> <module> [<module> ...]
Uses the same panel, workspace and run_suite helpers as tools/run_graders.py and tools/mutate_graders.py, so the
suite and the seeds are those of the repository. Prints PASS/FAIL per module and the first failing test per seed.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(sys.argv[0]).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))

from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

u = unit("CS2")
cfg = panel(u)
seeds = parse_seeds(sys.argv[1])
for name in sys.argv[2:]:
    path = Path(name).resolve()
    failures: dict[int, str] = {}
    work = workspace(u, path, cfg)
    try:
        for seed in seeds:
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                found = re.search(r"FAILED \S+::(\S+)", output)
                failures[seed] = found.group(1) if found else "collection/import error"
    finally:
        shutil.rmtree(work, ignore_errors=True)
    status = "PASS" if not failures else "FAIL"
    first = sorted(failures.items())[:3]
    print(f"{status} {path.name} seeds={len(seeds)} failing_seeds={len(failures)} first={first}")
