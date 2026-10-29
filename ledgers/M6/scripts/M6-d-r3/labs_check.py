"""For project.html: compare each lab's page code with its twin, run the twin alone (python -I -W error), compare its output with the expected block."""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

REPO = Path("/Users/billyribeiro/.fanout/wt/verifyC3-M6-d")
page = (REPO / "course/modules/M/M6/project.html").read_text(encoding="utf-8")
sections = re.findall(r'<section class="lab[^"]*" id="(lab-M6-project-\d)".*?</section>', page, flags=re.S)
for lab_id in sections:
    block = re.search(rf'id="{lab_id}".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, flags=re.S)
    code = html.unescape(block.group(1))
    expected = html.unescape(block.group(2)).rstrip("\n")
    twin_path = REPO / "tests/labs/M6" / f"{lab_id.replace('lab-', 'lab-')}.py"
    twin = twin_path.read_text(encoding="utf-8")
    same = code.strip() == twin.strip()
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, check=False)
    got = out.stdout.rstrip("\n")
    print(f"{lab_id}: twin_exit={out.returncode} page_code_equals_twin={same} expected_equals_output={got == expected} stderr={out.stderr.strip()[:200]!r}")
    if got != expected:
        print("EXPECTED:", expected[:400]); print("GOT:", got[:400])
    if not same:
        import difflib
        print("\n".join(list(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm=""))[:30]))
