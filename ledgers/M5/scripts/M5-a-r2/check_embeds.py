"""Verify, for each slice lesson page, that each lab's code equals its twin and its expected block equals the twin's output."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PY = str(ROOT / ".venv/bin/python")
for page in ["L01", "L02", "L03", "L04"]:
    text = (ROOT / f"course/modules/M/M5/{page}.html").read_text(encoding="utf-8")
    secs = re.findall(r'<section class="lab"[^>]*id="(lab-M5-(L0\d)-(\d))"[^>]*>(.*?)</section>', text, re.S)
    for lab_id, _, n, body in secs:
        code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
        exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
        code = html.unescape(code_m.group(1))
        expected = html.unescape(exp_m.group(1))
        twin = (ROOT / f"tests/labs/M5/lab-M5-{page}-{n}.py").read_text(encoding="utf-8")
        out = subprocess.run([PY, "-I", "-W", "error", str(ROOT / f"tests/labs/M5/lab-M5-{page}-{n}.py")],
                             capture_output=True, text=True, cwd=str(ROOT)).stdout
        print(f"{lab_id}: code==twin {code.strip() == twin.strip()} ; expected==output {expected.strip() == out.strip()} ; "
              f"code_lines={code.count(chr(10))+1} twin_lines={twin.count(chr(10))+1} expected_lines={expected.count(chr(10))+1}")
        if code.strip() != twin.strip():
            import difflib
            print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:60]))
        if expected.strip() != out.strip():
            import difflib
            print("".join(list(difflib.unified_diff(out.splitlines(True), expected.splitlines(True), "output", "expected"))[:60]))
