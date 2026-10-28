"""For each slice lesson page, compare the embedded data-run code block with its lab twin byte-for-byte.

Usage: python -I embed_match.py <checkout> <page ids...>  (read-only)
"""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
for page in sys.argv[2:]:
    text = (root / "course/modules/M/M2" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    embedded = html.unescape(m.group(1)) if m else None
    twin = (root / f"tests/labs/M2/lab-M2-{page}-1.py").read_text(encoding="utf-8")
    print(f"{page}: {'IDENTICAL' if embedded == twin else 'DIFFERENT'} (embedded {len(embedded or '')} chars, twin {len(twin)} chars)")
