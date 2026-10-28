import subprocess, pathlib
ROOT = pathlib.Path("/tmp/verify17-CF1-b")
PY = str(ROOT / ".venv/bin/python")
src = (ROOT / "tests/labs/CF1/lab-CF1-L03-1.py").read_text(encoding="utf-8")
e2 = src.replace("INFLATION = 0.03\n", "INFLATION = 0.00\n", 1)
e3 = src.replace("REAL_RATE = 0.06\n", "REAL_RATE = 0.10\n", 1)
assert e2 != src and e3 != src
for name, text in (("E2", e2), ("E3", e3)):
    p = pathlib.Path("/tmp/cf1-v/CF1-b-r17/mut") / f"copy_{name}.py"
    p.write_text(text, encoding="utf-8")
    out = subprocess.run([PY, "-I", "-W", "error", str(p)], capture_output=True, text=True).stdout
    print("==", name)
    print(out)
