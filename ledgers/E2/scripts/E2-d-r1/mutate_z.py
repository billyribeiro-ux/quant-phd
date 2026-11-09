# Targeted re-run: the three student-error mutants added in the 33744e5..HEAD delta (z01-z03).
# Same loop as tools/mutate_graders.py mutate(), restricted to the z-files.
import ast, re, shutil, sys
from pathlib import Path
sys.path.insert(0, "tools")
from coursekit import LEDGERS, unit
from run_graders import panel, parse_seeds, run_suite, workspace
u = unit("E2")
cfg = panel(u)
mutants = sorted((LEDGERS / u.id / "mutants").glob("z0*.py"))
print("mutants:", [m.name for m in mutants])
for mutant in mutants:
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
    print(f"{'KILLED' if killed_by else 'SURVIVED'} {mutant.name}: {description.splitlines()[0]} -> {killed_by}")
