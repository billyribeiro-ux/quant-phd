"""Compare each M6 lesson's code block and expected block with its lab twin and the twin's output.

Run from the checkout root: .venv/bin/python ledgers/M6/scripts/M6-a-r8/page_vs_twin_r8.py
"""

import re
import subprocess
import sys
from pathlib import Path

root = Path.cwd()
for n in ("01", "02", "03", "04"):
    page = (root / f"course/modules/M/M6/L{n}.html").read_text(encoding="utf-8")
    twin = (root / f"tests/labs/M6/lab-M6-L{n}-1.py").read_text(encoding="utf-8")
    codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    import html

    code_eq = [html.unescape(c).strip() == twin.strip() for c in codes]
    out = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M6/lab-M6-L{n}-1.py")],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    exp_eq = [html.unescape(e).strip() == out.strip() for e in expected]
    print(f"L{n}: code blocks={len(codes)} equal_twin={code_eq} expected blocks={len(expected)} equal_output={exp_eq}")
