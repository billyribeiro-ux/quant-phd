"""Compare each L08-L10 page's lab code and expected block with its twin and the twin's observed output.

Usage: python -I check_twin_match.py <checkout-root>
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for lesson in ("L08", "L09", "L10"):
    page = (root / "course/modules/M/M4" / f"{lesson}.html").read_text(encoding="utf-8")
    codes = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    twin = (root / "tests/labs/M4" / f"lab-M4-{lesson}-1.py").read_text(encoding="utf-8")
    out = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(root / "tests/labs/M4" / f"lab-M4-{lesson}-1.py")],
        capture_output=True, text=True, cwd="/tmp",
    ).stdout
    code_ok = len(codes) == 1 and html.unescape(codes[0]).strip() == twin.strip()
    exp_ok = len(expected) == 1 and html.unescape(expected[0]).strip() == out.strip()
    print(f"{lesson}: blocks={len(codes)} code_equals_twin={code_ok} expected_blocks={len(expected)} expected_equals_output={exp_ok} output_lines={len(out.splitlines())}")
    if not exp_ok and expected:
        a = html.unescape(expected[0]).strip().splitlines()
        b = out.strip().splitlines()
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                print(f"  first diff line {i + 1}:\n   page:  {x!r}\n   twin:  {y!r}")
                break
