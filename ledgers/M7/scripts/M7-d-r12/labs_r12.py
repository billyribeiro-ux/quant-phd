"""Compare each M7 project lab block on project.html with its twin, and run the twin under python -I -W error.

Usage: python -I -W error ledgers/M7/scripts/M7-d-r12/labs_r12.py <repo-root>
"""

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/M/M7/project.html").read_text(encoding="utf-8")
sections = re.findall(r'<section class="lab[^"]*" id="(lab-M7-project-\d)".*?<pre><code[^>]*>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
for lab_id, code, expected in sections:
    code_text = html.unescape(code)
    expected_text = html.unescape(expected)
    twin = root / "tests/labs/M7" / f"lab-M7-project-{lab_id[-1]}.py"
    twin_text = twin.read_text(encoding="utf-8")
    same = code_text.strip() == twin_text.strip()
    print(f"{lab_id}: page code == twin: {same} (page {len(code_text)} chars, twin {len(twin_text)} chars)")
    if not same:
        import difflib
        for line in list(difflib.unified_diff(twin_text.splitlines(), code_text.splitlines(), "twin", "page", lineterm=""))[:60]:
            print("   ", line)
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, check=False)
    print(f"{lab_id}: twin exit={out.returncode} stderr={out.stderr.strip()!r}")
    actual = out.stdout.rstrip("\n")
    print(f"{lab_id}: expected block == twin output: {actual == expected_text.strip()}")
    if actual != expected_text.strip():
        print("   expected:", expected_text.strip().splitlines()[:12])
        print("   actual  :", actual.splitlines()[:12])
