"""Round-10: run the grader-mutation loop of tools/mutate_graders.py on the round-10 mutants only (seeds 0-9)."""

import ast
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import mutate_graders as mg  # noqa: E402

unit = mg.unit("E3")
cfg = mg.panel(unit)
mutants = sorted((mg.LEDGERS / unit.id / "mutants").glob("r10e_*.py"))
for mutant in mutants:
    description = ast.get_docstring(ast.parse(mutant.read_text(encoding="utf-8"))) or "(no description)"
    killed_by = None
    work = mg.workspace(unit, mutant, cfg)
    try:
        for seed in mg.parse_seeds("0-9"):
            ok, output, _ = mg.run_suite(work, cfg["suite"], seed)
            if not ok:
                found = re.search(r"FAILED \S+::(\S+)", output)
                killed_by = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                break
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"{'KILLED' if killed_by else 'SURVIVED'} {mutant.name}: {description.splitlines()[0]} -> {killed_by}")
