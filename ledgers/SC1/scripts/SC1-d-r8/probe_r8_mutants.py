"""Round 8: run the grader suite on each r8_* mutant over seeds 0-49 (stops at the first kill); prints the outcome."""
import glob
import os
import re
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE8-SC1-d")
sys.path.insert(0, str(ROOT / "tools"))
os.chdir(ROOT)
import mutate_graders as mg  # noqa: E402
from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

u = unit("SC1")
cfg = panel(u)
for path in sorted(glob.glob(str(ROOT / "ledgers/SC1/mutants/r8_*.py"))):
    mutant = Path(path)
    work = workspace(u, mutant, cfg)
    killed = None
    seeds_run = 0
    try:
        for seed in parse_seeds("0-49"):
            seeds_run += 1
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                found = re.search(r"FAILED \S+::(\S+)", output)
                killed = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                break
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)
    print(f"{'KILLED' if killed else 'SURVIVED'} {mutant.name} (seeds run {seeds_run}) -> {killed}")
