"""Round 11 M4 slice a: lab twins vs page code, expected block vs twin stdout.

Run as: python -I -W error ledgers/M4/scripts/M4-a-r11/lab_check.py  (from the checkout root)
For each of L01-L04: extract the page's data-run code block and the expected block, compare
the code with the twin byte for byte, run the twin alone under python -I -W error, and compare
its stdout with the expected block.
"""

import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD11-M4-a")
PAGES = {"L01": "lab-M4-L01-1", "L02": "lab-M4-L02-1", "L03": "lab-M4-L03-1", "L04": "lab-M4-L04-1"}
ok = True
for page, twin_id in PAGES.items():
    text = (ROOT / "course/modules/M/M4" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="' + twin_id + r'".*?<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text[m.end():] if m else text, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(e.group(1))
    twin = (ROOT / "tests/labs/M4" / f"{twin_id}.py").read_text(encoding="utf-8")
    same_code = code == twin.rstrip("\n")
    proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(ROOT / "tests/labs/M4" / f"{twin_id}.py")],
        capture_output=True, text=True, cwd="/tmp", timeout=60,
    )
    same_out = proc.stdout.rstrip("\n") == expected.rstrip("\n")
    print(f"{page} {twin_id}: code==twin {same_code} (page {len(code)} chars, twin {len(twin)}); "
          f"exit {proc.returncode}; stdout==expected {same_out}; stderr={proc.stderr.strip()[:200]!r}")
    if not (same_code and same_out and proc.returncode == 0):
        ok = False
        if not same_code:
            import difflib
            print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:40]))
        if not same_out:
            import difflib
            print("".join(list(difflib.unified_diff(expected.splitlines(True), proc.stdout.splitlines(True), "expected", "stdout"))[:40]))
print("ALL OK" if ok else "MISMATCH")
