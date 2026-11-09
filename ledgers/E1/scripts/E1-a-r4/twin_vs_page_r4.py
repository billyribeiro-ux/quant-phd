"""Compare each slice-a lab page with its twin and its expected block with the twin's stdout (round 4)."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
for lid in ("L01", "L02", "L03"):
    page = (ROOT / f"course/modules/E/E1/{lid}.html").read_text(encoding="utf-8")
    twin = (ROOT / f"tests/labs/E1/lab-E1-{lid}-1.py").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(exp.group(1))
    out = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/E1/lab-E1-{lid}-1.py")],
        capture_output=True, text=True, check=False,
    ).stdout
    print(lid, "page code == twin:", code.strip() == twin.strip(),
          "| expected == stdout:", expected.strip() == out.strip(),
          "| page code bytes:", len(code), "twin bytes:", len(twin))
