"""Round-5 check (trailing newlines stripped, as tools/embed_labs.py and run_labs.py do): each lab page's code block equals its twin, and each expected block equals the twin's stdout.

Run: .venv/bin/python -I ledgers/PC3/scripts/PC3-a-r6/embed_compare_a_r5.py   (from the checkout root)
Also runs each twin alone under python -I -W error and prints its exit code, stdout line count and stderr size.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
PAIRS = {
    "L01": ("course/modules/PC/PC3/L01.html", "tests/labs/PC3/lab-PC3-L01-1.py", "lab-PC3-L01-1"),
    "L02": ("course/modules/PC/PC3/L02.html", "tests/labs/PC3/lab-PC3-L02-1.py", "lab-PC3-L02-1"),
    "L03": ("course/modules/PC/PC3/L03.html", "tests/labs/PC3/lab-PC3-L03-1.py", "lab-PC3-L03-1"),
}
ok_all = True
for page, (html_path, twin_path, lab_id) in PAIRS.items():
    text = (ROOT / html_path).read_text(encoding="utf-8")
    m = re.search(
        r'<section class="lab" id="' + re.escape(lab_id) + r'".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*'
        r'<pre class="expected"[^>]*>(.*?)</pre>',
        text,
        re.S,
    )
    if not m:
        print(page, "NO LAB MATCH")
        ok_all = False
        continue
    code = html.unescape(m.group(1)).rstrip("\n")
    expected = html.unescape(m.group(2)).rstrip("\n")
    twin = (ROOT / twin_path).read_text(encoding="utf-8").rstrip("\n")
    code_eq = code == twin
    proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", twin_path], capture_output=True, text=True, cwd=ROOT, timeout=120
    )
    stdout_eq = proc.stdout.rstrip("\n") == expected
    print(f"{page}: page code == twin: {code_eq} (code {len(code)} chars, twin {len(twin)} chars)")
    print(f"{page}: expected block == twin stdout: {stdout_eq} (stdout lines {proc.stdout.count(chr(10))}, expected lines {expected.count(chr(10))})")
    print(f"{page}: twin exit={proc.returncode} stderr_bytes={len(proc.stderr.encode())}")
    if not stdout_eq:
        import difflib

        print("".join(difflib.unified_diff(expected.splitlines(True), proc.stdout.splitlines(True), "expected", "stdout")))
    print(f"{page}: expected-block tolerance attr:", re.search(r'<pre class="expected"([^>]*)>', text).group(1).strip())
    ok_all = ok_all and code_eq and stdout_eq and proc.returncode == 0 and len(proc.stderr) == 0
print("ALL_OK" if ok_all else "NOT_OK")
