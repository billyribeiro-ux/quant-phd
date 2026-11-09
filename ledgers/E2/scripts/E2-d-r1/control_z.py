# Control: reference solution must pass seed 0; each z-mutant must fail with the named test.
import subprocess, sys, shutil
from pathlib import Path
sys.path.insert(0, "tools")
from coursekit import LEDGERS, unit
from run_graders import panel, workspace
u = unit("E2"); cfg = panel(u)
print("cfg:", {k: cfg[k] for k in cfg if k in ("suite", "solution", "grader", "support")})
ref = u.directory / cfg["grader"] / "reference.py"
for label, src in [("reference", ref)] + [(p.name, p) for p in sorted((LEDGERS / u.id / "mutants").glob("z0*.py"))]:
    work = workspace(u, src, cfg)
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", cfg["suite"]], cwd=work,
                           capture_output=True, text=True, env={"PATH": "/usr/bin:/bin", "QF_SEED": "0", "PYTHONHASHSEED": "0"})
        tail = [l for l in r.stdout.splitlines() if l.startswith("FAILED") or " passed" in l or " failed" in l]
        print(label, "rc", r.returncode, "|", " ; ".join(tail)[:400])
    finally:
        shutil.rmtree(work, ignore_errors=True)
