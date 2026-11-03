"""Round-2 verifier: run the M7 suite (unchanged grader files) against each alternative on seeds 0-49."""
import sys
import pathlib

REPO = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD2-M7-d")
sys.path.insert(0, str(REPO / "tools"))
import run_graders as rg  # noqa: E402
from coursekit import unit  # noqa: E402

u = unit("M7")
cfg = rg.panel(u)
name = sys.argv[1]
src = REPO / "ledgers/M7/scripts/M7-d-r2/alts" / f"{name}.py"
seeds = rg.parse_seeds(sys.argv[2] if len(sys.argv) > 2 else "0-49")
bad = []
for seed in seeds:
    work = rg.workspace(u, src, cfg)
    try:
        ok, out, secs = rg.run_suite(work, cfg["suite"], seed)
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)
    if not ok:
        bad.append(seed)
        print(f"{name} seed {seed} FAILED: {out[-600:]}")
print(f"{name}: {len(seeds) - len(bad)}/{len(seeds)} seeds pass the unchanged suite")
