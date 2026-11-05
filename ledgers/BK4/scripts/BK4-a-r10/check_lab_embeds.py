"""Round 10 check: each slice lab twin's page code equals the twin, and the page's expected block equals a fresh run.

Usage: check_lab_embeds.py <checkout-root>. Runs each twin with python -I -W error from the checkout root's scratch dir
and compares stdout with the expected block of the lab section in the page.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
for page in ("L01", "L02", "L03"):
    path = root / f"course/modules/BK/BK4/{page}.html"
    text = path.read_text(encoding="utf-8")
    lab_id = f"lab-BK4-{page}-1"
    section = re.search(rf'<section class="lab" id="{lab_id}".*?</section>', text, re.S)
    if section is None:
        print(f"{lab_id}: section not found")
        continue
    body = section.group(0)
    code = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    twin_path = root / f"tests/labs/BK4/{lab_id}.py"
    twin = twin_path.read_text(encoding="utf-8")
    code_text = html.unescape(code.group(1))
    exp_text = html.unescape(expected.group(1))
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp"
    )
    print(f"{lab_id}: page code equals twin: {code_text == twin} (page {len(code_text)} chars, twin {len(twin)})")
    print(f"{lab_id}: run exit {run.returncode}; expected block equals fresh stdout: {exp_text.rstrip() == run.stdout.rstrip()}")
    print(f"{lab_id}: stdout lines {len(run.stdout.splitlines())}, expected lines {len(exp_text.splitlines())}")
