"""For each project lab: compare the page's code block with its twin, run the twin under python -I -W error,
and compare the output with the page's expected block. Usage: python -I project_labs_check.py <repo_root>"""

from __future__ import annotations

import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
page = (root / "course/modules/CS/CS2/project.html").read_text(encoding="utf-8")
for lab in ("project-1", "project-2", "project-3"):
    sec = re.search(rf'<section[^>]*id="lab-CS2-{lab}".*?</section>', page, re.S).group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin_path = root / f"tests/labs/CS2/lab-CS2-{lab}.py"
    twin = twin_path.read_text(encoding="utf-8")
    same = code.strip() == twin.strip()
    print(f"== {lab}: page code == twin: {same}")
    if not same:
        for line in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""))[:40]:
            print("   ", line)
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True)
    out = run.stdout
    print(f"   twin exit {run.returncode}; stderr: {run.stderr.strip()[:200]!r}")
    print(f"   output == expected block: {out.strip() == expected.strip()}")
    if out.strip() != expected.strip():
        for line in list(difflib.unified_diff(expected.strip().splitlines(), out.strip().splitlines(), "expected", "output", lineterm=""))[:20]:
            print("   ", line)
