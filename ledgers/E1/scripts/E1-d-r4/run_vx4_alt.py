import sys
from pathlib import Path
ROOT = Path("/tmp/verifyB4-E1-d")
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit
from run_graders import panel, parse_seeds, run_suite, workspace
import shutil
u = unit("E1"); cfg = panel(u)
src = Path(sys.argv[1])
bad = []
for s in parse_seeds("0-49"):
    work = workspace(u, src, cfg)
    try:
        ok, out, _ = run_suite(work, cfg["suite"], s)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    if not ok:
        bad.append((s, out[-400:]))
print(src.name, "PASS 50/50" if not bad else f"FAIL on {len(bad)} seeds; first: {bad[0][0]}\n{bad[0][1]}")
