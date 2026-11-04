"""LX1-c round 2: internal links, rubric descriptor scan, round-1 mutants m05 and m10 against the current page."""
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))
P = ROOT / "course/modules/LX/LX1/project.html"
t = P.read_text(encoding="utf-8")
ids = set(re.findall(r'\sid="([^"]+)"', t))
bad = []
for href in re.findall(r'href="([^"]+)"', t):
    if href.startswith("#"):
        if href[1:] not in ids:
            bad.append(href)
    elif href.startswith("http"):
        continue
    else:
        path, _, frag = href.partition("#")
        full = (P.parent / path).resolve() if path else P
        if not full.exists():
            bad.append(href + " (missing file)")
            continue
        if frag and path.endswith(".html") and f'id="{frag}"' not in full.read_text(encoding="utf-8"):
            bad.append(href + " (missing anchor)")
print("internal href problems:", bad or "none", "| ids in page:", len(ids))
for needle in ["Discusses similarities.", "Notes some caveats.", "holds one exchange rate per currency for each month",
               "(the 2 zero changes of Lab 3)", "MANIFEST note", "reinhart2009this", "spot"]:
    lines = [i + 1 for i, ln in enumerate(t.splitlines()) if needle in ln]
    print(f"{needle!r}: lines {lines}")
s = t.index('id="lab-LX1-project-2"')
seg = t[s:t.index("</section>", s)]
exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', seg, re.S).group(1))
for name in ["lx1c_m05_rung2_real_value_rounded_before_burden.py", "lx1c_m10_lab3_blank_cell_skipped.py"]:
    wd = tempfile.mkdtemp(prefix="lx1c-r2-struct-")
    os.makedirs(os.path.join(wd, "data"))
    shutil.copy(ROOT / "course/assets/data/market/fx_monthly.csv", os.path.join(wd, "data", "fx_monthly.csv"))
    shutil.copy(ROOT / "ledgers/LX1/mutants" / name, os.path.join(wd, "m.py"))
    p = subprocess.run([sys.executable, "-I", "-W", "error", "m.py"], cwd=wd, capture_output=True, text=True)
    if name.startswith("lx1c_m05"):
        print(name, "rc", p.returncode, "differs from rung-2 expected block:", p.stdout.rstrip() != exp.rstrip())
    else:
        print(name, "rc", p.returncode, "(on the real snapshot no blank exists; the blank-input test is in labs_r2.out E1)")
    shutil.rmtree(wd)
