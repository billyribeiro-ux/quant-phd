"""Round-14 SC1-a check: page code equals twin, expected block equals twin stdout (run alone, -I -W error, empty cwd)."""
import html
import os
import re
import subprocess
import sys
import tempfile

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE14-SC1-a"
PY = os.path.join(ROOT, ".venv/bin/python")
PAGES = {"L01": "lab-SC1-L01-1", "L02": "lab-SC1-L02-1", "L03": "lab-SC1-L03-1"}

for page, lab in PAGES.items():
    src = open(os.path.join(ROOT, "course/modules/SC/SC1", page + ".html"), encoding="utf-8").read()
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin_path = os.path.join(ROOT, "tests/labs/SC1", lab + ".py")
    twin = open(twin_path, encoding="utf-8").read()
    print(f"{page}: page code == twin: {code.strip() == twin.strip()} (page {len(code)} chars, twin {len(twin)} chars)")
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([PY, "-I", "-W", "error", twin_path], cwd=d, capture_output=True, text=True)
    out = r.stdout
    print(f"{page}: twin rc={r.returncode} stderr={r.stderr.strip()!r}")
    print(f"{page}: expected block == twin stdout: {expected.strip() == out.strip()}")
    if expected.strip() != out.strip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.strip().splitlines(), out.strip().splitlines(), lineterm="")))
    print(out)
