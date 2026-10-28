import sys, pathlib, shutil
ROOT = pathlib.Path(sys.argv[1]); sys.path.insert(0, str(ROOT / "tools"))
from coursekit import unit
from run_graders import panel, parse_seeds, run_suite, workspace
u = unit("AC4"); cfg = panel(u)
seeds = parse_seeds(sys.argv[2])
for f in sys.argv[3:]:
    p = pathlib.Path(f); killed = None; n_ok = 0
    work = workspace(u, p, cfg)
    try:
        for s in seeds:
            ok, out, _ = run_suite(work, cfg["suite"], s)
            if not ok:
                import re
                m = re.search(r"FAILED \S+::(\S+)", out)
                killed = (m.group(1) if m else "collection/import error") + f" (seed {s})"; break
            n_ok += 1
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(("KILLED " if killed else "PASS   ") + p.name + " -> " + (killed or f"{n_ok}/{len(seeds)} seeds passed"))
