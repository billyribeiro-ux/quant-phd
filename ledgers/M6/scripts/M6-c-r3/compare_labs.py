"""Compare each L09-L12 page's lab code and expected block with its twin and twin output."""
import html
import re
import subprocess
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyC3-M6-c"
for page in ("L09", "L10", "L11", "L12"):
    src = open(f"{ROOT}/course/modules/M/M6/{page}.html", encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S).group(1)
    code = html.unescape(code)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S).group(1)
    expected = html.unescape(expected)
    twin = open(f"{ROOT}/tests/labs/M6/lab-M6-{page}-1.py", encoding="utf-8").read()
    print(page, "code==twin:", code.rstrip("\n") == twin.rstrip("\n"), "twin_len", len(twin))
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{ROOT}/tests/labs/M6/lab-M6-{page}-1.py"],
                         capture_output=True, text=True).stdout
    print(page, "expected==output:", expected.strip() == out.strip())
    if expected.strip() != out.strip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.strip().splitlines(), out.strip().splitlines(), lineterm="")))
