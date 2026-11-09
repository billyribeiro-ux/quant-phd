"""Round 18 (BK4 slice c): run the round-18 student-error mutants through the BK4 suite, the same way
tools/mutate_graders.py does, on seeds 0-49. Usage: python -I run_r18_mutants.py <checkout-root>"""
import ast
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

u = unit("BK4")
cfg = panel(u)
mutants = sorted((ROOT / "ledgers/BK4/mutants").glob("r18*.py"))
for mutant in mutants:
    desc = ast.get_docstring(ast.parse(mutant.read_text(encoding="utf-8"))) or "(no description)"
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
    print(f"{'KILLED' if killed_by else 'SURVIVED'} {mutant.name}: {desc.splitlines()[0]} -> {killed_by}")
