"""Round 7: compare each lesson's embedded lab code and expected block with its twin (independent of embed_labs)."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
for lesson in ("L01", "L02", "L03"):
    page = (ROOT / f"course/modules/PC/PC3/{lesson}.html").read_text(encoding="utf-8")
    twin_path = ROOT / f"tests/labs/PC3/lab-PC3-{lesson}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    m_code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    m_exp = re.search(r'<pre class="expected" data-tolerance="([^"]*)">(.*?)</pre>', page, re.S)
    code = html.unescape(m_code.group(1))
    expected = html.unescape(m_exp.group(2))
    stdout = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd=ROOT
    ).stdout
    code_eq = code.rstrip("\n") == twin.rstrip("\n")
    exp_eq = expected.rstrip("\n") == stdout.rstrip("\n")
    print(f"{lesson}: page code == twin (trailing newline ignored): {code_eq} (page {len(code)} chars, twin {len(twin)})")
    print(f"{lesson}: expected == twin stdout (trailing newline ignored): {exp_eq} (expected lines {len(expected.splitlines())}, stdout lines {len(stdout.splitlines())})")
    print(f"{lesson}: data-tolerance={m_exp.group(1)}; placeholders left in page: {'@@LAB' in page or '@@OUT' in page}")
    print(f"{lesson}: twin ends with newline: {twin.endswith(chr(10))}; page code ends with newline: {code.endswith(chr(10))}")
