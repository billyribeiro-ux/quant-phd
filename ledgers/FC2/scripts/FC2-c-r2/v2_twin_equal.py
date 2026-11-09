"""Byte-compare each page's lab code and expected block with its twin and with the twin's live stdout."""
import html
import re
import subprocess
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyS2-FC2-c"
PAIRS = [("L07", "lab-FC2-L07-1"), ("L08", "lab-FC2-L08-1")]
for page, lab in PAIRS:
    src = open(f"{ROOT}/course/modules/FC/FC2/{page}.html", encoding="utf-8").read()
    m = re.search(r'<section class="lab"[^>]*id="%s"[^>]*>.*?<pre><code[^>]*data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>' % lab, src, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin = open(f"{ROOT}/tests/labs/FC2/{lab}.py", encoding="utf-8").read()
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{ROOT}/tests/labs/FC2/{lab}.py"], capture_output=True, text=True, cwd="/tmp").stdout
    print(page, "code_equal_twin:", code.rstrip("\n") == twin.rstrip("\n"), "len", len(code), len(twin))
    print(page, "expected_equal_stdout:", expected.rstrip("\n") == out.rstrip("\n"))
    if expected.rstrip("\n") != out.rstrip("\n"):
        import difflib
        print("\n".join(difflib.unified_diff(expected.splitlines(), out.splitlines(), lineterm="")))
