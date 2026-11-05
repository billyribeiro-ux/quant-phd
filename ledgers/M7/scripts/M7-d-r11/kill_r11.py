"""Run the M7 suite against the named mutant files on seeds 0-49; print KILLED/SURVIVED with the first failing test."""
import re, shutil, sys
from pathlib import Path
ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import LEDGERS, unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402
u = unit("M7")
cfg = panel(u)
files = [Path(p) for p in sys.argv[3:]]
seeds = parse_seeds(sys.argv[2])
for mutant in files:
    work = workspace(u, mutant, cfg)
    killed = None
    try:
        for seed in seeds:
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                found = re.search(r"FAILED \S+::(\S+)", output)
                killed = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                break
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"{'KILLED' if killed else 'SURVIVED'} {mutant.name} -> {killed}", flush=True)
