"""Compare each slice page's lab code and expected block with its twin and with the twin's live output (exact text)."""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1])
PAGES = {"L22": "lab-M2-L22-1", "L23": "lab-M2-L23-1", "L24": "lab-M2-L24-1"}
for page, lab in PAGES.items():
    text = (ROOT / f"course/modules/M/M2/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab"[^>]*id="%s".*?<pre><code[^>]*>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>' % lab, text, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin = (ROOT / f"tests/labs/M2/{lab}.py").read_text(encoding="utf-8")
    print(f"{page}: page code == twin (modulo trailing newline): {code.rstrip() == twin.rstrip()}")
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "twin.py"
        p.write_text(twin, encoding="utf-8")
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(p)], cwd=d, capture_output=True, text=True, timeout=120)
    print(f"{page}: twin exit={r.returncode} stderr={r.stderr!r}")
    out = r.stdout
    print(f"{page}: exact stdout == expected block: {out.rstrip() == expected.rstrip()}")
    if out.rstrip() != expected.rstrip():
        import difflib
        for line in difflib.unified_diff(expected.rstrip().splitlines(), out.rstrip().splitlines(), "expected", "live", lineterm=""):
            print("   ", line)
    print(f"{page}: LIVE OUTPUT")
    print(out)
