"""Compare each project-page lab block with its twin, and run each twin alone under python -I -W error.

Usage: python -I lab_page_twin_check.py  (run from the checkout root)
Prints, per lab: the page code equals the twin (byte-for-byte after HTML unescape), the twin's exit status,
and whether the twin's stdout equals the page's expected block.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
page = (ROOT / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
blocks = re.findall(r'<section class="lab[^"]*" id="(lab-BK4-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, flags=re.S)
print("labs found on page:", [b[0] for b in blocks])
for lab_id, code_html, expected_html in blocks:
    code = html.unescape(code_html)
    expected = html.unescape(expected_html)
    n = lab_id[-1]
    twin_path = ROOT / f"tests/labs/BK4/lab-BK4-project-{n}.py"
    twin = twin_path.read_text(encoding="utf-8")
    same = code == twin
    print(f"{lab_id}: page code == twin: {same} (page {len(code)} chars, twin {len(twin)} chars)")
    if not same:
        import difflib
        for line in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm=""))[:20]:
            print("   ", line)
    result = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, check=False)
    print(f"{lab_id}: twin exit {result.returncode}, stderr {len(result.stderr)} chars")
    print(f"{lab_id}: twin stdout == page expected block: {result.stdout == expected + ('' if expected.endswith(chr(10)) else chr(10)) or result.stdout.rstrip(chr(10)) == expected.rstrip(chr(10))}")
