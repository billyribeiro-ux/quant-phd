"""Round-4 check for M5 slice b: page code equals twin; twin runs alone under python -I -W error; expected equals output."""
import html
import os
import re
import subprocess
import sys
import tempfile

ROOT = "/Users/billyribeiro/.fanout/wt/verifyS4-M5-b"
PY = os.path.join(ROOT, ".venv/bin/python")
LABS = {
    "L05": ("lab-M5-L05-1", "course/modules/M/M5/L05.html"),
    "L06": ("lab-M5-L06-1", "course/modules/M/M5/L06.html"),
    "L07": ("lab-M5-L07-1", "course/modules/M/M5/L07.html"),
}
for page, (lab, path) in LABS.items():
    src = open(os.path.join(ROOT, path), encoding="utf-8").read()
    twin = open(os.path.join(ROOT, "tests/labs/M5", lab + ".py"), encoding="utf-8").read()
    m = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    code = html.unescape(m.group(1))
    print(f"{page}: page code equals twin: {code == twin}  (len page {len(code)}, twin {len(twin)})")
    if code != twin:
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True)))[:40]))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(e.group(1))
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "twin.py"), "w", encoding="utf-8").write(twin)
        r = subprocess.run([PY, "-I", "-W", "error", "twin.py"], cwd=d, capture_output=True, text=True)
    print(f"{page}: twin rc={r.returncode} stderr={r.stderr!r}")
    print(f"{page}: expected equals output: {expected.strip() == r.stdout.strip()}")
    if expected.strip() != r.stdout.strip():
        print("OUTPUT:\n" + r.stdout)
    else:
        print("OUTPUT (first 3 lines):", r.stdout.splitlines()[:3])
    print("-" * 40)
