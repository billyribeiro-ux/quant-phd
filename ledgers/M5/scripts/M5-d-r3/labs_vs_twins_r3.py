"""Round 3, slice d: the project page's three lab blocks against tests/labs/M5/lab-M5-project-{1,2,3}.py.

Checks (a) the page's code block equals the twin file byte-for-byte after HTML unescaping, (b) the twin runs under
python -I -W error with exit 0, (c) its stdout equals the page's expected block. Usage: python3 -I <this> <checkout-root>.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
page = (root / "course/modules/M/M5/project.html").read_text(encoding="utf-8")
sections = re.split(r'<section class="lab', page)[1:4]
for n, sec in enumerate(sections, start=1):
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin_path = root / f"tests/labs/M5/lab-M5-project-{n}.py"
    twin = twin_path.read_text(encoding="utf-8")
    same = code.strip("\n") == twin.strip("\n")
    run = subprocess.run([str(root / ".venv/bin/python"), "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, check=False)
    out_ok = run.stdout.strip("\n") == expected.strip("\n")
    print(f"lab {n}: page code == twin: {same} | twin rc={run.returncode} stderr_bytes={len(run.stderr)} | stdout == expected block: {out_ok}")
    if not out_ok:
        print("  expected:", repr(expected[:300]))
        print("  actual:  ", repr(run.stdout[:300]))
