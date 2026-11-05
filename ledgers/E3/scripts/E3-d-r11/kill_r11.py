"""Round-11: run the grader suite on the round-11 mutants (same procedure as tools/mutate_graders.py, seeds 0-9)."""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

u = unit("E3")
cfg = panel(u)
names = sys.argv[1:] or sorted(p.name for p in (ROOT / "ledgers/E3/mutants").glob("r11d_*.py"))
for name in names:
    mutant = ROOT / "ledgers/E3/mutants" / name
    killed_by = None
    work = workspace(u, mutant, cfg)
    try:
        for seed in parse_seeds("0-9"):
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                found = re.findall(r"FAILED \S+::(\S+)", output)
                killed_by = f"{found[0] if found else 'collection/import error'} (seed {seed}); failing: {len(found)}"
                break
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"{'KILLED' if killed_by else 'SURVIVED'} {name} -> {killed_by}", flush=True)
