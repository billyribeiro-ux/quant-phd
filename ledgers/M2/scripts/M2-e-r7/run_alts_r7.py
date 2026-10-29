"""Run the M2 project suite against each alternative implementation over seeds 0-49, in fresh scratch dirs."""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT, ALTS, GRADER = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
py = str(ROOT / ".venv/bin/python")
for alt in sorted(ALTS.glob("*.py")):
    fails = []
    for seed in range(50):
        work = Path("/tmp/m2e_r7/work") / alt.stem
        shutil.rmtree(work, ignore_errors=True)
        work.mkdir(parents=True)
        shutil.copy(GRADER / "instance.py", work)
        shutil.copy(GRADER / "test_project.py", work)
        shutil.copy(alt, work / "sensitivity_engine.py")
        env = {"QF_SEED": str(seed), "PATH": "/usr/bin:/bin"}
        r = subprocess.run([py, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=work, env=env, capture_output=True, text=True)
        if r.returncode != 0:
            last = [l for l in r.stdout.splitlines() if l.startswith("FAILED")]
            fails.append((seed, last[:2] or r.stdout[-300:]))
    print(f"{alt.name}: {50 - len(fails)}/50 seeds pass", "" if not fails else fails[:3])
