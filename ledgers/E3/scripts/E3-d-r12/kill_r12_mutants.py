"""Kill-check the round-12 mutants with the same logic as tools/mutate_graders.py.

Each mutant is copied in as elicit.py beside the suite and instance, and the suite runs on seeds 0-9 until one fails.
Usage: python3 ledgers/E3/scripts/E3-d-r12/kill_r12_mutants.py [SEEDS]   (default 0-9; run from the checkout)
"""

from __future__ import annotations

import ast
import re
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))

from coursekit import LEDGERS, unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402


def kill(u, mutant: Path, cfg: dict[str, str], seeds: list[int]) -> tuple[str, str, str | None]:
    description = ast.get_docstring(ast.parse(mutant.read_text(encoding="utf-8"))) or "(no description)"
    work = workspace(u, mutant, cfg)
    killed_by = None
    try:
        for seed in seeds:
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                found = re.search(r"FAILED \S+::(\S+)", output)
                killed_by = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                break
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return mutant.name, description.splitlines()[0], killed_by


def main() -> int:
    u = unit("E3")
    cfg = panel(u)
    seeds = parse_seeds(sys.argv[1] if len(sys.argv) > 1 else "0-9")
    mutants = sorted((LEDGERS / u.id / "mutants").glob("r12d_*.py"))
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda m: kill(u, m, cfg, seeds), mutants))
    survivors = 0
    for name, desc, killed_by in results:
        print(f"{'KILLED' if killed_by else 'SURVIVED'} {name}: {desc} -> {killed_by}")
        survivors += killed_by is None
    print(f"round-12 mutants: {len(results) - survivors}/{len(results)} killed")
    return 1 if survivors else 0


if __name__ == "__main__":
    sys.exit(main())
