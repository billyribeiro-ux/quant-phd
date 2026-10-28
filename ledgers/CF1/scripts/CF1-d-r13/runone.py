import sys, shutil
from pathlib import Path
sys.path.insert(0, "/tmp/verify13-CF1-d/tools")
from coursekit import unit
from run_graders import panel, workspace, run_suite
u = unit("CF1")
cfg = panel(u)
mode, src = sys.argv[1], Path(sys.argv[2])
seeds = [int(s) for s in sys.argv[3].split(",")] if len(sys.argv) > 3 else [0]
if mode == "collect":
    work = workspace(u, u.directory / cfg["grader"] / "reference.py", cfg)
    import subprocess
    r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q", cfg["suite"]], cwd=work, capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1])
    shutil.rmtree(work, ignore_errors=True)
else:
    work = workspace(u, src, cfg)
    try:
        for s in seeds:
            ok, out, _ = run_suite(work, cfg["suite"], s)
            import re
            m = re.search(r"FAILED \S+::(\S+)", out)
            print("seed", s, "PASS" if ok else ("FAIL " + (m.group(1) if m else out[-200:])))
    finally:
        shutil.rmtree(work, ignore_errors=True)
