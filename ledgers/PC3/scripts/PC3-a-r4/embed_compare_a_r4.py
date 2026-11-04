"""Round-4 verifier: compare each slice lab's page code and expected block with its twin.

Page code: text inside the <code data-run> element, HTML-unescaped. Twin: the file text.
Expected block: the <pre class="expected"> text, HTML-unescaped, compared with the twin's stdout.
Usage (from checkout root): python -I <this file>
"""
from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
PAGES = {"L01": "course/modules/PC/PC3/L01.html", "L02": "course/modules/PC/PC3/L02.html", "L03": "course/modules/PC/PC3/L03.html"}
for page, rel in PAGES.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    twin = (ROOT / f"tests/labs/PC3/lab-PC3-{page}-1.py").read_text(encoding="utf-8")
    code = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    assert code and exp, page
    page_code = html.unescape(code.group(1))
    expected = html.unescape(exp.group(1))
    print(f"{page}: page code == twin: {page_code.rstrip() == twin.rstrip()} (page {len(page_code)} chars, twin {len(twin)} chars)")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/PC3/lab-PC3-{page}-1.py")], capture_output=True, text=True)
    print(f"{page}: twin exit={run.returncode} stderr_bytes={len(run.stderr.encode())}")
    print(f"{page}: expected block == stdout: {expected.rstrip() == run.stdout.rstrip()} (stdout lines {run.stdout.count(chr(10))})")
    # per-line diffs, if any
    if expected.rstrip() != run.stdout.rstrip():
        for a, b in zip(expected.splitlines(), run.stdout.splitlines()):
            if a != b:
                print("  DIFF expected:", a, "| stdout:", b)
    print(f"{page}: expected block marker tolerance:", re.search(r'<pre class="expected"([^>]*)>', text).group(1).strip())
    print(f"{page}: lab section count:", len(re.findall(r'<section class="lab"', text)), "; data-files attrs:", len(re.findall(r'data-files', text)))
