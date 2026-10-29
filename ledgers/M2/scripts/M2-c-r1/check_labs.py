"""Verifier script (M2 slice c, round 1): compare each L13-L18 page's embedded lab code and expected output with its twin.

Usage: python -I -W error check_labs.py <checkout-root>
Runs each twin in a subprocess with python -I -W error, compares stdout with the page's expected block,
and checks that the embedded code block equals the twin file (after html unescape).
"""

import html
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
for n in range(13, 19):
    page = (root / "course/modules/M/M2" / f"L{n:02d}.html").read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1))
    twin_path = root / "tests/labs/M2" / f"lab-M2-L{n:02d}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    same = code.strip() == twin.strip()
    proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, timeout=120
    )
    out = proc.stdout
    exact = out.rstrip("\n") == expected.rstrip("\n")
    print(f"L{n:02d} embedded==twin: {same} | rc={proc.returncode} | stdout==expected block: {exact}")
    if proc.stderr:
        print("  stderr:", proc.stderr.strip()[:300])
    if not exact:
        print("  ACTUAL:\n" + out)
        print("  EXPECTED:\n" + expected)
