"""Run copies of the L03 lab with E2 (INFLATION 0.00) and E3 (REAL_RATE 0.10) under python -I -W error."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
src = (ROOT / "tests/labs/CF1/lab-CF1-L03-1.py").read_text(encoding="utf-8")
cases = {"E2": ("INFLATION = 0.03", "INFLATION = 0.00"), "E3": ("REAL_RATE = 0.06", "REAL_RATE = 0.10")}
for name, (old, new) in cases.items():
    assert src.count(old) == 1, name
    copy = OUT / f"copy_{name}.py"
    copy.write_text(src.replace(old, new), encoding="utf-8")
    run = subprocess.run([str(ROOT / ".venv/bin/python"), "-I", "-W", "error", str(copy)], capture_output=True, text=True)
    print(name, "exit", run.returncode, "stderr", repr(run.stderr[:100]))
    for line in run.stdout.splitlines():
        if line.startswith(("real rate", "NPV real flows at nominal rate", "mixed minus real", "largest absolute gap", "0.00  ")):
            print("   ", line)
