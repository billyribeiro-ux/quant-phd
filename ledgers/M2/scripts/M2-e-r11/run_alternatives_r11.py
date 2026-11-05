"""Run every alternative implementation (r10 and r11) against the M2 suite on seeds 0-49, as sensitivity_engine.py in a scratch copy."""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path
root = Path(sys.argv[1])
py = str(root / ".venv/bin/python")
ALT_DIRS = ["ledgers/M2/scripts/M2-e-r3/alts", "ledgers/M2/scripts/M2-e-r5/alts_r5", "ledgers/M2/scripts/M2-e-r6/alts_r6",
            "ledgers/M2/scripts/M2-e-r7/alts_new", "ledgers/M2/scripts/M2-e-r8/alts_r8", "ledgers/M2/scripts/M2-e-r9/alts_r9",
            "ledgers/M2/scripts/M2-e-r10/alts_r10", "ledgers/M2/scripts/M2-e-r11/alts_r11"]
alts = [p for d in ALT_DIRS for p in sorted(Path(root, d).glob("*.py"))]
for alt in alts:
    work = Path(tempfile.mkdtemp(prefix="m2e_r11_"))
    shutil.copy(root / "course/modules/M/M2/grader/test_project.py", work)
    shutil.copy(root / "course/modules/M/M2/grader/instance.py", work)
    shutil.copy(alt, work / "sensitivity_engine.py")
    shutil.copy(root / "course/modules/M/M2/grader/reference.py", work / "reference_core.py")  # round-3 alternatives import it
    fails = []
    for seed in range(50):
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        r = subprocess.run([py, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                            "test_project.py"], cwd=work, env=env, capture_output=True, text=True)
        if r.returncode != 0:
            fails.append((seed, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]))
    print(f"{alt.name}: {50 - len(fails)}/50 seeds pass", "" if not fails else f"first failures: {fails[:3]}")
