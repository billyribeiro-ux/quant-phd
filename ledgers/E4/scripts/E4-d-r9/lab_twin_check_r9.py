"""For each project lab: the page's code block equals the twin (line by line, Lab 2 differs only at the blank), the twin
runs under python -I -W error, and its output equals the page's expected block.

Run: python3 -I lab_twin_check_r9.py <repo-root>
"""
import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/E/E4/project.html").read_text(encoding="utf-8")
py = str(root / ".venv/bin/python")
for n in (1, 2, 3):
    lab_id = f"lab-E4-project-{n}"
    sec = re.search(rf'<section[^>]*id="{lab_id}".*?</section>', page, re.S).group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin_path = root / "tests/labs/E4" / f"{lab_id}.py"
    twin = twin_path.read_text(encoding="utf-8")
    diff = [l for l in difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm="", n=0)
            if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    print(f"{lab_id}: page code lines {len(code.splitlines())}, twin lines {len(twin.splitlines())}, differing lines {len(diff)}")
    for l in diff[:8]:
        print("   ", l)
    r = subprocess.run([py, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True)
    out = r.stdout.rstrip("\n")
    print(f"  twin exit {r.returncode}, stderr {len(r.stderr)} bytes; output equals expected block: {out == expected.rstrip(chr(10))}")
    if out != expected.rstrip("\n"):
        for l in difflib.unified_diff(expected.splitlines(), out.splitlines(), lineterm="", n=0):
            print("   ", l)
