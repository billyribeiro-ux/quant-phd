"""Compare each M2 lab twin (run alone under python -I -W error) with the page code and expected block."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyB7-M2-a")
PY = str(ROOT / ".venv/bin/python")
for n in range(1, 7):
    lid = f"L{n:02d}"
    twin = ROOT / f"tests/labs/M2/lab-M2-{lid}-1.py"
    page = (ROOT / f"course/modules/M/M2/{lid}.html").read_text()
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(code_m.group(1)) if code_m else None
    expected = html.unescape(exp_m.group(1)) if exp_m else None
    twin_src = twin.read_text()
    res = subprocess.run([PY, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd="/tmp")
    out = res.stdout
    print(lid, "exit", res.returncode, "stderr", repr(res.stderr[:200]))
    print("  code==twin:", code is not None and code.rstrip("\n") == twin_src.rstrip("\n"))
    print("  expected==output:", expected is not None and expected.strip() == out.strip())
    if expected is not None and expected.strip() != out.strip():
        print("  EXPECTED:", expected)
        print("  OUTPUT:", out)
