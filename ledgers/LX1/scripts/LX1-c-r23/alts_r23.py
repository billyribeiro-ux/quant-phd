"""Round 23 (LX1-c): runs the five alternative correct implementations (ledgers/LX1/scripts/LX1-c-r20/alts/) and
compares each stdout with the page's expected block for its lab. Usage: python -I alts_r23.py <repo_root> <scratch>"""
import html
import re
import shutil
import subprocess
import sys
from pathlib import Path

root, scratch = Path(sys.argv[1]), Path(sys.argv[2])
page = (root / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
expected = [html.unescape(x).rstrip("\n") for x in re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)]
(scratch / "data").mkdir(parents=True, exist_ok=True)
shutil.copy(root / "course/assets/data/market/fx_monthly.csv", scratch / "data" / "fx_monthly.csv")
for f in sorted((root / "ledgers/LX1/scripts/LX1-c-r20/alts").glob("*.py")):
    lab = int(re.search(r"lab(\d)", f.name).group(1))
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(f)], capture_output=True, text=True, cwd=str(scratch), timeout=120)
    same = run.stdout.rstrip("\n") == expected[lab - 1]
    print(f"{f.name}: rc={run.returncode} stdout==expected {same} -> {'PASS' if run.returncode == 0 and same else 'DIFFERS'}")
