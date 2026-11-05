"""Round-11 verifier: runs every alternative correct implementation of the project labs (kept scripts from rounds 9-10
and the round-11 numpy alternative) alone under python -I -W error in a scratch directory holding data/fx_monthly.csv,
and compares its stdout with the expected block of the matching project lab on the page. Argument 1 is the checkout root."""
import html, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path
root = Path(sys.argv[1]).resolve()
PY = str(root / ".venv/bin/python")
page = (root / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
blocks = [html.unescape(b).rstrip("\n") for b in re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)]
ALTS = [
    ("ledgers/LX1/scripts/LX1-c-r10/v9_alt_lab1_float_and_lab2_ratio.py", 0),
    ("ledgers/LX1/scripts/LX1-c-r10/v9_alt_lab2_check.py", 1),
    ("ledgers/LX1/scripts/LX1-c-r10/v10_alt2float_lab2.py", 1),
    ("ledgers/LX1/scripts/LX1-c-r10/v9_alt_lab3_welford_and_log1p.py", 2),
    ("ledgers/LX1/scripts/LX1-c-r11/alt_lab3_numpy_ddof1.py", 2),
]
for rel, idx in ALTS:
    wd = tempfile.mkdtemp(prefix="r11alt-")
    try:
        os.makedirs(f"{wd}/data")
        shutil.copy(root / "course/assets/data/market/fx_monthly.csv", f"{wd}/data/fx_monthly.csv")
        p = subprocess.run([PY, "-I", "-W", "error", str(root / rel)], cwd=wd, capture_output=True, text=True)
        same = p.returncode == 0 and p.stdout.rstrip("\n") == blocks[idx]
        print(f"{rel}: rc={p.returncode} stderr_empty={p.stderr == ''} matches_project_lab_{idx+1}={same}")
    finally:
        shutil.rmtree(wd)
