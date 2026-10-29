"""Compare each E3 L04-L06 lab page: embedded code == twin file, expected block == twin stdout (python -I -W error)."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
for n in ("04", "05", "06"):
    page = (ROOT / f"course/modules/E/E3/L{n}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = (ROOT / f"tests/labs/E3/lab-E3-L{n}-1.py").read_text(encoding="utf-8")
    print(f"L{n}: embedded code == twin: {code.rstrip() == twin.rstrip()} (page {len(code)} chars, twin {len(twin)} chars)")
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1)).rstrip()
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/E3/lab-E3-L{n}-1.py")],
                         capture_output=True, text=True, cwd="/tmp").stdout.rstrip()
    print(f"L{n}: expected block == twin stdout: {expected == out}")
    if expected != out:
        import difflib
        for line in difflib.unified_diff(expected.splitlines(), out.splitlines(), lineterm=""):
            print("   ", line)
