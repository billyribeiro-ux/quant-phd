import sys, shutil, re
from pathlib import Path
sys.path.insert(0, "/tmp/verify14-CF1-d/tools")
from coursekit import unit
from run_graders import panel, workspace, run_suite
u = unit("CF1"); cfg = panel(u)
for p in sorted(Path(sys.argv[1]).glob("*.py")):
    res = []
    for s in range(10):
        work = workspace(u, p, cfg)
        try:
            ok, out, _ = run_suite(work, cfg["suite"], s)
        finally:
            shutil.rmtree(work, ignore_errors=True)
        if not ok:
            m = re.search(r"FAILED \S+::(\S+)", out)
            res.append(f"s{s}:FAIL {m.group(1) if m else out[-120:]}")
            break
        res.append(f"s{s}:ok")
    print(p.name, "PASS all 10 seeds" if all(r.endswith(":ok") for r in res[-1:]) and len(res) == 10 else res)
