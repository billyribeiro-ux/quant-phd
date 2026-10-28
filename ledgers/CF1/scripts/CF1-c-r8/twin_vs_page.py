"""Compare the code and expected output embedded in L05.html and L06.html with the twins and with a fresh run."""
import html
import re
import subprocess
import sys

ROOT = sys.argv[1]
PAIRS = [("course/modules/CF/CF1/L05.html", "tests/labs/CF1/lab-CF1-L05-1.py"),
         ("course/modules/CF/CF1/L06.html", "tests/labs/CF1/lab-CF1-L06-1.py")]
for page, twin in PAIRS:
    text = open(f"{ROOT}/{page}", encoding="utf-8").read()
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1))
    src = open(f"{ROOT}/{twin}", encoding="utf-8").read()
    print(page, "code identical to twin:", code == src, "lines", len(code.splitlines()))
    run = subprocess.run([sys.executable, "-I", "-W", "error", f"{ROOT}/{twin}"], capture_output=True, text=True).stdout
    print(page, "expected identical to fresh run:", expected.strip() == run.strip(), "lines", len(run.splitlines()))
    if expected.strip() != run.strip():
        for a, b in zip(expected.splitlines(), run.splitlines()):
            if a != b:
                print("DIFF", repr(a), repr(b))
