"""Round-1 FC1-a check: each lab section's code block equals its twin, and its expected block equals the twin's output.

Run from the checkout root: .venv/bin/python -I ledgers/FC1/scripts/FC1-a-r1/lab_equality.py
"""

from __future__ import annotations

import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(".").resolve()
PAGES = {"L01": "lab-FC1-L01-1", "L02": "lab-FC1-L02-1", "L03": "lab-FC1-L03-1"}
PY = str(ROOT / ".venv" / "bin" / "python")
ok = True
for page, lab_id in PAGES.items():
    text = (ROOT / "course/modules/FC/FC1" / f"{page}.html").read_text(encoding="utf-8")
    section = re.search(rf'<section class="lab" id="{lab_id}".*?</section>', text, re.S)
    if section is None:
        print(page, "NO LAB SECTION")
        ok = False
        continue
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', section.group(0), re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section.group(0), re.S)
    twin = (ROOT / "tests/labs/FC1" / f"{lab_id}.py").read_text(encoding="utf-8")
    page_code = html.unescape(code.group(1))
    same_code = page_code.rstrip("\n") == twin.rstrip("\n")
    out = subprocess.run([PY, "-I", "-W", "error", str(ROOT / "tests/labs/FC1" / f"{lab_id}.py")],
                         capture_output=True, text=True).stdout
    page_expected = html.unescape(expected.group(1))
    same_out = page_expected.rstrip("\n") == out.rstrip("\n")
    print(f"{page}: code==twin {same_code} (page {len(page_code)} chars, twin {len(twin)}); "
          f"expected==twin output {same_out} (page {len(page_expected)}, output {len(out)})")
    if not (same_code and same_out):
        ok = False
        if not same_code:
            import difflib
            print("".join(list(difflib.unified_diff(twin.splitlines(True), page_code.splitlines(True), "twin", "page"))[:60]))
        if not same_out:
            import difflib
            print("".join(list(difflib.unified_diff(out.splitlines(True), page_expected.splitlines(True), "output", "page"))[:60]))
print("ALL EQUAL" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
