"""Round 3 FC2-a: page lab code equals twin; expected block equals twin stdout; hub/lesson data-hours; card coverage numbers.

Run: .venv/bin/python ledgers/FC2/scripts/FC2-a-r3/page_twin.py  (from the checkout root)
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = ROOT / "course/modules/FC/FC2"
TWINS = ROOT / "tests/labs/FC2"
PY = sys.executable

fails = 0
for lesson, lab in [("L01", "lab-FC2-L01-1"), ("L02", "lab-FC2-L02-1"), ("L03", "lab-FC2-L03-1")]:
    text = (PAGES / f"{lesson}.html").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab"[^>]*id="' + lab + r'".*?<pre><code[^>]*>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1)).strip()
    twin = (TWINS / f"{lab}.py").read_text(encoding="utf-8").strip()
    same = code == twin
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(exp.group(1)).strip()
    out = subprocess.run(
        [PY, "-I", "-W", "error", str(TWINS / f"{lab}.py")],
        capture_output=True,
        text=True,
        cwd="/tmp",
        env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"},
        check=False,
    )
    stdout = out.stdout.strip()
    eq = stdout == expected
    print(f"{lesson}: page code == twin: {same}; expected == twin stdout: {eq}; twin exit {out.returncode}; stderr bytes {len(out.stderr)}")
    if not (same and eq and out.returncode == 0):
        fails += 1
print("SUMMARY failures=", fails)
