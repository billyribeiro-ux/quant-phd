"""Round-2 check for CS2 slice c: page code block equals twin file; expected block equals run output (python -I -W error)."""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = {
    "L09": ("course/modules/CS/CS2/L09.html", "tests/labs/CS2/lab-CS2-L09-1.py"),
    "L10": ("course/modules/CS/CS2/L10.html", "tests/labs/CS2/lab-CS2-L10-1.py"),
    "L11": ("course/modules/CS/CS2/L11.html", "tests/labs/CS2/lab-CS2-L11-1.py"),
}

for page, (html_rel, twin_rel) in PAGES.items():
    text = (ROOT / html_rel).read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    twin = (ROOT / twin_rel).read_text(encoding="utf-8")
    page_code = html.unescape(code.group(1))
    exp_block = html.unescape(expected.group(1))
    print(f"== {page}: page code == twin: {page_code == twin}; equal after stripping the final newline "
          f"(embed_labs.py strips it, line 117): {page_code.rstrip(chr(10)) == twin.rstrip(chr(10))}")
    proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(ROOT / twin_rel)],
        capture_output=True,
        text=True,
        cwd="/tmp",
        timeout=120,
    )
    print(f"   exit={proc.returncode} stderr={proc.stderr.strip()!r}")
    out = proc.stdout
    print(f"   expected block == run output: {out.rstrip() == exp_block.rstrip()}")
    if out.rstrip() != exp_block.rstrip():
        print("   OUTPUT:\n" + out)
        print("   EXPECTED:\n" + exp_block)
    print("   OUTPUT LINES:")
    for line in out.splitlines():
        print("     " + line)
