"""Compare each project.html lab code block with its twin, and each expected block with the twin's output.

Usage: lab_equal.py  (run from the verifier checkout root). Prints one line per lab.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
page = (ROOT / "course/modules/CS/CS2/project.html").read_text(encoding="utf-8")
sections = re.findall(r'<section class="lab[^"]*" id="(lab-CS2-project-\d)".*?</section>', page, re.S)
for lab_id in sections:
    block = re.search(r'id="%s".*?</section>' % lab_id, page, re.S).group(0)
    code = html.unescape(re.search(r"<code[^>]*data-run>(.*?)</code>", block, re.S).group(1))
    twin = (ROOT / "tests/labs/CS2" / f"{lab_id.replace('lab-', 'lab-')}.py").read_text(encoding="utf-8")
    expected_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', block, re.S)
    expected = html.unescape(expected_m.group(1)).rstrip("\n") if expected_m else None
    same = code.strip() == twin.strip()
    blanks = code.count("___")
    res = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / "tests/labs/CS2" / f"{lab_id}.py")],
                         capture_output=True, text=True)
    out = res.stdout.rstrip("\n")
    print(f"{lab_id}: code==twin {same}; blanks in page code {blanks}; twin rc={res.returncode}; "
          f"expected==output {expected == out}; expected lines {len(expected.splitlines()) if expected else None}")
    if not same:
        import difflib
        for line in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm=""))[:20]:
            print("   ", line)
