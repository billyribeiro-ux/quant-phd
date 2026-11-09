"""Round-16 fixer: runs the mutate_graders protocol (suite per seed, killed on the first failing seed) on the named
mutants only. Run from the repository root: .venv/bin/python ledgers/M7/scripts/M7-d-r16/mutate_subset_r16.py SEEDS NAME...
NAME is a file stem under ledgers/M7/mutants/ or ledgers/M7/equivalent/ (the folder is given with a prefix 'eq:')."""
import ast, re, shutil, sys
from pathlib import Path
sys.path.insert(0, "tools")
from coursekit import LEDGERS, unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

u = unit("M7")
cfg = panel(u)
seeds = parse_seeds(sys.argv[1])
for name in sys.argv[2:]:
    folder = LEDGERS / u.id / ("equivalent" if name.startswith("eq:") else "mutants")
    path = folder / (name.removeprefix("eq:") + ".py")
    description = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or "(no description)"
    killed_by = None
    work = workspace(u, path, cfg)
    try:
        for seed in seeds:
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                found = re.search(r"FAILED \S+::(\S+)", output)
                killed_by = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                break
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"{'KILLED' if killed_by else 'SURVIVED'} {path.name}: {description.splitlines()[0][:110]} -> {killed_by}")
