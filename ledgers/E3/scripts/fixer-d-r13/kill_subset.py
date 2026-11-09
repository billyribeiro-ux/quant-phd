"""Run the E3 mutate step (tools/mutate_graders.py semantics) on a named subset of mutants and seeds."""
import ast
import re
import shutil
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/dev/quant-phd")
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import LEDGERS, unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

u = unit("E3")
cfg = panel(u)
names = sys.argv[1].split(",")
seeds = parse_seeds(sys.argv[2])
for name in names:
    mutant = (LEDGERS / u.id / sys.argv[3] if len(sys.argv) > 3 else LEDGERS / u.id / "mutants") / name
    description = ast.get_docstring(ast.parse(mutant.read_text(encoding="utf-8"))) or "(no description)"
    killed_by = None
    work = workspace(u, mutant, cfg)
    try:
        for seed in seeds:
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                found = re.search(r"FAILED \S+::(\S+)", output)
                killed_by = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                break
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"{'KILLED' if killed_by else 'SURVIVED'} {mutant.name}: {description.splitlines()[0][:90]} -> {killed_by}", flush=True)
