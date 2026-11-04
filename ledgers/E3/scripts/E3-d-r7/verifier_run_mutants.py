import sys, re, shutil, ast
from pathlib import Path
CHECKOUT = Path("/Users/billyribeiro/.fanout/wt/verifyD7-E3-d")
sys.path.insert(0, str(CHECKOUT / "tools"))
from coursekit import unit
from run_graders import panel, parse_seeds, run_suite, workspace
u = unit("E3")
cfg = panel(u)
names = sys.argv[1].split(",")
seeds = parse_seeds(sys.argv[2] if len(sys.argv) > 2 else "0-9")
for name in names:
    mutant = CHECKOUT / "ledgers/E3/mutants" / name
    desc = ast.get_docstring(ast.parse(mutant.read_text(encoding="utf-8"))).splitlines()[0]
    killed = None
    work = workspace(u, mutant, cfg)
    try:
        for seed in seeds:
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                found = re.search(r"FAILED \S+::(\S+)", output)
                killed = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                break
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(("KILLED " if killed else "SURVIVED ") + name + ": " + desc + " -> " + str(killed), flush=True)
