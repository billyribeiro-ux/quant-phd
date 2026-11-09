"""LX1-b round 16: page code blocks equal twins byte for byte; page expected blocks equal twin stdout (run alone).

Run: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r16/compare_r15.py <checkout>
Requires out/twin_L03.out and out/twin_L04.out from gates_r15.sh (run alone under -I -W error).
"""

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = root / "ledgers/LX1/scripts/LX1-b-r16/out"
for page, twin in (("L03", "lab-LX1-L03-1"), ("L04", "lab-LX1-L04-1"), ("L01", "lab-LX1-L01-1")):
    text = (root / f"course/modules/LX/LX1/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin_src = (root / f"tests/labs/LX1/{twin}.py").read_text(encoding="utf-8")
    print(f"{page} page data-run code equals twin source: {code == twin_src} (page {len(code)} chars, twin {len(twin_src)} chars)")
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    print(f"{page} expected block line count: {expected.count(chr(10)) + 1}")
    if (out / f"twin_{page}.out").exists():
        got = (out / f"twin_{page}.out").read_text(encoding="utf-8")
        print(f"{page} expected block equals twin stdout (run alone): {expected.rstrip() == got.rstrip()}")
    # embedded line count and placement of the code block
    print(f"{page} code block line numbers:", text[: m.start()].count("\n") + 1, "to", text[: m.end()].count("\n") + 1)

# Trailing-newline check: the embed convention ends the page code with "main()" and no newline before </code>.
for page, twin in (("L03", "lab-LX1-L03-1"), ("L04", "lab-LX1-L04-1"), ("L01", "lab-LX1-L01-1")):
    text = (root / f"course/modules/LX/LX1/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    src = (root / f"tests/labs/LX1/{twin}.py").read_text(encoding="utf-8")
    print(f"{page} code equals twin modulo the final newline: {code.rstrip(chr(10)) == src.rstrip(chr(10))}; "
          f"code + newline == twin: {code + chr(10) == src}")
