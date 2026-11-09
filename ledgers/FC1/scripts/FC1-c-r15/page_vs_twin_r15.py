"""Round 15, FC1-c: compare each project-page run block with its lab twin, and each twin's output with the page's expected block.

Usage: python -I page_vs_twin_r15.py <checkout>   (run from any directory; prints one line per lab)
A page block must equal its twin, except that the completion lab's blanks (___) replace the twin's expressions.
"""

import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

checkout = Path(sys.argv[1])
page = (checkout / "course/modules/FC/FC1/project.html").read_text(encoding="utf-8")
runs = re.findall(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
expected = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
twins = ["lab-FC1-project-1.py", "lab-FC1-project-2.py", "lab-FC1-project-3.py"]
python = checkout / ".venv/bin/python"
assert len(runs) == len(expected) == len(twins) == 3, (len(runs), len(expected))
for i, (block, exp, twin) in enumerate(zip(runs, expected, twins), start=1):
    code = html.unescape(block)
    twin_text = (checkout / "tests/labs" / "FC1" / twin).read_text(encoding="utf-8")
    diff = [l for l in difflib.unified_diff(twin_text.splitlines(), code.splitlines(), lineterm="") if l[:1] in "+-" and l[:3] not in ("+++", "---")]
    run = subprocess.run([str(python), "-I", "-W", "error", str(checkout / "tests/labs/FC1" / twin)],
                         capture_output=True, text=True, timeout=120)
    same_output = run.stdout.rstrip("\n") == html.unescape(exp).rstrip("\n")
    print(f"{twin}: rc={run.returncode} output==expected: {same_output}; page block vs twin differing lines: {len(diff) // 2}")
    for line in diff:
        print("   ", line)
