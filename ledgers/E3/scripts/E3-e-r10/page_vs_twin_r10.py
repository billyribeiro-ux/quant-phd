"""Round-10: each project lab's code on the page equals its twin (after strip), with ___ blanks allowed on Lab 2;
the page's expected block equals the twin's printed output (run under python -I -W error)."""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
page = (ROOT / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    m = re.search(rf'<section class="lab[^"]*" id="lab-E3-project-{n}".*?<pre><code[^>]*data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, flags=re.S)
    code = html.unescape(m.group(1)).strip()
    expected = html.unescape(m.group(2)).strip()
    twin_path = ROOT / f"tests/labs/E3/lab-E3-project-{n}.py"
    twin = twin_path.read_text(encoding="utf-8").strip()
    same = code == twin
    if n == 2:
        code_lines, twin_lines = code.splitlines(), twin.splitlines()
        blank_ok = len(code_lines) == len(twin_lines) and all(
            a == b or "___" in a for a, b in zip(code_lines, twin_lines, strict=True))
        print(f"lab {n}: page lines={len(code_lines)} twin lines={len(twin_lines)} every line equal or blanked: {blank_ok}; blank lines: {[l.strip() for l in code_lines if '___' in l]}")
    else:
        print(f"lab {n}: page code equals twin: {same}")
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd=ROOT)
    print(f"lab {n}: twin exit={out.returncode} stderr_bytes={len(out.stderr)} output_equals_expected={out.stdout.strip() == expected}")
    if out.stdout.strip() != expected:
        print("  expected:", expected.splitlines()[:3], "\n  got     :", out.stdout.strip().splitlines()[:3])
