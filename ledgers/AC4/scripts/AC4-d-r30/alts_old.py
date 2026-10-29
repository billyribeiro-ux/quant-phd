import pathlib, subprocess, sys
root = pathlib.Path(sys.argv[1])
base = {k: subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/AC4/lab-AC4-{k}-1.py")], capture_output=True, text=True).stdout for k in ("L07", "L08")}
for f in sorted((root / "ledgers/AC4/scripts").glob("AC4-d-r*/alts/*.py")):
    tag = "L08" if "L08" in f.name else "L07"
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(f)], capture_output=True, text=True)
    print(("exit0 " if r.returncode == 0 else f"EXC{r.returncode} ") + ("SAME-AS-TWIN " if r.stdout == base[tag] else "DIFFERENT ") + f"{f.parent.parent.name}/alts/{f.name}")
