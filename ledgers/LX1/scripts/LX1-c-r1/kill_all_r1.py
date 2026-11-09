"""Round 23 (LX1-c): runs EVERY mutant in ledgers/LX1/mutants/ against its project lab twin's expected block, on the
embedded snapshot (scratch dir with a copy of data/fx_monthly.csv). The lab number comes from the file name (lab<n>,
rung<n>) or from the docstring ("project lab <n>" or "lab <n>"). Usage: python -I kill_all_r23.py <repo_root> <scratch>
Prints one line per mutant: KILLED (rc != 0 or stdout differs) or SURVIVED (rc 0 and stdout equal to expected)."""
import html
import json
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
results = []
for f in sorted((root / "ledgers/LX1/mutants").glob("*.py")):
    text = f.read_text(encoding="utf-8")
    head = "\n".join(text.splitlines()[:4])
    m = re.search(r"(?:lab|rung)(\d)", f.name) or re.search(r"(?:project lab|lab|rung) ?(\d)", head)
    if not m:
        results.append((f.name, None, "NO-LAB-MAPPING", ""))
        print(f"{f.name}: no lab mapping")
        continue
    lab = int(m.group(1))
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(f)], capture_output=True, text=True,
                         cwd=str(scratch), timeout=120)
    same = run.stdout.rstrip("\n") == expected[lab - 1]
    status = "KILLED" if (run.returncode != 0 or not same) else "SURVIVED"
    results.append((f.name, lab, status, f"rc={run.returncode}"))
    print(f"lab{lab} {f.name}: rc={run.returncode} stdout==expected {same} -> {status}")
json.dump(results, open(Path(__file__).with_name("kill_all_r1.json"), "w"), indent=1)
k = sum(1 for r in results if r[2] == "KILLED")
print(f"TOTAL mutants {len(results)}: killed on embedded snapshot {k}, survived {len(results) - k}")
