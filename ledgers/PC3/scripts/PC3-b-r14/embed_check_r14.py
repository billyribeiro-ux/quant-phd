"""Round-14 check for PC3 slice b: page code vs twin, twin under python -I -W error, expected block vs stdout.

Run from the checkout root: .venv/bin/python ledgers/PC3/scripts/PC3-b-r14/embed_check_r14.py
"""

import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE14-PC3-b")
OUT = ROOT / "ledgers/PC3/scripts/PC3-b-r14/out"
OUT.mkdir(parents=True, exist_ok=True)
PAIRS = [("L04", "lab-PC3-L04-1"), ("L05", "lab-PC3-L05-1"), ("L06", "lab-PC3-L06-1")]
for page, lab in PAIRS:
    src = (ROOT / f"course/modules/PC/PC3/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    code = html.unescape(m.group(1))
    twin = (ROOT / f"tests/labs/PC3/{lab}.py").read_text(encoding="utf-8")
    same_exact = code == twin
    same_rstrip = code.rstrip("\n") == twin.rstrip("\n")
    print(f"{page}: page code == twin byte-identical: {same_exact}; equal after trailing newline strip: {same_rstrip}")
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(e.group(1))
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/PC3/{lab}.py")],
        capture_output=True,
        text=True,
        cwd="/tmp",
    )
    (OUT / f"stdout_{page}_r14.txt").write_text(run.stdout, encoding="utf-8")
    print(f"{page}: twin exit={run.returncode} stderr_bytes={len(run.stderr.encode())}")
    print(f"{page}: stdout == expected block after rstrip: {run.stdout.rstrip() == expected.rstrip()}")
    print(f"{page}: stdout lines={run.stdout.count(chr(10))} expected lines={expected.count(chr(10))}")
