import html, re, sys
from pathlib import Path
root = Path(sys.argv[1])
S = root / "ledgers/M4/scripts/M4-b-r9"
for L in ("L05", "L06", "L07"):
    page = (root / f"course/modules/M/M4/{L}.html").read_text()
    twin = (root / f"tests/labs/M4/lab-M4-{L}-1.py").read_text()
    out = (S / f"twin_{L}.out").read_text()
    blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code_ok = any(html.unescape(b).rstrip() == twin.rstrip() for b in blocks)
    exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    exp_ok = any(html.unescape(e).rstrip() == out.rstrip() for e in exp)
    print(L, "code_blocks", len(blocks), "code==twin", code_ok, "expected_blocks", len(exp), "expected==stdout", exp_ok)
