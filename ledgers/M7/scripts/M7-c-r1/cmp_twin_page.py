"""Compare each L07/L08 page's embedded lab code and expected block with its twin and with the twin's real output.

Run: python3 -I ledgers/M7/scripts/M7-c-r1/cmp_twin_page.py <checkout>
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for lid in ("L07", "L08"):
    page = (root / f"course/modules/M/M7/{lid}.html").read_text(encoding="utf-8")
    twin_path = root / f"tests/labs/M7/lab-M7-{lid}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(code_m.group(1))
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(exp_m.group(1))
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True)
    print(f"{lid}: page code == twin: {code == twin} ; equal after stripping the twin's final newline: {code == twin.rstrip(chr(10))} (page {len(code)} chars, twin {len(twin)} chars)")
    print(f"{lid}: expected == twin stdout: {expected.rstrip() == out.stdout.rstrip()}  exit={out.returncode}")
    if expected.rstrip() != out.stdout.rstrip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.splitlines(), out.stdout.splitlines(), lineterm="")))
    if code != twin:
        import difflib
        print("\n".join(list(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm=""))[:60]))
    print(f"{lid}: page code count of '@@' markers: {page.count('@@')}")
