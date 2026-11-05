"""Compare each LX1-b page's lab code and expected block with its twin and with the live twin output.

Usage: python3 -I compare_pages_twins.py <checkout> <outdir>
Reads only files inside the checkout; prints PASS/FAIL lines.
"""
import html
import re
import sys
from pathlib import Path

checkout = Path(sys.argv[1])
outdir = Path(sys.argv[2])
ok = True
for page, twin in (("L03", "lab-LX1-L03-1.py"), ("L04", "lab-LX1-L04-1.py")):
    text = (checkout / "course/modules/LX/LX1" / f"{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    twin_src = (checkout / "tests/labs/LX1" / twin).read_text(encoding="utf-8")
    page_code = html.unescape(code.group(1))
    same_code = page_code.rstrip("\n") == twin_src.rstrip("\n")
    exp = html.unescape(expected.group(1))
    live = (outdir / f"twin_{page}.out").read_text(encoding="utf-8")
    same_exp = exp.rstrip("\n") == live.rstrip("\n")
    print(f"{page}: page code == twin (modulo trailing newline): {same_code}; "
          f"expected block == live twin output: {same_exp}; "
          f"expected lines {len(exp.splitlines())}, live lines {len(live.splitlines())}")
    ok = ok and same_code and same_exp
    if not same_code:
        import difflib
        print("\n".join(difflib.unified_diff(twin_src.splitlines(), page_code.splitlines(), lineterm="")))
    if not same_exp:
        import difflib
        print("\n".join(difflib.unified_diff(live.splitlines(), exp.splitlines(), lineterm="")))
print("RESULT", "PASS" if ok else "FAIL")
