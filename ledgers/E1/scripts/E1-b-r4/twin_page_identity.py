"""Round 4 check: each lesson page's embedded lab code and expected output equal the twin file and its run output.

Run as: .venv/bin/python -I ledgers/E1/scripts/E1-b-r4/twin_page_identity.py  (from the checkout root)
"""

import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(".")
for lesson in ("L04", "L05", "L06"):
    page = (ROOT / f"course/modules/E/E1/{lesson}.html").read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)).strip()
    twin_path = ROOT / f"tests/labs/E1/lab-E1-{lesson}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, check=False
    )
    print(lesson, "page code == twin:", code.strip() == twin.strip(), "| exit", run.returncode,
          "| run output == embedded:", run.stdout.strip() == expected)
