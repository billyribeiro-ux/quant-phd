"""Project labs: twin run under python -I -W error, page code vs twin, page expected block vs twin output (BK4-c r2).

Usage (from the checkout root): .venv/bin/python ledgers/BK4/scripts/BK4-c-r2/twin_vs_page.py
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGE = (ROOT / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
sections = re.findall(r'<section class="(lab[^"]*)" id="(lab-BK4-project-\d)"[^>]*>(.*?)</section>', PAGE, re.S)
for cls, lab_id, body in sections:
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1))
    twin_path = ROOT / "tests/labs/BK4" / f"{lab_id}.py"
    twin = twin_path.read_text(encoding="utf-8")
    res = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp", check=False)
    twin_out = res.stdout
    print(f"{lab_id} class={cls!r} twin exit={res.returncode} stderr_bytes={len(res.stderr.encode())}")
    print(f"  page code == twin (trailing newline aside): {code.rstrip(chr(10)) == twin.rstrip(chr(10))}")
    if "completion" in cls:
        page_lines = code.rstrip("\n").splitlines()
        twin_lines = twin.rstrip("\n").splitlines()
        print(f"  completion: page lines {len(page_lines)} twin lines {len(twin_lines)}")
        diffs = [(i, p, t) for i, (p, t) in enumerate(zip(page_lines, twin_lines)) if p != t and "___" not in p]
        print(f"  completion: lines that differ from twin and contain no blank: {diffs}")
    print(f"  expected block == twin output: {expected.strip() == twin_out.strip()}")
    if expected.strip() != twin_out.strip():
        print("  expected:", expected.strip()[:300])
        print("  output:  ", twin_out.strip()[:300])
