"""Compare the embedded lab code in each page with its twin file (byte-level, after HTML unescape)."""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
pairs = [
    ("course/modules/AC/AC2/L03.html", "tests/labs/AC2/lab-AC2-L03-1.py"),
    ("course/modules/AC/AC2/L04.html", "tests/labs/AC2/lab-AC2-L04-1.py"),
]
for page, twin in pairs:
    text = (root / page).read_text(encoding="utf-8")
    m = re.search(r'<code class="language-python" data-run>(.*?)</code>', text, re.S)
    code = html.unescape(m.group(1))
    tw = (root / twin).read_text(encoding="utf-8")
    print(page, "embedded_len", len(code), "twin_len", len(tw), "identical_modulo_final_newline", code + "\n" == tw)
    if code + "\n" != tw:
        import difflib
        for line in list(difflib.unified_diff(tw.splitlines(), code.splitlines(), "twin", "page", lineterm=""))[:40]:
            print(line)
    out = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    print("expected_block_lines", len(html.unescape(out.group(1)).splitlines()))
