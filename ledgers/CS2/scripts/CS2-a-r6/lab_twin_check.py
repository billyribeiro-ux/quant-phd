"""Check CS2 slice-a lab sections: page code equals twin, expected block equals twin output.

Usage: lab_twin_check.py ROOT  (ROOT = checkout directory). Runs each twin under python -I -W error
in a scratch directory and compares its stdout with the page's expected block byte for byte
(after stripping one trailing newline on each side). Prints one line per lab.
"""

import html
import pathlib
import re
import subprocess
import sys
import tempfile

root = pathlib.Path(sys.argv[1])
py = root / ".venv" / "bin" / "python"
for lesson in ("L01", "L02", "L03", "L04"):
    page = (root / "course/modules/CS/CS2" / f"{lesson}.html").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="(lab-CS2-%s-1)"[^>]*>(.*?)</section>' % lesson, page, re.S)
    lab_id, body = m.group(1), m.group(2)
    code = html.unescape(re.search(r'<code class="language-python"[^>]*>(.*?)</code>', body, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1))
    twin = (root / "tests/labs/CS2" / f"{lab_id}.py").read_text(encoding="utf-8")
    same_code = code.rstrip("\n") == twin.rstrip("\n")
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([str(py), "-I", "-W", "error", str(root / "tests/labs/CS2" / f"{lab_id}.py")],
                           cwd=d, capture_output=True, text=True, timeout=120)
    out_ok = r.stdout.rstrip("\n") == expected.rstrip("\n")
    print(f"{lab_id}: page_code_equals_twin={same_code} exit={r.returncode} stderr_bytes={len(r.stderr)} "
          f"expected_equals_output={out_ok} lines={r.stdout.count(chr(10))}")
