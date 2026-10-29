"""Compare each lab's page code and expected block with its twin and with the twin's observed output."""
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
for n in range(1, 5):
    page = (ROOT / f"course/modules/M/M6/L0{n}.html").read_text(encoding="utf8")
    twin_path = ROOT / f"tests/labs/M6/lab-M6-L0{n}-1.py"
    twin = twin_path.read_text(encoding="utf8")
    m = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(exp.group(1))
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True)
    observed = out.stdout
    print(f"L0{n}: page code == twin: {code.strip() == twin.strip()} (page {len(code)} chars, twin {len(twin)} chars)")
    print(f"L0{n}: expected == observed stdout: {expected.strip() == observed.strip()} exit={out.returncode} stderr={out.stderr.strip()[:200]!r}")
    if expected.strip() != observed.strip():
        import difflib
        for line in difflib.unified_diff(expected.strip().splitlines(), observed.strip().splitlines(), lineterm=""):
            print("   ", line)
