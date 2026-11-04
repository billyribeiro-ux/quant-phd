"""Run candidate streamstats.py files through the CS2 suite on seeds 0-49 (same flags as tools/run_graders.py)."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "tools"))
import run_graders as rg  # noqa: E402
from coursekit import unit  # noqa: E402

u = unit("CS2")
cfg = rg.panel(u)
seeds = list(range(int(sys.argv[2]), int(sys.argv[3]) + 1))
for path in sys.argv[4:]:
    p = pathlib.Path(path)
    work = rg.workspace(u, p, cfg)
    passed = []
    failed = []
    try:
        for seed in seeds:
            ok, out, _ = rg.run_suite(work, cfg["suite"], seed)
            (passed if ok else failed).append(seed)
            if not ok and len(failed) == 1:
                first = [ln for ln in out.splitlines() if "FAILED" in ln or "Error" in ln][:3]
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)
    print(f"{p.name}: passed {len(passed)}/{len(seeds)} seeds; failing seeds {failed[:10]}")
    if failed:
        print("   first failure lines:", first)
