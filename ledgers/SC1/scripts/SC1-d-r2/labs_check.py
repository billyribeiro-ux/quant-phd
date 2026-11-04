"""Check the three SC1 project labs: page code vs twin, twin run under python -I -W error, stdout vs the page's expected block."""

from __future__ import annotations

import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PAGE = ROOT / "course/modules/SC/SC1/project.html"
TWINS = ROOT / "tests/labs/SC1"
text = PAGE.read_text(encoding="utf-8")

for lab in ("lab-SC1-project-1", "lab-SC1-project-2", "lab-SC1-project-3"):
    m = re.search(rf'<section[^>]*id="{lab}"[^>]*>(.*?)</section>', text, re.S)
    assert m, lab
    body = m.group(1)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    assert code and expected, lab
    page_code = html.unescape(code.group(1))
    page_expected = html.unescape(expected.group(1))
    twin_path = TWINS / f"{lab}.py"
    twin = twin_path.read_text(encoding="utf-8")
    diff = list(difflib.unified_diff(twin.splitlines(), page_code.splitlines(), "twin", "page", lineterm="", n=0))
    print(f"== {lab}: page code vs twin: {'IDENTICAL' if page_code == twin else f'{len(diff)} diff lines'}")
    for line in diff:
        print("   ", line)
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, timeout=120
    )
    print(f"   twin exit {run.returncode}, stderr bytes {len(run.stderr.encode())}")
    same = run.stdout.rstrip("\n") == page_expected.rstrip("\n")
    print(f"   stdout equals page expected block: {same}")
    if not same:
        print("   stdout:", repr(run.stdout))
        print("   expected:", repr(page_expected))
