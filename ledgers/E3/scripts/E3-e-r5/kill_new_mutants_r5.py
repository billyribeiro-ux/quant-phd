"""Run only the round-5 mutants (g5_*) through the E3 grader suite on seeds 0-9, with the same workspace and
run function that tools/mutate_graders.py uses. Usage: python -I kill_new_mutants_r5.py <checkout-root>
"""

import ast
import re
import shutil
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

u = unit("E3")
cfg = panel(u)
for mutant in sorted((root / "ledgers" / "E3" / "mutants").glob("g5_*.py")):
    description = ast.get_docstring(ast.parse(mutant.read_text(encoding="utf-8"))) or "(no description)"
    killed_by = None
    work = workspace(u, mutant, cfg)
    try:
        for seed in parse_seeds("0-9"):
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                found = re.search(r"FAILED \S+::(\S+)", output)
                killed_by = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                break
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"{'KILLED' if killed_by else 'SURVIVED'} {mutant.name}: {description.splitlines()[0]} -> {killed_by}", flush=True)
