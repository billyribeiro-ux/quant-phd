"""LX1-c round 20: runs the three new student-error mutants and the five alternative correct implementations, each under
python -I -W error in a scratch dir with data/fx_monthly.csv, against the expected block of the lab named in its file name."""
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
files = sorted((root / "ledgers/LX1/mutants").glob("lx1c_r20n0*.py")) + sorted((root / "ledgers/LX1/scripts/LX1-c-r20/alts").glob("alt*.py"))
for f in files:
    lab = int(re.search(r"lab(\d)", f.name).group(1))
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(f)], capture_output=True, text=True, cwd=str(scratch), timeout=120)
    same = run.stdout.rstrip("\n") == expected[lab - 1]
    kind = "MUTANT" if "mutants" in str(f) else "ALT"
    verdict = ("KILLED" if (run.returncode != 0 or not same) else "SURVIVED") if kind == "MUTANT" else ("PASSES(expected)" if (run.returncode == 0 and same) else "FAILS(over-constraint?)")
    print(f"{kind} lab{lab} {f.name}: rc={run.returncode} stdout==expected {same} -> {verdict}"
          + (f" stderr_tail={run.stderr.strip().splitlines()[-1:]}" if run.returncode else ""))
