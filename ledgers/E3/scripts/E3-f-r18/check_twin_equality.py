"""Round-14: compare each lab's page code (HTML-unescaped) with its twin file, byte for byte, and
compare the expected block with the twin's stdout run under python -I -W error."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for page in ("L01", "L02", "L03", "L04"):
    src = (root / f"course/modules/E/E3/{page}.html").read_text(encoding="utf-8")
    sections = re.findall(r'<section class="lab" id="(lab-E3-[^"]+)".*?<code class="language-python" data-run>(.*?)</code></pre>.*?<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    for lab_id, code, expected in sections:
        twin = root / "tests/labs/E3" / f"{lab_id}.py"
        twin_text = twin.read_text(encoding="utf-8")
        page_code = html.unescape(code)
        same = page_code.rstrip("\n") == twin_text.rstrip("\n")
        run = subprocess.run([str(root / ".venv/bin/python"), "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd=root)
        exp = html.unescape(expected)
        out_ok = run.stdout.rstrip("\n") == exp.rstrip("\n")
        print(f"{page} {lab_id} page_code_equals_twin={same} expected_equals_stdout={out_ok} rc={run.returncode} stderr={run.stderr.strip()[:200]!r}")
