"""Round-21 check of the LX1 project labs: page code vs twin, expected block vs twin output.

Usage: .venv/bin/python -I ledgers/LX1/scripts/LX1-c-r21/twins_r21.py <repo_root> <scratch_dir>
Copies the lab data file into the scratch dir, runs each twin there with python -I -W error, and compares
its stdout with the page's expected block. Lab 2's page code must equal its twin except for the blank lines.
"""

import html
import re
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
(scratch / "data").mkdir(exist_ok=True)
shutil.copy(root / "course/assets/data/market/fx_monthly.csv", scratch / "data" / "fx_monthly.csv")
page = (root / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")

code_blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
expected_blocks = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("code blocks:", len(code_blocks), "expected blocks:", len(expected_blocks))

for n in (1, 2, 3):
    twin = (root / f"tests/labs/LX1/lab-LX1-project-{n}.py").read_text(encoding="utf-8")
    page_code = html.unescape(code_blocks[n - 1])
    twin_lines = twin.rstrip("\n").split("\n")
    page_lines = page_code.rstrip("\n").split("\n")
    diffs = [(i, p, t) for i, (p, t) in enumerate(zip(page_lines, twin_lines)) if p != t]
    same_len = len(page_lines) == len(twin_lines)
    print(f"lab {n}: twin lines {len(twin_lines)}, page lines {len(page_lines)}, same length {same_len}, differing lines {len(diffs)}")
    for i, p, t in diffs:
        print(f"   line {i + 1}: page={p!r}")
        print(f"   line {i + 1}: twin={t!r}")
    proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(root / f"tests/labs/LX1/lab-LX1-project-{n}.py")],
        cwd=scratch,
        capture_output=True,
        text=True,
        timeout=60,
    )
    print(f"lab {n}: twin exit {proc.returncode}, stderr {proc.stderr.strip()[:200]!r}")
    expected = html.unescape(expected_blocks[n - 1]).rstrip("\n")
    out = proc.stdout.rstrip("\n")
    print(f"lab {n}: expected block equals twin stdout: {expected == out}")
    if n == 2:
        # the page's lab 2 must also be equal to the completed twin in the expected block
        print("lab 2 page code equals twin with blanks only:", all(p == t or "___" in p for p, t in zip(page_lines, twin_lines)))
