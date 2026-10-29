"""Run every lab-twin mutant under python -I -W error; report exit code and whether its stdout equals the twin's."""
import pathlib, subprocess, sys
root = pathlib.Path(sys.argv[1])
twins = {"L07": root / "tests/labs/AC4/lab-AC4-L07-1.py", "L08": root / "tests/labs/AC4/lab-AC4-L08-1.py"}
base = {k: subprocess.run([sys.executable, "-I", "-W", "error", str(v)], capture_output=True, text=True).stdout for k, v in twins.items()}
files = sorted(p for d in (root / "ledgers/AC4/mutants").glob("AC4-d-r*") for p in d.rglob("*.py"))
killed = survived = 0
for f in files:
    rel = f.relative_to(root)
    tag = "L08" if "L08" in f.name else "L07"
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(f)], capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        killed += 1
        status = f"KILLED exit={r.returncode} last_err={r.stderr.strip().splitlines()[-1][:110] if r.stderr.strip() else ''}"
    else:
        survived += 1
        status = "SURVIVED exit=0 " + ("same-stdout-as-twin" if r.stdout == base[tag] else "different-stdout")
    print(f"{status}  {rel}")
print(f"total={len(files)} killed={killed} survived={survived}")
