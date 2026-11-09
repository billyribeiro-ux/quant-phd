"""FC1-a round 4: page code and expected block versus the twin, and the twin's own output (run alone, -I -W error).

Run from the checkout root: .venv/bin/python -I ledgers/FC1/scripts/FC1-a-r4/twin_page_r4.py
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
PY = str(ROOT / ".venv" / "bin" / "python")
PAIRS = [
    ("L01", "course/modules/FC/FC1/L01.html", "tests/labs/FC1/lab-FC1-L01-1.py"),
    ("L02", "course/modules/FC/FC1/L02.html", "tests/labs/FC1/lab-FC1-L02-1.py"),
    ("L03", "course/modules/FC/FC1/L03.html", "tests/labs/FC1/lab-FC1-L03-1.py"),
]
for name, page, twin in PAIRS:
    text = (ROOT / page).read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="lab-FC1-(L0\d)-1"[^>]*>(.*?)</section>', text, re.S)
    body = m.group(2)
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', body, re.S).group(1)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1)
    code_plain = html.unescape(code).strip("\n")
    twin_src = (ROOT / twin).read_text(encoding="utf-8").strip("\n")
    print(f"{name}: page code == twin (after outer newlines): {code_plain == twin_src}; "
          f"page code lines {len(code_plain.splitlines())}, twin lines {len(twin_src.splitlines())}")
    # the page must not contain @@ markers left behind
    print(f"{name}: @@ markers in page: {'@@' in body}")
    out = subprocess.run([PY, "-I", "-W", "error", str(ROOT / twin)], capture_output=True, text=True, cwd=str(ROOT))
    print(f"{name}: twin alone exit={out.returncode} stderr_bytes={len(out.stderr)}")
    exp_plain = html.unescape(expected).strip("\n")
    run_plain = out.stdout.strip("\n")
    print(f"{name}: expected block == twin output: {exp_plain == run_plain}")
    if exp_plain != run_plain:
        for i, (a, b) in enumerate(zip(exp_plain.splitlines(), run_plain.splitlines())):
            if a != b:
                print("   first diff line", i, repr(a), repr(b))
                break
        print("   lens", len(exp_plain.splitlines()), len(run_plain.splitlines()))
    sys.stdout.flush()
