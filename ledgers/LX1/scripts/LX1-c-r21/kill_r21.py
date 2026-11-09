"""Round 21 (LX1-c): runs every project-lab mutant (r20 and r21 student-error files) and the r21 alternatives' check,
each under python -I -W error in a scratch dir with data/fx_monthly.csv, against the expected block of its lab.
Usage: python -I kill_r21.py <repo_root> <scratch_dir>"""
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
files = sorted((root / "ledgers/LX1/mutants").glob("lx1c_r2[01]n*.py"))
killed = 0
for f in files:
    m = re.search(r"lab(\d)", f.name)
    lab = int(m.group(1)) if m else None
    if lab is None:
        # project-lab mutants only; other early mutants are reviewed under earlier rounds
        continue
    if lab not in (1, 2, 3):
        continue
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(f)], capture_output=True, text=True, cwd=str(scratch), timeout=120)
    same = run.stdout.rstrip("\n") == expected[lab - 1]
    status = "KILLED" if (run.returncode != 0 or not same) else "SURVIVED"
    killed += status == "KILLED"
    print(f"lab{lab} {f.name}: rc={run.returncode} stdout==expected {same} -> {status}")
    if status == "KILLED" and run.returncode == 0:
        import difflib
        diff = list(difflib.unified_diff(expected[lab - 1].splitlines(), run.stdout.rstrip("\n").splitlines(), lineterm="", n=0))
        for line in diff[2:8]:
            print("     ", line)
print(f"killed {killed}/{len([f for f in files if re.search(r'lab([123])', f.name)])}")
