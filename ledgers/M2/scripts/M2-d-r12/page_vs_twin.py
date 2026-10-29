import html, re, sys
from pathlib import Path
root = Path(sys.argv[1])
for n in range(19, 25):
    page = (root / f"course/modules/M/M2/L{n}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    twin = (root / f"tests/labs/M2/lab-M2-L{n}-1.py").read_text(encoding="utf-8")
    print(f"L{n}: page code == twin: {code.strip() == twin.strip()} (page {len(code)} chars, twin {len(twin)} chars)")
