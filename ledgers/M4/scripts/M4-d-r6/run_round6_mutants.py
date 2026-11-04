"""Round-6 verifier (slice d): run named mutants through the same grader panel, workspace and suite runner the gate uses.

Usage: .venv/bin/python ledgers/M4/scripts/M4-d-r6/run_round6_mutants.py r6d_01 r6d_02 ...  (prefixes of files in mutants/)
Each mutant runs on seeds 0-9 (the gate's window) and reports KILLED with the first failing test, or SURVIVED.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import shutil  # noqa: E402

from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402
import re  # noqa: E402

u = unit("M4")
cfg = panel(u)
mutants = sorted((ROOT / "ledgers" / "M4" / "mutants").glob("*.py"))
for prefix in sys.argv[1:]:
    matches = [m for m in mutants if m.name.startswith(prefix)]
    for mutant in matches:
        work = workspace(u, mutant, cfg)
        killed = None
        try:
            for seed in parse_seeds("0-9"):
                ok, output, _ = run_suite(work, cfg["suite"], seed)
                if not ok:
                    found = re.search(r"FAILED \S+::(\S+)", output)
                    killed = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                    break
        finally:
            shutil.rmtree(work, ignore_errors=True)
        print(f"{'KILLED' if killed else 'SURVIVED'} {mutant.name} -> {killed}")
