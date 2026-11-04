"""Round-2 BK4-b check: page code equals twin, expected block equals twin stdout, twin runs clean under -I -W error.

Usage: python3 -I ledgers/BK4/scripts/BK4-b-r2/twin_check.py <checkout-root>
Reads the page and twin files only. Runs each twin from a fresh temporary directory.
"""

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
pages = {"L04": "lab-BK4-L04-1", "L05": "lab-BK4-L05-1"}
failures = 0
for page, lab in pages.items():
    text = (root / "course/modules/BK/BK4" / f"{page}.html").read_text(encoding="utf-8")
    twin_src = (root / "tests/labs/BK4" / f"{lab}.py").read_text(encoding="utf-8")
    m_code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    m_exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    if not m_code or not m_exp:
        print(f"{page}: code or expected block not found")
        failures += 1
        continue
    page_code = html.unescape(m_code.group(1))
    expected = html.unescape(m_exp.group(1))
    same_code = page_code == twin_src
    print(f"{page} page code == twin: {same_code} (page {len(page_code)} chars, twin {len(twin_src)} chars)")
    failures += 0 if same_code else 1
    with tempfile.TemporaryDirectory() as d:
        script = Path(d) / f"{lab}.py"
        script.write_text(twin_src, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(script)],
            cwd=d, capture_output=True, text=True, timeout=60,
        )
    print(f"{page} exit={proc.returncode} stderr={proc.stderr!r}")
    same_out = proc.stdout == expected
    print(f"{page} expected block == twin stdout: {same_out}")
    if not same_out:
        import difflib
        for line in difflib.unified_diff(expected.splitlines(), proc.stdout.splitlines(), "expected", "stdout", lineterm=""):
            print("   ", line)
    failures += (proc.returncode != 0) + (proc.stderr != "") + (not same_out)
    if page == "L04":
        Path("/tmp/bk4b-r2/L04.stdout").write_text(proc.stdout, encoding="utf-8")
    else:
        Path("/tmp/bk4b-r2/L05.stdout").write_text(proc.stdout, encoding="utf-8")
print("FAILURES", failures)
