"""Compare each lab's page code block with its twin, and each expected block with the twin's stdout (LX1-b r17)."""
import html
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = ROOT / "ledgers/LX1/scripts/LX1-b-r17/out"
pairs = [("L01", "lab-LX1-L01-1"), ("L03", "lab-LX1-L03-1"), ("L04", "lab-LX1-L04-1")]
for page, lab in pairs:
    text = (ROOT / f"course/modules/LX/LX1/{page}.html").read_text(encoding="utf-8")
    code = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    twin = (ROOT / f"tests/labs/LX1/{lab}.py").read_text(encoding="utf-8")
    stdout = (OUT / f"twin_{page}.stdout").read_text(encoding="utf-8")
    print(page, "code blocks:", len(code), "expected blocks:", len(expected))
    c = html.unescape(code[0])
    print(" page code == twin:", c.rstrip("\n") == twin.rstrip("\n"), len(c), len(twin))
    e = html.unescape(expected[0])
    print(" expected == twin stdout:", e.rstrip("\n") == stdout.rstrip("\n"))
    if e.rstrip("\n") != stdout.rstrip("\n"):
        import difflib
        print("".join(difflib.unified_diff(e.splitlines(True), stdout.splitlines(True), "page", "twin")))
