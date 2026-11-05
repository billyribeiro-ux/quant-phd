"""Run the round-10 verifier mutants (v10_*) through the same workspace and suite runner as tools/mutate_graders.py."""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD10-E3-d")
sys.path.insert(0, str(ROOT / "tools"))

from coursekit import LEDGERS, unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

u = unit("E3")
cfg = panel(u)
seeds = parse_seeds("0-9")
for mutant in sorted((LEDGERS / u.id / "mutants").glob("v10_*.py")):
    killed_by = None
    work = workspace(u, mutant, cfg)
    try:
        for seed in seeds:
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                found = re.search(r"FAILED \S+::(\S+)", output)
                killed_by = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                break
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"{'KILLED' if killed_by else 'SURVIVED'} {mutant.name} -> {killed_by}", flush=True)
