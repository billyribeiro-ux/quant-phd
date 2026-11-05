# Runs the round-9 student-error mutants (argv: mutant file names) through the E3 suite on seeds 0-9, as tools/mutate_graders.py does.
import ast, re, shutil, sys
from pathlib import Path
sys.path.insert(0, "tools")
from coursekit import LEDGERS, unit
from run_graders import panel, parse_seeds, run_suite, workspace

u = unit("E3")
cfg = panel(u)
for name in sys.argv[1:]:
    mutant = LEDGERS / u.id / "mutants" / name
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
    print(f"{'KILLED' if killed_by else 'SURVIVED'} {mutant.name}: {description} -> {killed_by}", flush=True)
