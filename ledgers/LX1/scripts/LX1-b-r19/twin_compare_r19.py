"""Round 19: page lab code equals the lab twin, and the page expected block equals the twin's run output.

Usage (from the checkout root): .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r19/twin_compare_r18.py
Reads course/modules/LX/LX1/L01.html, L03.html, L04.html and tests/labs/LX1/lab-LX1-L0n-1.py, and the stdout
files written by run_twins_r18.sh under ledgers/LX1/scripts/LX1-b-r19/out/twin_L0n.stdout.
"""

import html
import re
import sys
from pathlib import Path

ROOT = Path(".")
OUT = ROOT / "ledgers/LX1/scripts/LX1-b-r19/out"
CODE = re.compile(r'<code class="language-python" data-run>(.*?)</code></pre>', re.S)
EXPECTED = re.compile(r'<pre class="expected"[^>]*>(.*?)</pre>', re.S)
status = 0
for lesson in ("L01", "L03", "L04"):
    page = (ROOT / f"course/modules/LX/LX1/{lesson}.html").read_text(encoding="utf-8")
    twin = (ROOT / f"tests/labs/LX1/lab-LX1-{lesson}-1.py").read_text(encoding="utf-8")
    m = CODE.search(page)
    code = html.unescape(m.group(1)) if m else None
    same = code is not None and code.rstrip(chr(10)) == twin.rstrip(chr(10))
    strict = code == twin
    print(f"{lesson}: page code block found={m is not None}; page code equals twin (trailing newline stripped, as run_labs does): {same}; strict byte equality: {strict}")
    if not same and code is not None:
        status = 1
        import difflib

        for line in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""))[:40]:
            print("   ", line)
    e = EXPECTED.search(page)
    expected = html.unescape(e.group(1)) if e else None
    stdout_path = OUT / f"twin_{lesson}.stdout"
    if stdout_path.exists():
        actual = stdout_path.read_text(encoding="utf-8")
        ok = expected is not None and expected.rstrip("\n") == actual.rstrip("\n")
        print(f"{lesson}: expected block equals twin stdout: {ok} (expected lines {len(expected.splitlines()) if expected else 0}, actual lines {len(actual.splitlines())})")
        if not ok:
            status = 1
            import difflib

            for line in list(difflib.unified_diff((expected or "").splitlines(), actual.splitlines(), "page", "run", lineterm=""))[:40]:
                print("   ", line)
    else:
        print(f"{lesson}: no twin stdout file at {stdout_path}")
        status = 1
sys.exit(status)
