import sys, pathlib, shutil
ROOT = pathlib.Path("/tmp/verify42-AC4-e")
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit
from run_graders import panel, workspace, run_suite, parse_seeds
u = unit("AC4"); cfg = panel(u)
seeds = parse_seeds("0-49")
for path in sorted(pathlib.Path(p) for p in sys.argv[1:]):
    bad = None
    work = workspace(u, path, cfg)
    try:
        for seed in seeds:
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            if not ok:
                bad = f"seed {seed}: " + output.strip().splitlines()[-1][:160] if output.strip() else f"seed {seed}"
                break
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"{'PASSES' if bad is None else 'FAILS'} {path.name} on seeds 0-49" + ("" if bad is None else f" -> {bad}"))
