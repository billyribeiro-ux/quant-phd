"""Compare each lab page's code block and expected block with its twin and the twin's stdout (verifier r3)."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PY = str(ROOT / ".venv" / "bin" / "python")
for lab in ("L01", "L02", "L03"):
    page = (ROOT / f"course/modules/E/E1/{lab}.html").read_text(encoding="utf-8")
    twin = (ROOT / f"tests/labs/E1/lab-E1-{lab}-1.py").read_text(encoding="utf-8")
    sec = re.search(r'<section class="lab" id="lab-E1-%s-1".*?</section>' % lab, page, re.S).group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    out = subprocess.run([PY, "-I", "-W", "error", "-c", "import sys; sys.argv=['x']"], capture_output=True, text=True)
    run = subprocess.run([PY, "-I", "-W", "error", str(ROOT / f"tests/labs/E1/lab-E1-{lab}-1.py")],
                         capture_output=True, text=True, cwd="/tmp")
    print(f"{lab}: page code == twin: {code.rstrip(chr(10)) == twin.rstrip(chr(10))} (len page {len(code)}, twin {len(twin)})")
    print(f"{lab}: expected == twin stdout: {expected.rstrip(chr(10)) == run.stdout.rstrip(chr(10))}; exit {run.returncode}; stderr {run.stderr!r}")
    print(f"{lab}: expected lines {len(expected.splitlines())}")
