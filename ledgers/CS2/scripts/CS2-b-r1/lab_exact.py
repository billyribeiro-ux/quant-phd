"""Exact lab check for CS2 slice b (L05-L08).

For each lab section on the page: (1) the page code, unescaped, equals the twin byte for byte
(trailing newlines aside); (2) the twin runs alone under python -I -W error in an empty scratch
directory with no data/ files, exit 0, empty stderr; (3) its stdout equals the page's expected
block byte for byte (after unescaping); (4) the twin calls main() at top level.
Usage: python -I -W error lab_exact.py <repo_root>
"""
from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1])
pages = {"L05": "lab-CS2-L05-1", "L06": "lab-CS2-L06-1", "L07": "lab-CS2-L07-1", "L08": "lab-CS2-L08-1"}
ok_all = True
for page, lab in pages.items():
    text = (root / "course/modules/CS/CS2" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(
        rf'<section class="lab" id="{lab}".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*'
        r'<pre class="expected"[^>]*>(.*?)</pre>',
        text,
        re.S,
    )
    if not m:
        print(page, "NO LAB SECTION FOUND")
        ok_all = False
        continue
    page_code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin = (root / "tests/labs/CS2" / f"{lab}.py").read_text(encoding="utf-8")
    code_eq = page_code.rstrip("\n") == twin.rstrip("\n")
    with tempfile.TemporaryDirectory() as scratch:
        proc = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(root / "tests/labs/CS2" / f"{lab}.py")],
            cwd=scratch, capture_output=True, text=True, timeout=60,
        )
    out_eq = proc.stdout.rstrip("\n") == expected.rstrip("\n")
    top_main = bool(re.search(r"^main\(\)\s*$", twin, re.M))
    print(f"{page} {lab}: page==twin {code_eq} exit {proc.returncode} stderr_empty {proc.stderr == ''} "
          f"stdout==expected {out_eq} top_level_main {top_main} stdout_lines {len(proc.stdout.splitlines())} "
          f"twin_bytes {len(twin.encode())}")
    if not (code_eq and proc.returncode == 0 and proc.stderr == "" and out_eq and top_main):
        ok_all = False
        if not out_eq:
            import difflib
            print("\n".join(difflib.unified_diff(expected.splitlines(), proc.stdout.splitlines(), "expected", "stdout", lineterm="")))
print("ALL_OK" if ok_all else "FAILURES")
