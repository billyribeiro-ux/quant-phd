"""Compare each mutant or alternative with the twin's stdout (the verbatim embedded block) and exit code."""
import pathlib, subprocess, sys
root = pathlib.Path(sys.argv[1])
base = {k: subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/AC4/lab-AC4-{k}-1.py")], capture_output=True, text=True).stdout for k in ("L07", "L08")}
for f in sorted((root / "ledgers/AC4/mutants/AC4-d-r30").glob("*.py")) + sorted((root / "ledgers/AC4/scripts/AC4-d-r30/alts").glob("*.py")):
    tag = "L08" if "L08" in f.name else "L07"
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(f)], capture_output=True, text=True)
    if r.returncode:
        print(f"EXC exit={r.returncode} {r.stderr.strip().splitlines()[-1][:100]} {f.parent.name}/{f.name}")
    else:
        print(("SAME-AS-TWIN " if r.stdout == base[tag] else "DIFFERENT-OUTPUT ") + f"{f.parent.name}/{f.name}")
