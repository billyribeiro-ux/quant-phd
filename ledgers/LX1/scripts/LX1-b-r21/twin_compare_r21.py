"""Compare each LX1 slice-b lab block in a lesson page with its twin file and with the twin's stdout."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = ROOT / "ledgers/LX1/scripts/LX1-b-r21/out"
PAGES = {"L01": "course/modules/LX/LX1/L01.html", "L03": "course/modules/LX/LX1/L03.html", "L04": "course/modules/LX/LX1/L04.html"}
CODE = re.compile(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', re.S)
EXPECTED = re.compile(r'<pre class="expected"[^>]*>(.*?)</pre>', re.S)

for lesson, rel in PAGES.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    codes = CODE.findall(text)
    expected = EXPECTED.findall(text)
    twin = (ROOT / f"tests/labs/LX1/lab-LX1-{lesson}-1.py").read_text(encoding="utf-8")
    page_code = html.unescape(codes[0])
    print(f"{lesson}: code blocks {len(codes)}, expected blocks {len(expected)}")
    print(f"  page code == twin (exact): {page_code == twin}")
    print(f"  page code == twin (trailing newline stripped): {page_code.rstrip(chr(10)) == twin.rstrip(chr(10))}")
    print(f"  page code line count {page_code.count(chr(10))}, twin line count {twin.count(chr(10))}")
    stdout = (OUT / f"twin_{lesson}.out").read_text(encoding="utf-8").splitlines()
    if stdout and stdout[-1].startswith("exit "):
        stdout = stdout[:-1]
    exp_lines = html.unescape(expected[0]).rstrip("\n").splitlines()
    print(f"  expected lines {len(exp_lines)}, twin stdout lines {len(stdout)}")
    print(f"  expected == twin stdout: {exp_lines == stdout}")
    if exp_lines != stdout:
        for i, (a, b) in enumerate(zip(exp_lines, stdout)):
            if a != b:
                print(f"  first diff line {i + 1}: page={a!r} twin={b!r}")
                break
