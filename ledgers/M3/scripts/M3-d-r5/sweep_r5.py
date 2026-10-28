"""Run the M3 project suite on given solution files over a seed window; print failing seeds and the first failing test.

Usage: sweep_r5.py <seeds> <solution.py> [<solution.py> ...]   (run from the checkout root)
"""
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "tools"))
import run_graders as rg  # noqa: E402
from coursekit import unit  # noqa: E402

u = unit("M3")
cfg = rg.panel(u)
seeds = rg.parse_seeds(sys.argv[1])
for src in sys.argv[2:]:
    failing = []
    first = None
    for seed in seeds:
        work = rg.workspace(u, Path(src), cfg)
        try:
            ok, output, _ = rg.run_suite(work, cfg["suite"], seed)
        finally:
            import shutil
            shutil.rmtree(work, ignore_errors=True)
        if not ok:
            failing.append(seed)
            if first is None:
                import re
                m = re.search(r"FAILED \S+::(\S+)", output)
                first = m.group(1) if m else output[-300:]
    print(f"{Path(src).name}: {len(seeds) - len(failing)}/{len(seeds)} seeds pass; failing seeds {failing[:10]}; first: {first}")
