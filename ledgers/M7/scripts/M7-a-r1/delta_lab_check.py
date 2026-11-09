"""Verifier M7 slice a round 1: page code equals twin text; expected block equals the twin's stdout.

For each lesson page L01-L03: take the first <code data-run> block and the <pre class="expected"> block that
follows it, html-unescape both, compare the code with tests/labs/M7/lab-M7-<L>-1.py byte for byte, run the twin
with python -I -W error and compare its stdout with the expected block exactly. Prints the first differing line
when they differ.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyF21-M7-a")
PY = str(ROOT / ".venv/bin/python")
ok = True
for L in ("L01", "L02", "L03"):
    page = (ROOT / f"course/modules/M/M7/{L}.html").read_text(encoding="utf-8")
    code_m = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page[code_m.end():], re.S)
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin_path = ROOT / f"tests/labs/M7/lab-M7-{L}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    code_eq = code == twin.rstrip(chr(10))  # the page omits only the final newline of the file
    run = subprocess.run([PY, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd=ROOT)
    out = run.stdout
    exp_eq = expected.strip() == out.strip()
    print(f"{L}: code==twin {code_eq} (len {len(code)} vs {len(twin)}); twin exit {run.returncode}; "
          f"expected==stdout {exp_eq} (lines {len(expected.splitlines())} vs {len(out.splitlines())}); stderr {run.stderr.strip()[:200]!r}")
    if not exp_eq:
        for i, (a, b) in enumerate(zip(expected.splitlines(), out.splitlines()), 1):
            if a != b:
                print("  first diff line", i, "expected", repr(a), "stdout", repr(b))
                break
    if not (code_eq and exp_eq and run.returncode == 0):
        ok = False
    if L == "L03":
        print(out)
print("ALL OK" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
