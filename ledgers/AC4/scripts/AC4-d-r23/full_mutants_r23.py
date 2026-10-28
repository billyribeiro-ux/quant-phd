import subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
ref = {t: subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/AC4/lab-AC4-{t}-1.py")], capture_output=True, text=True) for t in ("L07", "L08")}
for p in sorted(root.glob("ledgers/AC4/mutants/AC4-d-r*/*.py")):
    twin = "L07" if "L07" in p.name else ("L08" if "L08" in p.name else None)
    if twin is None:
        print(p.parent.name, p.name, "no twin tag"); continue
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(p)], capture_output=True, text=True, timeout=120)
    diff = r.stdout != ref[twin].stdout
    print(f"{p.parent.name}/{p.name} | twin {twin} | exit {r.returncode} | output_differs {diff} | {'KILLED' if (r.returncode!=0 or diff) else 'SURVIVED'}")
