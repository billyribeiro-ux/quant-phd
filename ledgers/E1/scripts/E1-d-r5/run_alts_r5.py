"""Run one candidate module through the E1 project suite on seeds 0-49 (verifier r5)."""
import sys
import shutil
from pathlib import Path

ROOT = Path("/tmp/verifyB5-E1-d")
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, parse_seeds, run_suite, workspace  # noqa: E402

u = unit("E1")
cfg = panel(u)
src = Path(sys.argv[1])
seeds = sys.argv[2] if len(sys.argv) > 2 else "0-49"
bad = []
for s in parse_seeds(seeds):
    work = workspace(u, src, cfg)
    try:
        ok, out, _ = run_suite(work, cfg["suite"], s)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    if not ok:
        bad.append((s, out[-600:]))
print(src.name, "PASS" if not bad else f"FAIL on {len(bad)} seeds; first seed {bad[0][0]}")
if bad:
    print(bad[0][1])
