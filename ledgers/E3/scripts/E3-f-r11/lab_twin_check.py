"""E3 slice f round 11: page lab code equals the twin, the twin runs alone under python -I -W error, and the
expected block equals the twin's printed output. Run from the checkout root with .venv/bin/python -I."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(".")
for n in range(1, 5):
    page = ROOT / f"course/modules/E/E3/L0{n}.html"
    text = page.read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="lab-E3-L0%d-1"[^>]*>(.*?)</section>' % n, text, re.S)
    block = m.group(1)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', block, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', block, re.S).group(1))
    twin_path = ROOT / f"tests/labs/E3/lab-E3-L0{n}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    print(f"L0{n}: page code == twin: {code.strip() == twin.strip()} (page {len(code)} chars, twin {len(twin)} chars)")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path.resolve())], capture_output=True, text=True, cwd="/tmp")
    print(f"L0{n}: twin alone exit {run.returncode}, stderr bytes {len(run.stderr)}")
    print(f"L0{n}: expected block == printed output: {expected.strip() == run.stdout.strip()}")
    if expected.strip() != run.stdout.strip():
        print("DIFF", expected.strip()[:300], "|||", run.stdout.strip()[:300])
