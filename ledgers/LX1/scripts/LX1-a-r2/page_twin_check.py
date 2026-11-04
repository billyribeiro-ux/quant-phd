"""Compare each lab's page code block with its twin file, and each expected block with the twin's real output."""
import html
import re
import subprocess
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE2-LX1-a"
PAGES = {"L01": ("L01-1", "L01"), "L02": ("L02-1", "L02")}
for page, (lab, _) in PAGES.items():
    text = open(f"{ROOT}/course/modules/LX/LX1/{page}.html", encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    page_code = html.unescape(code.group(1))
    twin = open(f"{ROOT}/tests/labs/LX1/lab-LX1-{lab}.py", encoding="utf-8").read()
    print(f"{page}: page code == twin: {page_code == twin} (page {len(page_code)} chars, twin {len(twin)} chars)")
    if page_code != twin:
        import difflib
        for line in list(difflib.unified_diff(twin.splitlines(), page_code.splitlines(), lineterm=""))[:40]:
            print("   ", line)
    run = subprocess.run([sys.executable, "-I", "-W", "error", f"{ROOT}/tests/labs/LX1/lab-LX1-{lab}.py"],
                         capture_output=True, text=True)
    exp = html.unescape(expected.group(1))
    print(f"{page}: twin exit {run.returncode}, stderr {len(run.stderr)} bytes")
    print(f"{page}: expected block == twin stdout: {exp.strip() == run.stdout.strip()}")
    if exp.strip() != run.stdout.strip():
        import difflib
        for line in list(difflib.unified_diff(exp.strip().splitlines(), run.stdout.strip().splitlines(), lineterm=""))[:40]:
            print("   ", line)

for page, (lab, _) in PAGES.items():
    text = open(f"{ROOT}/course/modules/LX/LX1/{page}.html", encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    page_code = html.unescape(code.group(1))
    twin = open(f"{ROOT}/tests/labs/LX1/lab-LX1-{lab}.py", encoding="utf-8").read()
    print(f"{page}: page code == twin after removing the final newline only: {page_code == twin.rstrip(chr(10))}")
    print(f"{page}: twin ends with newline: {twin.endswith(chr(10))}; page code ends with newline: {page_code.endswith(chr(10))}")
