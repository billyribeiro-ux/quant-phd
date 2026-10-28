"""Run candidate implementations over seeds through the repository's workspace and suite runner."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, "/tmp/quant-b2/tools")
from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

u = unit("CS2")
cfg = panel(u)
seeds = parse_seeds(sys.argv[1])
for arg in sys.argv[2:]:
    path = Path(arg)
    work = workspace(u, path, cfg)
    failed: list[int] = []
    try:
        for seed in seeds:
            ok, _, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                failed.append(seed)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"{path.name}: {len(seeds) - len(failed)}/{len(seeds)} seeds pass" + (f" failing {failed[:5]}" if failed else ""))
