# Usage: python -I this.py <checkout-root>. Compares each slice page's data-run code with its twin, runs each twin
# alone under python -I -W error in an empty scratch directory, and compares the expected block with stdout.
import html
import os
import re
import subprocess
import sys
import tempfile

root = os.path.abspath(sys.argv[1])
py = os.path.join(root, ".venv", "bin", "python")
pages = {"L22": "course/modules/M/M2/L22.html", "L23": "course/modules/M/M2/L23.html", "L24": "course/modules/M/M2/L24.html"}
for name, rel in pages.items():
    text = open(os.path.join(root, rel), encoding="utf-8").read()
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin_path = os.path.join(root, "tests/labs/M2/lab-M2-%s-1.py" % name)
    twin = open(twin_path, encoding="utf-8").read()
    print(name, "page code == twin strict:", code == twin, "| modulo final newline:", code.rstrip("\n") == twin.rstrip("\n"), "| code lines", code.count("\n"), "twin lines", twin.count("\n"))
    if code != twin:
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True)))[:40]))
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([py, "-I", "-W", "error", twin_path], cwd=d, capture_output=True, text=True)
    print(name, "twin alone rc", r.returncode, "stderr bytes", len(r.stderr.encode()))
    print(name, "expected == stdout strict:", expected == r.stdout, "| modulo final newline:", expected.rstrip("\n") == r.stdout.rstrip("\n"), "| expected lines", expected.count("\n") + 1,
          "stdout lines", r.stdout.count("\n"))
    if expected != r.stdout:
        import difflib
        print("".join(difflib.unified_diff(expected.splitlines(True), r.stdout.splitlines(True), "expected", "stdout")))
    # block must also be byte-compared for trailing newline
    print(name, "repr tail expected", repr(expected[-30:]), "stdout", repr(r.stdout[-30:]))
