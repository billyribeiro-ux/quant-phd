"""Round-6 check: each lab's page code equals its twin, and its expected block equals the twin's stdout (exact).

Run from the checkout root with: python3 -I ledgers/SC1/scripts/SC1-c-r6/twin_page_check_r6.py .
The twin is executed with python -I -W error, so no network, no user site, and no warnings are allowed.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
for lesson in ("L07", "L08"):
    page = (root / f"course/modules/SC/SC1/{lesson}.html").read_text(encoding="utf-8")
    twin_path = root / f"tests/labs/SC1/lab-SC1-{lesson}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1))
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp"
    )
    print(f"{lesson}: twin exit={run.returncode} stderr_bytes={len(run.stderr)}")
    print(f"{lesson}: page code == twin: {code.strip() == twin.strip()}")
    print(f"{lesson}: expected == twin stdout (exact): {expected.strip() == run.stdout.strip()}")
    print(f"{lesson}: expected lines={len(expected.splitlines())} stdout lines={len(run.stdout.splitlines())}")
