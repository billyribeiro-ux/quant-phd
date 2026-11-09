"""FC1-a round 2: page lab code equals its twin, and the page expected block equals the twin's stdout.

Run from the checkout root with: .venv/bin/python -I ledgers/FC1/scripts/FC1-a-r2/lab_equality_r2.py
"""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
PAGES = {
    "L01": ("course/modules/FC/FC1/L01.html", "tests/labs/FC1/lab-FC1-L01-1.py"),
    "L02": ("course/modules/FC/FC1/L02.html", "tests/labs/FC1/lab-FC1-L02-1.py"),
    "L03": ("course/modules/FC/FC1/L03.html", "tests/labs/FC1/lab-FC1-L03-1.py"),
}
CODE = re.compile(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', re.S)
EXPECTED = re.compile(r'<pre class="expected"[^>]*>(.*?)</pre>', re.S)
ok = True
for page, (html_path, twin_path) in PAGES.items():
    text = (ROOT / html_path).read_text(encoding="utf-8")
    codes = CODE.findall(text)
    expected = EXPECTED.findall(text)
    twin = (ROOT / twin_path).read_text(encoding="utf-8")
    page_code = html.unescape(codes[0])
    code_eq = page_code.rstrip("\n") == twin.rstrip("\n")
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(ROOT / twin_path)], capture_output=True, text=True, check=False
    )
    out = run.stdout
    exp = html.unescape(expected[0])
    exp_eq = exp.rstrip("\n") == out.rstrip("\n")
    print(f"{page}: blocks={len(codes)}/{len(expected)} code==twin {code_eq}; expected==twin stdout {exp_eq}; twin exit {run.returncode}")
    if not (code_eq and exp_eq and run.returncode == 0 and len(codes) == 1 and len(expected) == 1):
        ok = False
        if not code_eq:
            print("  first differing code line:")
            for a, b in zip(page_code.splitlines(), twin.splitlines()):
                if a != b:
                    print("   page:", a)
                    print("   twin:", b)
                    break
print("ALL EQUAL" if ok else "MISMATCH")
