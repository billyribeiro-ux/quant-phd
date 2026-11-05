"""For each SC1 lesson page: the data-run code block equals the lab twin, and the expected block equals the twin's output.

Usage: python -I embed_check_r9.py <repo_root>
"""
import html
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
for n in range(1, 9):
    page = (root / f"course/modules/SC/SC1/L{n:02d}.html").read_text(encoding="utf-8")
    twins = sorted((root / "tests/labs/SC1").glob(f"lab-SC1-L{n:02d}-*.py"))
    runs = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    expects = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    for twin in twins:
        src = twin.read_text(encoding="utf-8")
        code_ok = any(html.unescape(r) == src or html.unescape(r).rstrip() == src.rstrip() for r in runs)
        out = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, check=False)
        got = out.stdout
        exp_ok = any(html.unescape(e).strip() == got.strip() for e in expects)
        print(f"L{n:02d} {twin.name}: code_in_page={code_ok} expected_in_page={exp_ok} exit={out.returncode} runs={len(runs)} expects={len(expects)}")
