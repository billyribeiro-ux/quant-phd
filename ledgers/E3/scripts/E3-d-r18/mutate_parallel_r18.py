"""Verifier driver (round 18): the same kill logic as tools/mutate_graders.py (the tool's own panel, workspace and
run_suite helpers; a mutant is killed by the first seed on which the suite fails), run with one process per mutant so the
standing set finishes in minutes. Writes one line per mutant, then a summary.

Usage (repo root): .venv/bin/python -I ledgers/E3/scripts/E3-d-r18/mutate_parallel_r18.py <out.txt> 0-9
"""

import ast
import re
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "tools"))


def job(args: tuple[str, str]) -> str:
    from coursekit import unit  # noqa: PLC0415
    from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: PLC0415

    mutant_path, seeds = Path(args[0]), args[1]
    u = unit("E3")
    cfg = panel(u)
    description = ast.get_docstring(ast.parse(mutant_path.read_text(encoding="utf-8"))) or "(no description)"
    killed_by = None
    work = workspace(u, mutant_path, cfg)
    try:
        for seed in parse_seeds(seeds):
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                found = re.search(r"FAILED \S+::(\S+)", output)
                killed_by = f"{found.group(1) if found else 'collection/import error'} (seed {seed})"
                break
    finally:
        shutil.rmtree(work, ignore_errors=True)
    status = "KILLED" if killed_by else "SURVIVED"
    return f"{status} {mutant_path.name}: {description.splitlines()[0]} -> {killed_by}"


if __name__ == "__main__":
    out, seeds = sys.argv[1], sys.argv[2]
    mutants = sorted((ROOT / "ledgers/E3/mutants").glob("*.py"))
    with ProcessPoolExecutor(max_workers=14) as ex:
        lines = list(ex.map(job, [(str(m), seeds) for m in mutants]))
    killed = sum(l.startswith("KILLED") for l in lines)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
        fh.write(f"mutate_parallel E3: {'PASS' if killed == len(lines) else 'FAIL'} ({killed}/{len(lines)} killed)\n")
    print("done", killed, len(lines))
