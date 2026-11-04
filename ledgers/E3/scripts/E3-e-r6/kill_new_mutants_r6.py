# Runs the three verifier-written mutants (r6_*) through the E3 suite on seeds 0-9, using the tools' own workspace code.
import ast, re, shutil, sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD6-E3-e/tools")
from coursekit import LEDGERS, unit
from run_graders import panel, parse_seeds, run_suite, workspace
u = unit("E3")
cfg = panel(u)
for mutant in sorted((LEDGERS / u.id / "mutants").glob("r6_*.py")):
    desc = ast.get_docstring(ast.parse(mutant.read_text(encoding="utf-8"))) or ""
    killed = None
    work = workspace(u, mutant, cfg)
    try:
        for seed in parse_seeds("0-9"):
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                found = re.search(r"FAILED \S+::(\S+)", output)
                killed = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                break
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(("KILLED " if killed else "SURVIVED ") + mutant.name + " | " + desc.splitlines()[0] + " -> " + str(killed))
