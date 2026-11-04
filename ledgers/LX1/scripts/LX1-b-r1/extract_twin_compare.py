"""Compare each lab twin with the data-run code block and expected block of its page (LX1 slice b, round 1)."""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
pairs = [
    ("course/modules/LX/LX1/L03.html", "tests/labs/LX1/lab-LX1-L03-1.py"),
    ("course/modules/LX/LX1/L04.html", "tests/labs/LX1/lab-LX1-L04-1.py"),
]
for page, twin in pairs:
    text = (root / page).read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin_text = (root / twin).read_text(encoding="utf-8")
    print(page, "code block chars", len(code), "twin chars", len(twin_text), "identical:", code == twin_text)
    if code != twin_text:
        import difflib
        for line in difflib.unified_diff(twin_text.splitlines(), code.splitlines(), "twin", "page", lineterm=""):
            print(line)
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    out = (root / "ledgers/LX1/scripts/LX1-b-r1" / (Path(twin).stem + ".expected.txt"))
    out.write_text(expected, encoding="utf-8")
    print(page, "expected block lines", len(expected.splitlines()))
