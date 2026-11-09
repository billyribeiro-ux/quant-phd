"""Project labs: page code block equals the twin file, the twin runs alone under python -I -W error, and the page's
expected block equals the twin's output. Usage: python -I labs_twin_r14.py (run from the checkout root)."""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGE = (ROOT / "course/modules/CS/CS2/project.html").read_text(encoding="utf-8")
PY = sys.executable
ok_all = True
for n in (1, 2, 3):
    lab_id = f"lab-CS2-project-{n}"
    section = re.search(rf'<section class="lab[^"]*" id="{lab_id}".*?</section>', PAGE, re.S)
    assert section, lab_id
    body = section.group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1))
    twin = (ROOT / f"tests/labs/CS2/lab-CS2-project-{n}.py").read_text(encoding="utf-8")
    same = code.strip() == twin.strip()
    res = subprocess.run([PY, "-I", "-W", "error", str(ROOT / f"tests/labs/CS2/lab-CS2-project-{n}.py")],
                         capture_output=True, text=True, cwd="/tmp", timeout=120)
    out_ok = res.returncode == 0 and res.stdout.strip() == expected.strip()
    print(f"{lab_id}: page code == twin: {same}; twin rc={res.returncode}; twin stdout == expected block: {out_ok}")
    if res.returncode or res.stderr:
        print("  stderr:", res.stderr[:300])
    if not (same and out_ok):
        ok_all = False
    print("  page code lines:", len(code.splitlines()), "twin lines:", len(twin.splitlines()), "expected lines:", len(expected.splitlines()))
print("ALL OK" if ok_all else "MISMATCH")
