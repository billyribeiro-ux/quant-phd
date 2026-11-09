"""Round-4 check: page code equals twin, expected block equals twin stdout, twin stderr empty (M5 L08-L10)."""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PY = str(ROOT / ".venv" / "bin" / "python")
ok_all = True
for page in ("L08", "L09", "L10"):
    text = (ROOT / f"course/modules/M/M5/{page}.html").read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1))
    twin = (ROOT / f"tests/labs/M5/lab-M5-{page}-1.py").read_text(encoding="utf-8")
    same_code = code.strip() == twin.strip()
    run = subprocess.run([PY, "-I", "-W", "error", str(ROOT / f"tests/labs/M5/lab-M5-{page}-1.py")],
                         capture_output=True, text=True, cwd="/tmp")
    same_out = run.stdout.strip() == expected.strip()
    print(f"{page}: code_equals_twin={same_code} expected_equals_stdout={same_out} exit={run.returncode} stderr_bytes={len(run.stderr)}")
    if not (same_code and same_out and run.returncode == 0 and not run.stderr):
        ok_all = False
        import difflib
        if not same_code:
            print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:60]))
        if not same_out:
            print("".join(list(difflib.unified_diff(expected.splitlines(True), run.stdout.splitlines(True), "expected", "stdout"))[:60]))
print("RESULT", "PASS" if ok_all else "FAIL")
sys.exit(0 if ok_all else 1)
