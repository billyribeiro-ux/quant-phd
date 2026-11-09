"""Compare each LX1 lab page's embedded code and expected block with its twin and with the twin's output."""
import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PY = ROOT / ".venv/bin/python"
for lab in ("L01", "L02"):
    page = (ROOT / f"course/modules/LX/LX1/{lab}.html").read_text(encoding="utf-8")
    twin = (ROOT / f"tests/labs/LX1/lab-LX1-{lab}-1.py").read_text(encoding="utf-8")
    m = re.search(
        r'<section class="lab" id="lab-LX1-%s-1".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>' % lab,
        page,
        re.S,
    )
    if not m:
        print(lab, "NO LAB BLOCK FOUND")
        continue
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    print(lab, "page code == twin (trailing newline ignored):", code.rstrip("\n") == twin.rstrip("\n"), "| exact:", code == twin)
    if code.rstrip("\n") != twin.rstrip("\n"):
        print("\n".join(difflib.unified_diff(twin.rstrip("\n").splitlines(), code.rstrip("\n").splitlines(), "twin", "page", lineterm="")))
    out = subprocess.run([str(PY), "-I", "-W", "error", str(ROOT / f"tests/labs/LX1/lab-LX1-{lab}-1.py")], capture_output=True, text=True, cwd=ROOT).stdout
    print(lab, "expected block == twin output:", expected.rstrip("\n") == out.rstrip("\n"))
    if expected.rstrip("\n") != out.rstrip("\n"):
        print("\n".join(difflib.unified_diff(out.rstrip("\n").splitlines(), expected.rstrip("\n").splitlines(), "output", "expected", lineterm="")))
