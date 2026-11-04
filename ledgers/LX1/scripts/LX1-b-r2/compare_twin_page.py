"""Compare each lab twin with its page: code block, expected block, and the twin's own output.

Usage: python -I compare_twin_page.py <checkout> <page.html> <twin.py> <run_output.txt>
"""
import html
import re
import sys
from pathlib import Path

checkout, page_rel, twin_rel, run_out = sys.argv[1:5]
page = Path(checkout, page_rel).read_text(encoding="utf-8")
twin = Path(checkout, twin_rel).read_text(encoding="utf-8")
run = Path(run_out).read_text(encoding="utf-8")

code_blocks = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
expected_blocks = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
print("code blocks:", len(code_blocks), "expected blocks:", len(expected_blocks))
code = html.unescape(code_blocks[0])
exp = html.unescape(expected_blocks[0])
print("code == twin (exact):", code == twin)
print("code == twin (rstrip of trailing newline):", code.rstrip("\n") == twin.rstrip("\n"))
print("trailing newline in twin:", twin.endswith("\n"), "in page block:", code.endswith("\n"))
print("expected == run output (exact):", exp == run)
print("expected == run output (rstrip):", exp.rstrip("\n") == run.rstrip("\n"))
print("expected lines:", len(exp.splitlines()), "run lines:", len(run.splitlines()))
for i, (a, b) in enumerate(zip(exp.splitlines(), run.splitlines()), 1):
    if a != b:
        print("DIFF line", i, "\n  page:", a, "\n  run: ", b)
