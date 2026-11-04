"""Runs tools/mutate_graders.py's kill loop on the named mutant files only (round-5 verifier, for the new mutants).

Usage (from the checkout): python3 -I ledgers/E3/scripts/E3-d-r5/v5_mutate_subset.py 0-9 mutant.py [mutant.py ...]
Imports the tool's own helpers (panel, workspace, run_suite, parse_seeds) so the kill rule is identical.
"""
import ast
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

seeds = sys.argv[1]
u = unit("E3")
cfg = panel(u)
survivors = 0
for name in sys.argv[2:]:
    mutant = ROOT / "ledgers/E3/mutants" / name
    description = ast.get_docstring(ast.parse(mutant.read_text(encoding="utf-8"))) or "(no description)"
    killed_by = None
    work = workspace(u, mutant, cfg)
    try:
        for seed in parse_seeds(seeds):
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                found = re.search(r"FAILED \S+::(\S+)", output)
                killed_by = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                break
    finally:
        shutil.rmtree(work, ignore_errors=True)
    survivors += killed_by is None
    print(f"{'KILLED' if killed_by else 'SURVIVED'} {mutant.name}: {description.splitlines()[0]} -> {killed_by}", flush=True)
print("subset:", "PASS" if not survivors else "FAIL", f"({len(sys.argv) - 2 - survivors}/{len(sys.argv) - 2} killed)")
