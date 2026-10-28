import subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
twin = (root / "tests/labs/AC4/lab-AC4-L08-1.py").read_text(encoding="utf-8").split("\n")
ref = subprocess.run([sys.executable, "-I", "-W", "error", str(root / "tests/labs/AC4/lab-AC4-L08-1.py")], capture_output=True, text=True).stdout
old = "if a.name < b.name:"
new = "if a.name <= b.name:"
idx = [i for i, l in enumerate(twin) if old in l]
print("twin lines containing guard:", [i + 1 for i in idx])
for i in idx:
    lines = list(twin); lines[i] = lines[i].replace(old, new)
    p = pathlib.Path("/tmp/AC4-d-v23/tie_transplant.py"); p.write_text("\n".join(lines), encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(p)], capture_output=True, text=True)
    print("exit", r.returncode, "output_differs", r.stdout != ref)
    if r.stdout != ref:
        import difflib
        print("\n".join(difflib.unified_diff(ref.split("\n"), r.stdout.split("\n"), lineterm="")))
    else:
        print("no output change: tie-guard removal is equivalent on the shipped seed")
