"""SC1-a round 18: page lab code equals the twin file; the expected block equals the twin's stdout (run under -I -W error)."""

import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
for n in (1, 2, 3):
    page = (ROOT / f"course/modules/SC/SC1/L0{n}.html").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab"[^>]*>.*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin = (ROOT / f"tests/labs/SC1/lab-SC1-L0{n}-1.py").read_text(encoding="utf-8")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/SC1/lab-SC1-L0{n}-1.py")], capture_output=True, text=True, cwd="/tmp")
    print(f"L0{n}: page code == twin: {code.strip() == twin.strip()}; twin rc={run.returncode}; stderr bytes={len(run.stderr)}; "
          f"expected == stdout: {expected.strip() == run.stdout.strip()}")
