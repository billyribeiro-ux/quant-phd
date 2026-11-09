"""Compare each project lab's page code block (data-run) with its twin, and its expected block with the twin's output."""

import html
import re
import subprocess
import sys

root = sys.argv[1]
page = open(f"{root}/course/modules/E/E3/project.html", encoding="utf-8").read()
blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, flags=re.S)
expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, flags=re.S)
print("code blocks:", len(blocks), "expected blocks:", len(expected))
for i, block in enumerate(blocks, start=1):
    code = html.unescape(block)
    twin = open(f"{root}/tests/labs/E3/lab-E3-project-{i}.py", encoding="utf-8").read()
    print(f"lab {i}: page code == twin:", code.strip() == twin.strip(), "| page lines", len(code.splitlines()), "twin lines", len(twin.splitlines()))
    if i == 2:
        print("  (lab 2 page has blanks: ___ count =", code.count("___"), ")")
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/E3/lab-E3-project-{i}.py"], capture_output=True, text=True).stdout
    print(f"lab {i}: expected block == twin output:", html.unescape(expected[i - 1]).strip() == out.strip())
