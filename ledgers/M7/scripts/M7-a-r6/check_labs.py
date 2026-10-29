"""Independent lab check for M7 slice a (L01-L03): page code vs twin, twin output vs page expected block.

Usage: python3 -I ledgers/M7/scripts/M7-a-r6/check_labs.py <repo_root>
Runs each twin with python -I -W error in a fresh temp directory, no network.
"""
import html
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
pages = root / "course/modules/M/M7"
twins = root / "tests/labs/M7"
ok_all = True
for lid, page in (("lab-M7-L01-1", "L01"), ("lab-M7-L02-1", "L02"), ("lab-M7-L03-1", "L03")):
    text = (pages / f"{page}.html").read_text(encoding="utf-8")
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    exp_m = re.search(r'<pre class="expected" data-tolerance="([^"]+)">(.*?)</pre>', text, re.S)
    code = html.unescape(code_m.group(1)).rstrip("\n")
    expected = html.unescape(exp_m.group(2)).rstrip("\n")
    twin_text = (twins / f"{lid}.py").read_text(encoding="utf-8").rstrip("\n")
    same = code == twin_text
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(twins / f"{lid}.py")],
            capture_output=True, text=True, cwd=d, env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"}, timeout=60,
        )
    out = r.stdout.rstrip("\n")
    match = out == expected
    print(f"== {page} {lid}: code==twin {same}; exit {r.returncode}; stderr {r.stderr.strip()!r}; output==expected {match}")
    if not match:
        import difflib
        print("\n".join(difflib.unified_diff(expected.split("\n"), out.split("\n"), "expected", "twin-output", lineterm="")))
    print("OUTPUT:")
    print(out)
    ok_all = ok_all and same and match and r.returncode == 0 and not r.stderr.strip()
print("ALL OK" if ok_all else "PROBLEM")
