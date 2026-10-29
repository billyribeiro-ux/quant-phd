"""Round-8 verifier script: print the failing test lines of one alternative on one seed (diagnostic only)."""
import shutil, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit  # noqa: E402
from run_graders import panel, run_suite, workspace  # noqa: E402
u = unit("CS2"); cfg = panel(u)
src = Path(sys.argv[1]); seed = int(sys.argv[2])
work = workspace(u, src, cfg)
try:
    ok, output, _ = run_suite(work, cfg["suite"], seed)
finally:
    shutil.rmtree(work, ignore_errors=True)
lines = [l for l in output.splitlines() if "FAILED" in l or "Error" in l or "assert" in l.lower()]
print("ok", ok)
print("\n".join(lines[:12]))
print(output[-1500:])
