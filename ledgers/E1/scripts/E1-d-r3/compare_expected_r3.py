"""Compare each project lab's embedded <pre class="expected"> block with the output of its twin run.

Usage: .venv/bin/python ledgers/E1/scripts/E1-d-r3/compare_expected_r3.py <checkout>
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/E/E1/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<section class="lab[^"]*" id="(lab-E1-project-\d)".*?<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
for lab, expected in blocks:
    twin = root / "tests/labs/E1" / f"{lab}.py"
    out = subprocess.run([str(root / ".venv/bin/python"), "-I", "-W", "error", str(twin)],
                         capture_output=True, text=True, check=True).stdout
    want = html.unescape(expected).strip()
    got = out.strip()
    print(lab, "IDENTICAL" if want == got else "DIFFERENT")
    if want != got:
        for i, (w, g) in enumerate(zip(want.splitlines(), got.splitlines())):
            if w != g:
                print("  line", i + 1, "page:", w, "| run:", g)
