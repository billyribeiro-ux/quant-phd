"""Run the M2 suite (pinned grader copy) against each alternative over seeds 0-49, each in a fresh scratch dir."""
import shutil, subprocess, sys
from pathlib import Path
ROOT = Path(sys.argv[1]); GRADER = ROOT / "course/modules/M/M2/grader"; PY = str(ROOT / ".venv/bin/python")
work_root = Path("/tmp/m2e-r8-alts")
results = []
for arg in sys.argv[2:]:
    alt = Path(arg)
    fails = []
    for seed in range(50):
        work = work_root / alt.stem / str(seed)
        shutil.rmtree(work, ignore_errors=True); work.mkdir(parents=True)
        shutil.copy(GRADER / "instance.py", work); shutil.copy(GRADER / "test_project.py", work)
        shutil.copy(alt, work / "sensitivity_engine.py")
        r = subprocess.run([PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=work, env={"QF_SEED": str(seed), "PATH": "/usr/bin:/bin"}, capture_output=True, text=True)
        if r.returncode != 0:
            failed = [l for l in r.stdout.splitlines() if l.startswith("FAILED")]
            fails.append((seed, failed[:2] or r.stdout[-200:]))
    print(f"{alt.parent.parent.name}/{alt.name}: {50 - len(fails)}/50 seeds pass", "" if not fails else fails[:3], flush=True)
