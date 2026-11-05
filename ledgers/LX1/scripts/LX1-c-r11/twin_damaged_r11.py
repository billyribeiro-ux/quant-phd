"""Round-11 verifier: runs the lab 3 twin alone on three damaged copies of the snapshot (blank GBP cell, non-decimal
GBP cell, removed month) and reports rc, stderr last line and whether stdout is empty. Argument 1 is the checkout root."""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path
root = Path(sys.argv[1])
PY = str(root / ".venv/bin/python")
TWIN = root / "tests/labs/LX1/lab-LX1-project-3.py"
lines = (root / "course/assets/data/market/fx_monthly.csv").read_text(encoding="utf-8").splitlines()
gi = lines[0].split(",").index("GBP")
def with_cell(value):
    out = []
    for l in lines:
        f = l.split(",")
        if f[0] == "2000-06":
            f[gi] = value
        out.append(",".join(f))
    return out
variants = {
    "blank": with_cell(""),
    "non_decimal": with_cell("n/a"),
    "gap": [l for l in lines if not l.startswith("1990-06,")],
}
for name, ls in variants.items():
    wd = tempfile.mkdtemp(prefix="r11dmg-")
    try:
        os.makedirs(f"{wd}/data")
        Path(f"{wd}/data/fx_monthly.csv").write_text("\n".join(ls) + "\n", encoding="utf-8")
        shutil.copy(TWIN, f"{wd}/lab.py")
        p = subprocess.run([PY, "-I", "-W", "error", f"{wd}/lab.py"], cwd=wd, capture_output=True, text=True)
        print(f"{name}: rc={p.returncode} stdout_empty={p.stdout == ''} stderr_last={p.stderr.strip().splitlines()[-1:]}")
    finally:
        shutil.rmtree(wd)
