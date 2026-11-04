"""Run the round-6 student-error mutants through the grader suite (same harness as tools/mutate_graders.py).

Usage (from the checkout root): .venv/bin/python <this file> <checkout root> <seeds, e.g. 0-9> <mutant file> [...]
"""
import ast
import re
import shutil
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

u = unit("E3")
cfg = panel(u)
seeds = parse_seeds(sys.argv[2])
for arg in sys.argv[3:]:
    mutant = Path(arg)
    doc = ast.get_docstring(ast.parse(mutant.read_text(encoding="utf-8"))) or "(no description)"
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
    print(f"{'KILLED' if killed_by else 'SURVIVED'} {mutant.name}: {doc.splitlines()[0]} -> {killed_by}", flush=True)
