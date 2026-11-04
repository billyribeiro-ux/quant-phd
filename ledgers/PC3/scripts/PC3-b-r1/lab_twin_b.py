"""Verifier PC3-b round 1: for L04-L06, (a) the twin runs alone under python -I -W error with exit 0 and no stderr,
(b) the page's data-run code equals the twin byte for byte, (c) the page's expected block equals the twin's stdout.
Run from the checkout root: .venv/bin/python -I ledgers/PC3/scripts/PC3-b-r1/lab_twin_b.py
"""
from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = {
    "L04": ("lab-PC3-L04-1", "course/modules/PC/PC3/L04.html"),
    "L05": ("lab-PC3-L05-1", "course/modules/PC/PC3/L05.html"),
    "L06": ("lab-PC3-L06-1", "course/modules/PC/PC3/L06.html"),
}
ok = True
for page, (twin_id, rel) in PAGES.items():
    twin = ROOT / "tests/labs" / "PC3" / f"{twin_id}.py"
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd="/tmp", check=False
    )
    print(f"{page} twin exit={run.returncode} stderr_bytes={len(run.stderr)} stdout_lines={run.stdout.count(chr(10))}")
    ok &= run.returncode == 0 and run.stderr == ""
    text = (ROOT / rel).read_text(encoding="utf-8")
    m_code = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    m_exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    code = html.unescape(m_code.group(1)) if m_code else None
    expected = html.unescape(m_exp.group(1)) if m_exp else None
    twin_src = twin.read_text(encoding="utf-8")
    same_code = code == twin_src
    same_out = expected == run.stdout.rstrip("\n")
    print(f"{page} page code == twin: {same_code} (page {len(code or '')} chars, twin {len(twin_src)} chars)")
    print(f"{page} expected == twin stdout: {same_out}")
    if not same_code or not same_out:
        import difflib

        if not same_code:
            print("\n".join(list(difflib.unified_diff(twin_src.splitlines(), (code or "").splitlines(), "twin", "page", lineterm=""))[:40]))
        if not same_out:
            print("\n".join(list(difflib.unified_diff(run.stdout.rstrip("\n").splitlines(), (expected or "").splitlines(), "stdout", "expected", lineterm=""))[:40]))
    ok &= same_code and same_out
print("ALL OK" if ok else "MISMATCH")
