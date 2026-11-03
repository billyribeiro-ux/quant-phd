"""Round-4 verifier: run each project lab twin alone under python -I -W error, compare the twin's stdout with the
expected block on project.html, and check that the page code equals the twin (after the embed markers).

Usage (from the checkout root): .venv/bin/python -I ledgers/M3/scripts/M3-d-r4/project_labs_check_r4.py
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
PAGE = (ROOT / "course/modules/M/M3/project.html").read_text(encoding="utf-8")
TWINS = {1: "tests/labs/M3/lab-M3-project-1.py", 2: "tests/labs/M3/lab-M3-project-2.py", 3: "tests/labs/M3/lab-M3-project-3.py"}
SECTIONS = {1: "lab-M3-project-1", 2: "lab-M3-project-2", 3: "lab-M3-project-3"}

import html


def page_block(lab_id: str) -> tuple[str, str]:
    start = PAGE.index(f'id="{lab_id}"')
    end = PAGE.index("</section>", start)
    section = PAGE[start:end]
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', section, re.S).group(1)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section, re.S).group(1)
    return html.unescape(code), html.unescape(expected)


for n, twin_path in TWINS.items():
    twin = (ROOT / twin_path).read_text(encoding="utf-8")
    code, expected = page_block(SECTIONS[n])
    res = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / twin_path)], capture_output=True, text=True)
    out = res.stdout
    print(f"lab {n}: twin exit={res.returncode} stderr={res.stderr.strip()[:200]!r}")
    print(f"lab {n}: twin stdout equals page expected block: {out.strip() == expected.strip()}")
    print(f"lab {n}: page code equals twin (code-only, whitespace-stripped): {code.strip() == twin.strip()}")
    if out.strip() != expected.strip():
        print("  output:\n" + out)
        print("  expected:\n" + expected)
    if code.strip() != twin.strip():
        import difflib
        for line in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""))[:40]:
            print("  " + line)
