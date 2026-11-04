"""Compare each lab's page code and expected block with its twin and with the twin's observed stdout.

Run from the checkout root: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r3/embed_check.py
"""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
PAGES = {"L01": "course/modules/SC/SC1/L01.html", "L02": "course/modules/SC/SC1/L02.html", "L03": "course/modules/SC/SC1/L03.html"}
for page, rel in PAGES.items():
    text = (ROOT / rel).read_text(encoding="utf-8")
    twin_path = ROOT / f"tests/labs/SC1/lab-SC1-{page}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    code_eq = code.rstrip("\n") == twin.rstrip("\n")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True)
    stdout_eq = expected.rstrip("\n") == run.stdout.rstrip("\n")
    print(f"{page}: code==twin (trailing newline ignored): {code_eq}; expected==stdout: {stdout_eq}; exit {run.returncode}; stderr bytes {len(run.stderr.encode())}; expected lines {len(expected.splitlines())}")
    if not code_eq:
        import difflib
        for line in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""):
            print("   ", line)
    if not stdout_eq:
        import difflib
        for line in difflib.unified_diff(expected.splitlines(), run.stdout.splitlines(), "page_expected", "stdout", lineterm=""):
            print("   ", line)
