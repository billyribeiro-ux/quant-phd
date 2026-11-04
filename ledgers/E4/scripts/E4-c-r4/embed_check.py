"""E4-c round 3: compare each lab's embedded expected block and code block with its twin and its standalone output.

Usage: python -I embed_check.py <checkout-root>. Standard library only.
"""
import html
import os
import re
import subprocess
import sys

root = sys.argv[1]
os.chdir(root)
for t in ("L07", "L08", "L09"):
    page = f"course/modules/E/E4/{t}.html"
    twin = f"tests/labs/E4/lab-E4-{t}-1.py"
    src = open(page, encoding="utf-8").read()
    twin_src = open(twin, encoding="utf-8").read()
    code_blocks = re.findall(r"<pre><code class=\"language-python\" data-run>(.*?)</code></pre>", src, re.S)
    exp_blocks = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    code_ok = [html.unescape(c).strip() == twin_src.strip() for c in code_blocks]
    out = subprocess.run([sys.executable, "-I", "-W", "error", os.path.join(root, twin)], capture_output=True, text=True, cwd="/tmp")
    exp_ok = [html.unescape(e).strip() == out.stdout.strip() for e in exp_blocks]
    print(t, "code blocks:", len(code_blocks), code_ok, "| expected blocks:", len(exp_blocks), exp_ok, "| twin exit", out.returncode, "stderr bytes", len(out.stderr))
