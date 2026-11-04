"""Compare each project lab's page code block with its twin, and run each twin under python -I -W error.

Usage: labs_page_vs_twin.py <checkout_root>. Prints one line per lab: code-equal flag, twin exit code, stderr length,
and whether the page's expected block equals the twin's stdout (expected blocks compared after html unescape).
"""

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    m = re.search(
        rf'id="lab-BK4-project-{n}".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*'
        rf'<pre class="expected"[^>]*>(.*?)</pre>',
        page,
        re.S,
    )
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin_path = root / f"tests/labs/BK4/lab-BK4-project-{n}.py"
    twin = twin_path.read_text(encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp"
    )
    same_code = code.strip() == twin.strip()
    same_out = proc.stdout.strip() == expected.strip()
    print(f"lab {n}: page_code_equals_twin={same_code} twin_exit={proc.returncode} stderr_bytes={len(proc.stderr)} "
          f"expected_equals_stdout={same_out} code_lines={len(code.splitlines())} twin_lines={len(twin.splitlines())}")
    if not same_code:
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:60]))
