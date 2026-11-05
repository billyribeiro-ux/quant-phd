"""Round-9 check (M3 slice d): each project lab's page code equals its twin, and the expected block equals the twin's output.

Run from the checkout root with the checkout's interpreter: .venv/bin/python -I ledgers/M3/scripts/M3-d-r9/labs_twin_vs_page_r9.py
"""
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path.cwd()
PAGE = ROOT / "course/modules/M/M3/project.html"
text = PAGE.read_text(encoding="utf-8")
blocks = re.findall(r'<section class="lab[^"]*" id="(lab-M3-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
for lab_id, code_html, expected_html in blocks:
    code = html.unescape(code_html)
    expected = html.unescape(expected_html)
    twin = (ROOT / f"tests/labs/M3/{lab_id}.py").read_text(encoding="utf-8")
    same = code.strip() == twin.strip()
    print(f"{lab_id}: page code == twin: {same} (page {len(code)} chars, twin {len(twin)} chars)")
    if not same:
        import difflib
        for line in list(difflib.unified_diff(twin.strip().splitlines(), code.strip().splitlines(), "twin", "page", lineterm=""))[:60]:
            print("   ", line)
    res = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/M3/{lab_id}.py")], capture_output=True, text=True, cwd="/tmp")
    out = res.stdout.strip()
    print(f"{lab_id}: twin exit {res.returncode}; stderr {res.stderr.strip()[:200]!r}")
    print(f"{lab_id}: expected == output: {expected.strip() == out}")
    if expected.strip() != out:
        for a, b in zip(expected.strip().splitlines(), out.splitlines()):
            if a != b:
                print("   expected:", a)
                print("   output:  ", b)
print("blocks found:", len(blocks))
