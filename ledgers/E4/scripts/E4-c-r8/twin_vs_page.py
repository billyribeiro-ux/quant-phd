"""Compare each E4 slice page's embedded lab code and expected block with its twin and with the twin's live output.

Usage: python twin_vs_page.py <repo_root> <output_dir_with_twin_outputs>
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
outdir = Path(sys.argv[2])
pairs = [("L07", "lab-E4-L07-1"), ("L08", "lab-E4-L08-1"), ("L09", "lab-E4-L09-1")]
for page, lab in pairs:
    text = (root / f"course/modules/E/E4/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code = html.unescape(m.group(1))
    twin = (root / f"tests/labs/E4/{lab}.py").read_text(encoding="utf-8")
    code_eq = code == twin
    print(f"{page} code_equals_twin {code_eq} page_chars {len(code)} twin_chars {len(twin)} page_lines {code.count(chr(10))} twin_lines {twin.count(chr(10))}")
    if not code_eq:
        import difflib
        for line in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""):
            print("   ", line)
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1))
    out = (outdir / f"twin_{lab.replace('lab-E4-', '')}.out").read_text(encoding="utf-8")
    out_lines = [l for l in out.splitlines() if not l.startswith("exit ")]
    exp_lines = expected.splitlines()
    eq = exp_lines == out_lines
    print(f"{page} expected_equals_output {eq} expected_lines {len(exp_lines)} output_lines {len(out_lines)}")
    if not eq:
        import difflib
        for line in difflib.unified_diff(out_lines, exp_lines, "output", "expected", lineterm=""):
            print("   ", line)
