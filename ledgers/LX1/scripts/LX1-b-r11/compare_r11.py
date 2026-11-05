"""LX1-b round 11: compare each page's data-run code and expected block with its twin and with the twin's output.

Usage: python -I ledgers/LX1/scripts/LX1-b-r11/compare_r11.py <checkout> <outdir>
"""

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
pairs = {
    "L03": (root / "course/modules/LX/LX1/L03.html", root / "tests/labs/LX1/lab-LX1-L03-1.py", out / "twin_L03.out"),
    "L04": (root / "course/modules/LX/LX1/L04.html", root / "tests/labs/LX1/lab-LX1-L04-1.py", out / "twin_L04.out"),
}
ok = True
for lesson, (page, twin, twin_out) in pairs.items():
    text = page.read_text(encoding="utf-8")
    runs = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    print(f"{lesson}: data-run blocks={len(runs)} expected blocks={len(expected)}")
    code = html.unescape(runs[0])
    twin_src = twin.read_text(encoding="utf-8")
    same = code.rstrip("\n") == twin_src.rstrip("\n")
    print(f"{lesson}: page code equals twin source (ignoring trailing newline): {same}")
    if not same:
        ok = False
        import difflib

        for line in difflib.unified_diff(twin_src.splitlines(), code.splitlines(), "twin", "page", lineterm=""):
            print("   ", line)
    exp = html.unescape(expected[0]).rstrip("\n")
    actual = twin_out.read_text(encoding="utf-8").rstrip("\n")
    eq = exp == actual
    print(f"{lesson}: expected block equals twin stdout: {eq}")
    if not eq:
        ok = False
        import difflib

        for line in difflib.unified_diff(actual.splitlines(), exp.splitlines(), "actual", "expected", lineterm=""):
            print("   ", line)
    # Numbers printed by the twin must match the expected block token for token.
    print(f"{lesson}: twin stdout lines={len(actual.splitlines())} expected lines={len(exp.splitlines())}")
print("ALL EQUAL" if ok else "MISMATCH")
