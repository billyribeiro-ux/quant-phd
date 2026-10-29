"""Check each page's data-run code block equals its lab twin source (AC1 slice b)."""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
for n in ("L04", "L05", "L06"):
    page = (root / f"course/modules/AC/AC1/{n}.html").read_text(encoding="utf-8")
    m = re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S)
    code = html.unescape(m.group(1))
    twin = (root / f"tests/labs/AC1/lab-AC1-{n}-1.py").read_text(encoding="utf-8")
    print(n, "code_block_equals_twin", code == twin, "len", len(code), len(twin))
