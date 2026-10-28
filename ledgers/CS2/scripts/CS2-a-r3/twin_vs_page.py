"""Run each CS2-a lab twin under python -I -W error and compare stdout with the page's expected block.

Usage: python twin_vs_page.py <checkout>. Reads the checkout's pages only, writes nothing.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
ok_all = True
for n in range(1, 5):
    page = root / "course/modules/CS/CS2" / f"L0{n}.html"
    text = page.read_text(encoding="utf-8")
    twin = root / "tests/labs" / "CS2" / f"lab-CS2-L0{n}-1.py"
    twin_src = twin.read_text(encoding="utf-8")
    m_run = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    m_exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    page_code = html.unescape(m_run.group(1))
    expected = html.unescape(m_exp.group(1))
    same_code = page_code.strip() == twin_src.strip()
    proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, timeout=120
    )
    actual = proc.stdout
    same_out = actual.rstrip("\n") == expected.rstrip("\n")
    print(f"L0{n}: code_identical_to_twin={same_code} rc={proc.returncode} stdout_equals_expected={same_out} stderr={proc.stderr.strip()[:200]!r}")
    if not same_out:
        import difflib
        for line in difflib.unified_diff(expected.splitlines(), actual.splitlines(), "page", "run", lineterm=""):
            print("   ", line)
    ok_all = ok_all and same_code and same_out and proc.returncode == 0
print("ALL_OK" if ok_all else "MISMATCH")
