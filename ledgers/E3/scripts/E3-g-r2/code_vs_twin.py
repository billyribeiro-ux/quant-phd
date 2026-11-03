"""Compare the code block of each L05-L08 lab page with its twin source (html-unescaped, whitespace-normalised)."""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
for lesson in ("L05", "L06", "L07", "L08"):
    twin = (root / "tests/labs/E3" / f"lab-E3-{lesson}-1.py").read_text(encoding="utf-8")
    page = (root / "course/modules/E/E3" / f"{lesson}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    norm = lambda s: [ln.rstrip() for ln in s.strip("\n").splitlines()]
    same = norm(code) == norm(twin)
    print(f"{lesson}: page code == twin: {same} (page lines {len(norm(code))}, twin lines {len(norm(twin))})")
    if not same:
        import difflib
        for d in list(difflib.unified_diff(norm(twin), norm(code), lineterm=""))[:20]:
            print("  ", d)
