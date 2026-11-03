"""Run each E3 lab twin for L05-L08 alone under python -I -W error and compare stdout with the page's expected block.

Usage: twin_vs_page.py <repo_root> <python>
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
py = sys.argv[2]
for lesson in ("L05", "L06", "L07", "L08"):
    twin = root / "tests/labs" / "E3" / f"lab-E3-{lesson}-1.py"
    page = (root / "course/modules/E/E3" / f"{lesson}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else None
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    run = subprocess.run([py, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd="/tmp", timeout=120)
    out = run.stdout.strip()
    print(f"{lesson}: twin exit={run.returncode} stderr_bytes={len(run.stderr)} output_lines={len(out.splitlines())}")
    print(f"{lesson}: page expected block present={m is not None}; page code block present={code_m is not None}")
    print(f"{lesson}: expected == twin stdout: {expected == out}")
    if expected != out:
        print("DIFF expected:", repr(expected[:300]))
        print("DIFF output  :", repr(out[:300]))
