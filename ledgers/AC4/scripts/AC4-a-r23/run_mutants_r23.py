"""Round 23: run every AC4-a lab-twin mutant (r18..r22, plus any r23 mutants) under python -I -W error.

A mutant is KILLED when its exit code is nonzero or its stdout differs from the unmutated twin's stdout.
"""
import subprocess, sys
from pathlib import Path

ROOT = Path(sys.argv[1])
base = {}
for lab in ("L01", "L02"):
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/AC4/lab-AC4-{lab}-1.py")],
                         capture_output=True, text=True, timeout=60)
    base[lab] = run.stdout
count = {"KILLED": 0, "SURVIVED": 0}
for d in sorted((ROOT / "ledgers/AC4/mutants").glob("AC4-a-r*")):
    for mut in sorted(d.glob("*.py")):
        lab = "L01" if mut.name.startswith("L01") else "L02"
        run = subprocess.run([sys.executable, "-I", "-W", "error", str(mut)],
                             capture_output=True, text=True, timeout=60)
        if run.returncode != 0 or run.stdout != base[lab]:
            status = "KILLED"
            why = f"rc={run.returncode} stdout_differs={run.stdout != base[lab]}"
        else:
            status = "SURVIVED"
            why = "rc=0 stdout identical"
        count[status] += 1
        print(f"{d.name}/{mut.name}: {status} {why}")
print(count)
