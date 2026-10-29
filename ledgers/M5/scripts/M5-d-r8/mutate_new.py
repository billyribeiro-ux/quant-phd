import sys, ast, shutil
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyB8-M5-d/tools")
from pathlib import Path
from coursekit import LEDGERS, unit
from run_graders import panel, parse_seeds, run_suite, workspace
import re
u = unit("M5")
cfg = panel(u)
for name in sys.argv[1:]:
    mutant = LEDGERS / u.id / "mutants" / name
    desc = ast.get_docstring(ast.parse(mutant.read_text(encoding="utf-8")))
    killed_by = None
    work = workspace(u, mutant, cfg)
    try:
        for seed in parse_seeds("0-49"):
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                found = re.search(r"FAILED \S+::(\S+)", output)
                killed_by = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                break
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(("KILLED " if killed_by else "SURVIVED ") + name + " -> " + str(killed_by))
