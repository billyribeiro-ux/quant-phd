"""M2-d2 r10: page code block == twin (byte, trailing newlines aside); expected block == live stdout (exact text).

Usage (checkout root): .venv/bin/python ledgers/M2/scripts/M2-d2-r10/lab_equalities.py
Live stdout is taken from running each twin under python -I -W error in an empty temp directory.
"""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
PY = str(ROOT / ".venv" / "bin" / "python")
ok = True
for L in ["L22", "L23", "L24"]:
    page = (ROOT / f"course/modules/M/M2/{L}.html").read_text(encoding="utf-8")
    twin = (ROOT / f"tests/labs/M2/lab-M2-{L}-1.py").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    code_eq = code.rstrip("\n") == twin.rstrip("\n")
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1))
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([PY, "-I", "-W", "error", str(ROOT / f"tests/labs/M2/lab-M2-{L}-1.py")],
                           cwd=d, capture_output=True, text=True)
    live = r.stdout
    exp_eq = expected.rstrip("\n") == live.rstrip("\n")
    ok = ok and code_eq and exp_eq and r.returncode == 0 and r.stderr == ""
    print(f"{L}: code-block==twin {code_eq} (code {len(code)} chars, twin {len(twin)}); "
          f"expected==live {exp_eq} (exit {r.returncode}, stderr {len(r.stderr)} bytes, {live.count(chr(10))} lines)")
    if not exp_eq:
        print("  expected-only:", [x for x in expected.splitlines() if x not in live.splitlines()])
        print("  live-only:", [x for x in live.splitlines() if x not in expected.splitlines()])
print("ALL EQUAL" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
