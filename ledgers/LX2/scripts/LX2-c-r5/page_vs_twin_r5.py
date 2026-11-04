"""Compare each project lab's page code and expected block with its twin and its real output."""
import html
import re
import subprocess
import sys

PAGE = "course/modules/LX/LX2/project.html"
TWINS = {1: "tests/labs/LX2/lab-LX2-project-1.py", 2: "tests/labs/LX2/lab-LX2-project-2.py",
         3: "tests/labs/LX2/lab-LX2-project-3.py"}
page = open(PAGE, encoding="utf-8").read()
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, flags=re.S)
print("lab blocks found:", len(blocks))
for n, (code_html, expected_html) in enumerate(blocks, 1):
    code = html.unescape(code_html)
    expected = html.unescape(expected_html)
    twin = open(TWINS[n], encoding="utf-8").read()
    print(f"lab {n}: page code == twin: {code.rstrip() == twin.rstrip()}")
    if code.rstrip() != twin.rstrip():
        import difflib
        for line in difflib.unified_diff(twin.rstrip().splitlines(), code.rstrip().splitlines(), "twin", "page", lineterm=""):
            print("   ", line)
    out = subprocess.run([sys.executable, "-I", "-W", "error", TWINS[n]], capture_output=True, text=True)
    print(f"lab {n}: twin stdout == expected block: {out.stdout.rstrip() == expected.rstrip()} (exit {out.returncode}, stderr bytes {len(out.stderr)})")
