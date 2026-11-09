"""Verifier E1-c round 2: page code equals twin, expected block equals twin stdout (python -I -W error)."""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PAGES = {"L07": "lab-E1-L07-1", "L08": "lab-E1-L08-1", "L09": "lab-E1-L09-1"}

for page, lab in PAGES.items():
    text = (ROOT / "course/modules/E/E1" / f"{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    twin_path = ROOT / "tests/labs/E1" / f"{lab}.py"
    twin = twin_path.read_text(encoding="utf-8")
    page_code = html.unescape(code.group(1))
    same_code = page_code.rstrip("\n") == twin.rstrip("\n")
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd=ROOT
    )
    out = run.stdout
    exp = html.unescape(expected.group(1))
    same_exp = exp.rstrip("\n") == out.rstrip("\n")
    print(f"{page} {lab}: exit={run.returncode} stderr={run.stderr.strip()!r} code_equals_twin={same_code} "
          f"expected_equals_output={same_exp} code_lines={page_code.count(chr(10))} twin_lines={twin.count(chr(10))}")
    if not same_exp:
        import difflib
        print("\n".join(difflib.unified_diff(exp.splitlines(), out.splitlines(), "expected", "output", lineterm="")))
    if not same_code:
        import difflib
        print("\n".join(list(difflib.unified_diff(page_code.splitlines(), twin.splitlines(), "page", "twin", lineterm=""))[:40]))
    print(out, end="")
