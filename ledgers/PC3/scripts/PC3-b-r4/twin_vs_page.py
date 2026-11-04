"""Compare each PC3 L04-L06 page's data-run code and expected block with its lab twin and its real stdout.

Usage: python -I twin_vs_page.py <checkout-root>. Stdlib only; runs each twin under python -I -W error.
"""
import html
import re
import subprocess
import sys
import tempfile
import os

root = sys.argv[1]
for p in ("L04", "L05", "L06"):
    text = open(f"{root}/course/modules/PC/PC3/{p}.html", encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin = open(f"{root}/tests/labs/PC3/lab-PC3-{p}-1.py", encoding="utf-8").read()
    e = re.search(r'<pre class="expected" data-tolerance="[^"]*">(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    print(p, "page code == twin:", code.rstrip("\n") == twin.rstrip("\n"), "len", len(code), len(twin))
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "twin.py")
        open(path, "w", encoding="utf-8").write(twin)
        r = subprocess.run([sys.executable, "-I", "-W", "error", path], capture_output=True, text=True, cwd=d)
        print(p, "twin exit", r.returncode, "stderr bytes", len(r.stderr))
        out = r.stdout
        print(p, "expected == stdout:", expected.rstrip("\n") == out.rstrip("\n"))
        if expected.rstrip("\n") != out.rstrip("\n"):
            import difflib
            for line in difflib.unified_diff(expected.rstrip("\n").splitlines(), out.rstrip("\n").splitlines(), "expected", "stdout", lineterm=""):
                print("   ", line)
        open(f"{os.path.dirname(os.path.abspath(__file__))}/stdout_{p}.out", "w", encoding="utf-8").write(out)
