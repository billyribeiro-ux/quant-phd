"""FC2 slice b round 2: twin vs page code vs expected block, for L04, L05, L06.

Run: python -I -W error ledgers/FC2/scripts/FC2-b-r2/v2_twin_vs_page.py <checkout>
Each twin is executed alone with python -I -W error from an empty temporary directory;
its stdout is compared byte-for-byte with the page's expected block, and the page's
code block is compared with the twin source (after HTML unescaping).
"""

from __future__ import annotations

import html
import os
import re
import subprocess
import sys
import tempfile

ROOT = sys.argv[1]
PAGES = {
    "L04": ("course/modules/FC/FC2/L04.html", "tests/labs/FC2/lab-FC2-L04-1.py", "lab-FC2-L04-1"),
    "L05": ("course/modules/FC/FC2/L05.html", "tests/labs/FC2/lab-FC2-L05-1.py", "lab-FC2-L05-1"),
    "L06": ("course/modules/FC/FC2/L06.html", "tests/labs/FC2/lab-FC2-L06-1.py", "lab-FC2-L06-1"),
}
PY = os.path.join(ROOT, ".venv", "bin", "python")

for page_key, (page_rel, twin_rel, lab_id) in PAGES.items():
    with open(os.path.join(ROOT, page_rel), encoding="utf-8") as fh:
        text = fh.read()
    section = re.search(r'<section class="lab" id="%s".*?</section>' % re.escape(lab_id), text, re.S)
    assert section, page_key
    body = section.group(0)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S).group(1)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1)
    code_src = html.unescape(code)
    expected_out = html.unescape(expected)
    with open(os.path.join(ROOT, twin_rel), encoding="utf-8") as fh:
        twin_src = fh.read()
    print(
        f"{page_key}: page code == twin source: {code_src == twin_src} "
        f"(modulo the final newline: {code_src.rstrip(chr(10)) == twin_src.rstrip(chr(10))}; "
        f"page {len(code_src)} chars, twin {len(twin_src)} chars)"
    )
    with tempfile.TemporaryDirectory() as scratch:
        twin_copy = os.path.join(scratch, "twin_" + lab_id + ".py")
        with open(twin_copy, "w", encoding="utf-8") as fh:
            fh.write(twin_src)
        proc = subprocess.run(
            [PY, "-I", "-W", "error", twin_copy],
            cwd=scratch,
            capture_output=True,
            text=True,
            timeout=120,
        )
    out_ok = proc.stdout == expected_out or proc.stdout.rstrip("\n") == expected_out.rstrip("\n")
    print(
        f"{page_key}: twin exit={proc.returncode} stderr_empty={proc.stderr == ''} "
        f"stdout_equals_expected={out_ok} stdout_lines={proc.stdout.count(chr(10))}"
    )
    if not out_ok:
        print("--- diff (expected vs actual)")
        import difflib

        for line in difflib.unified_diff(
            expected_out.splitlines(), proc.stdout.splitlines(), "expected", "actual", lineterm=""
        ):
            print(line)
