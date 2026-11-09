"""Compare each M7 project lab's code on project.html with its twin, and run each twin alone; compare the printed output
with the page's expected block (exact text, after HTML unescape).

Usage: python -I labs_page_vs_twin_M7d_r12.py <repo_root>
"""

import html
import re
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
page = (repo / "course/modules/M/M7/project.html").read_text(encoding="utf-8")
python = repo / ".venv/bin/python"
for lab in ("lab-M7-project-1", "lab-M7-project-2", "lab-M7-project-3"):
    m = re.search(rf'<section class="lab[^"]*" id="{lab}".*?</section>', page, re.S)
    section = m.group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', section, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section, re.S).group(1))
    twin = (repo / f"tests/labs/M7/{lab}.py").read_text(encoding="utf-8")
    same = code.rstrip(chr(10)) == twin.rstrip(chr(10))
    print(f"{lab}: page code == twin: {same}")
    if not same:
        import difflib
        for line in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""):
            print("   ", line)
    run = subprocess.run([str(python), "-I", "-W", "error", str(repo / f"tests/labs/M7/{lab}.py")],
                         capture_output=True, text=True, cwd="/tmp")
    out = run.stdout.rstrip("\n")
    print(f"{lab}: twin exit {run.returncode}; stderr {run.stderr.strip()[:200]!r}")
    print(f"{lab}: output == expected block: {out == expected.rstrip(chr(10))}")
    if out != expected.rstrip("\n"):
        print("  OUTPUT:\n" + out)
        print("  EXPECTED:\n" + expected)
