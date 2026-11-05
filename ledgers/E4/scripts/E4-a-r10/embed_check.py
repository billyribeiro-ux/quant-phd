"""Check that each E4 slice-a lab page embeds its twin verbatim and that its expected block equals the twin's output.

Usage: .venv/bin/python -I ledgers/E4/scripts/E4-a-r10/embed_check.py
Runs each twin with the same interpreter (-I -W error) and compares stdout to the page's pre.expected text.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAIRS = [
    ("course/modules/E/E4/L01.html", "tests/labs/E4/lab-E4-L01-1.py", "lab-E4-L01-1"),
    ("course/modules/E/E4/L02.html", "tests/labs/E4/lab-E4-L02-1.py", "lab-E4-L02-1"),
    ("course/modules/E/E4/L03.html", "tests/labs/E4/lab-E4-L03-1.py", "lab-E4-L03-1"),
]
ok = True
for page, twin, lab_id in PAIRS:
    text = (ROOT / page).read_text(encoding="utf-8")
    section = re.search(rf'<section class="lab" id="{lab_id}".*?</section>', text, flags=re.S)
    if not section:
        print(f"{lab_id}: section missing")
        ok = False
        continue
    body = section.group(0)
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', body, flags=re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, flags=re.S)
    twin_src = (ROOT / twin).read_text(encoding="utf-8")
    page_code = html.unescape(code.group(1))
    code_same = page_code.rstrip("\n") == twin_src.rstrip("\n")
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(ROOT / twin)], capture_output=True, text=True, cwd=ROOT / "tests" / "labs" / "E4"
    )
    page_expected = html.unescape(expected.group(1))
    out_same = page_expected.rstrip("\n") == run.stdout.rstrip("\n")
    print(f"{lab_id}: twin_exit={run.returncode} stderr_bytes={len(run.stderr.encode())} "
          f"page_code_equals_twin={code_same} expected_equals_output={out_same} "
          f"page_code_has_blanks={'___' in page_code}")
    ok = ok and code_same and out_same and run.returncode == 0 and not run.stderr
print("ALL OK" if ok else "MISMATCH")
