"""PC3 slice a, round 8: page lab code == twin (trailing newline ignored); expected block == twin stdout (python -I)."""
import html
import re
import subprocess
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE8-PC3-a"
for lid, page in [("L01", "L01"), ("L02", "L02"), ("L03", "L03")]:
    page_html = open(f"{ROOT}/course/modules/PC/PC3/{page}.html", encoding="utf-8").read()
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page_html, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page_html, re.S).group(1))
    twin = open(f"{ROOT}/tests/labs/PC3/lab-PC3-{lid}-1.py", encoding="utf-8").read()
    print(f"{lid}: page code == twin: {code.rstrip(chr(10)) == twin.rstrip(chr(10))}")
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{ROOT}/tests/labs/PC3/lab-PC3-{lid}-1.py"],
                         capture_output=True, text=True, cwd="/tmp")
    print(f"{lid}: twin exit {out.returncode}; expected == twin stdout: {expected.rstrip(chr(10)) == out.stdout.rstrip(chr(10))}; lines {len(expected.splitlines())}")
    if expected.rstrip(chr(10)) != out.stdout.rstrip(chr(10)):
        print("  DIFF stdout:", out.stdout[:400])
