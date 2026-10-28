"""Verifier round 2: embedded data-run code equals the twin up to the final newline (python -I; read-only).

Usage: python -I embed_match_r2.py <checkout> <page ids...>
"""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
for page in sys.argv[2:]:
    text = (root / "course/modules/M/M2" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    e = html.unescape(m.group(1))
    w = (root / f"tests/labs/M2/lab-M2-{page}-1.py").read_text(encoding="utf-8")
    print(page, "equal-up-to-final-newline:", e.rstrip("\n") == w.rstrip("\n"), "exact-with-one-newline:", e + "\n" == w)
