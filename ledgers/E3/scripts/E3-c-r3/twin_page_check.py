"""Compare each lab twin with its embedded page code and expected block; run each twin alone.

Usage: python -I ledgers/E3/scripts/E3-c-r3/twin_page_check.py
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = {
    "L07": ("course/modules/E/E3/L07.html", "tests/labs/E3/lab-E3-L07-1.py", "lab-E3-L07-1"),
    "L08": ("course/modules/E/E3/L08.html", "tests/labs/E3/lab-E3-L08-1.py", "lab-E3-L08-1"),
}
VENV_PY = ROOT / ".venv" / "bin" / "python"

for name, (page_rel, twin_rel, lab_id) in PAGES.items():
    page = (ROOT / page_rel).read_text(encoding="utf-8")
    twin = (ROOT / twin_rel).read_text(encoding="utf-8")
    m = re.search(
        r'<section class="lab" id="' + lab_id + r'".*?<pre><code[^>]*data-run>(.*?)</code></pre>\s*'
        r'<pre class="expected"[^>]*>(.*?)</pre>',
        page,
        re.S,
    )
    if not m:
        print(name, "NO LAB BLOCK FOUND")
        sys.exit(1)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    print(name, "page code == twin:", code == twin, "| len page", len(code), "len twin", len(twin))
    if code != twin:
        import difflib

        for line in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""))[:40]:
            print("   ", line)
    proc = subprocess.run(
        [str(VENV_PY), "-I", "-W", "error", str(ROOT / twin_rel)],
        capture_output=True,
        text=True,
        cwd="/tmp",
        timeout=120,
    )
    print(name, "twin exit", proc.returncode, "stderr:", proc.stderr.strip()[:300])
    out = proc.stdout
    print(name, "expected == output:", expected.rstrip("\n") == out.rstrip("\n"))
    if expected.rstrip("\n") != out.rstrip("\n"):
        for i, (a, b) in enumerate(zip(expected.splitlines(), out.splitlines())):
            if a != b:
                print("   line", i, "expected:", a, "| output:", b)
        print("   counts expected/output:", len(expected.splitlines()), len(out.splitlines()))
    (ROOT / "ledgers/E3/scripts/E3-c-r3" / f"{name}-twin-output.txt").write_text(out, encoding="utf-8")
