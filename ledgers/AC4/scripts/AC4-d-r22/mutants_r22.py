import difflib, pathlib, subprocess, sys
root = pathlib.Path(sys.argv[1])
twins = {t: (root / f"tests/labs/AC4/lab-AC4-{t}-1.py").read_text(encoding="utf-8").splitlines() for t in ("L07", "L08")}
ref = {}
for t, p in ((t, root / f"tests/labs/AC4/lab-AC4-{t}-1.py") for t in ("L07", "L08")):
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(p)], capture_output=True, text=True)
    ref[t] = (r.returncode, r.stdout)
files = sorted(p for d in sorted((root / "ledgers/AC4/mutants").glob("AC4-d-r*")) for p in d.glob("*.py"))
for f in files:
    mut = f.read_text(encoding="utf-8").splitlines()
    best = None
    for t in ("L07", "L08"):
        n = sum(1 for l in difflib.unified_diff(twins[t], mut, lineterm="") if l[:1] in "+-" and l[:3] not in ("+++", "---"))
        if best is None or n < best[1]:
            best = (t, n)
    t, n = best
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(f)], capture_output=True, text=True, timeout=120)
    killed = r.returncode != 0 or r.stdout != ref[t][1]
    print(f"{f.parent.name}/{f.name} | twin {t} | changed-lines-vs-current {n} | exit {r.returncode} | output_differs {r.stdout != ref[t][1]} | {'KILLED' if killed else 'SURVIVED'}")
