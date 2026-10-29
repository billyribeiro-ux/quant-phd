"""Round 4: run the five alternative correct implementations and the reference on seeds 0-49 with the current suite."""
import pathlib, shutil, sys
ROOT = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "tools"))
from coursekit import LEDGERS, unit
from run_graders import panel, parse_seeds, run_suite, workspace
u = unit("FC1")
cfg = panel(u)
cands = sorted((LEDGERS / u.id / "alternatives").glob("*.py")) if False else sorted((ROOT / "ledgers/FC1/alternatives").glob("*.py"))
cands.append(ROOT / "course/modules/FC/FC1/grader/reference.py")
for c in cands:
    bad = []
    for seed in parse_seeds("0-49"):
        work = workspace(u, c, cfg)
        try:
            ok, output, _ = run_suite(work, cfg["suite"], seed)
        finally:
            shutil.rmtree(work, ignore_errors=True)
        if not ok:
            bad.append(seed)
    print(c.name, "failing seeds:", len(bad), bad[:5])
