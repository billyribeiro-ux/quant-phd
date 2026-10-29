import sys, shutil, re
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyB8-M5-d/tools")
from pathlib import Path
from coursekit import unit
from run_graders import panel, parse_seeds, run_suite, workspace
u = unit("M5"); cfg = panel(u)
for p in sys.argv[1:]:
    path = Path(p)
    work = workspace(u, path, cfg)
    res = []
    try:
        for seed in parse_seeds("0-4"):
            ok, output, _ = run_suite(work, cfg["suite"], seed)
            found = re.findall(r"FAILED \S+::(\S+)", output)
            res.append((seed, ok, found[:2]))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(path.name, "all-pass" if all(r[1] for r in res) else "FAILS", res[0][2] if not res[0][1] else "")
