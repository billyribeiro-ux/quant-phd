"""Run every CF1 slice-a lab mutant under python -I -W error and compare stdout with the twin (round 18)."""
import difflib
import pathlib
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
py = str(root / ".venv/bin/python")
twins = {"L01": root / "tests/labs/CF1/lab-CF1-L01-1.py", "L02": root / "tests/labs/CF1/lab-CF1-L02-1.py"}


def run(path):
    p = subprocess.run([py, "-I", "-W", "error", str(path)], capture_output=True, text=True, timeout=60)
    return p.returncode, p.stdout


base = {k: run(v) for k, v in twins.items()}
for k, (rc, _) in base.items():
    assert rc == 0, (k, rc)
files = []
for d in ["CF1-a-r7", "CF1-a-r8", "CF1-a-r9", "CF1-a-r10", "CF1-a-r11", "CF1-a-r17", "CF1-a-r18"]:
    files += sorted((root / "ledgers/CF1/mutants" / d).glob("*.py"))
killed = survived = 0
for f in files:
    src = f.read_text().splitlines()
    best = min(
        twins,
        key=lambda k: sum(1 for d in difflib.ndiff(twins[k].read_text().splitlines(), src) if d[:1] in "+-"),
    )
    rc, out = run(f)
    verdict = "KILLED" if (rc != 0 or out != base[best][1]) else "SURVIVED"
    killed += verdict == "KILLED"
    survived += verdict == "SURVIVED"
    print(verdict, best, f.parent.name, f.name, "rc=%d" % rc)
print("killed", killed, "survived", survived, "total", len(files))
