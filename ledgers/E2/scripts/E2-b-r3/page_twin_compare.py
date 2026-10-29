"""E2 slice b (L04-L06), round 3: page lab code equals its twin, and the expected block equals the twin's output.

Run as: python3 -I page_twin_compare.py (from the checkout root, which is four levels up from this file).
Trailing newlines are ignored (the page stores the code without the final newline)."""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = ROOT / "course" / "modules" / "E" / "E2"
TWINS = ROOT / "tests" / "labs" / "E2"
for n in ("04", "05", "06"):
    page = (PAGES / f"L{n}.html").read_text(encoding="utf-8")
    code_block = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(code_block.group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1))
    twin = (TWINS / f"lab-E2-L{n}-1.py").read_text(encoding="utf-8")
    assert code.rstrip("\n") == twin.rstrip("\n"), f"L{n}: page code differs from twin"
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(TWINS / f"lab-E2-L{n}-1.py")],
        capture_output=True,
        text=True,
        check=True,
    )
    assert expected.rstrip("\n") == run.stdout.rstrip("\n"), f"L{n}: expected block differs from output"
    print(
        f"L{n}: page code == twin ({len(twin)} bytes); expected block == twin output "
        f"({len(run.stdout.splitlines())} lines); twin ends with main(): {twin.rstrip().endswith('main()')}"
    )
print("page_twin_compare: PASS")
