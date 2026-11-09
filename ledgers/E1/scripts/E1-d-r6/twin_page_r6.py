"""Compare each E1 project lab's page code block with its twin, and its expected block with the twin's output."""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PAGE = ROOT / "course/modules/E/E1/project.html"
LABS = ["lab-E1-project-1", "lab-E1-project-2", "lab-E1-project-3", "lab-E1-L04-1"]
text = PAGE.read_text(encoding="utf-8")
pages = {"lab-E1-L04-1": ROOT / "course/modules/E/E1/L04.html"}
for lab in LABS:
    src = pages.get(lab, PAGE).read_text(encoding="utf-8")
    sec = re.search(r'<section[^>]*id="%s"[^>]*>(.*?)</section>' % lab, src, re.S)
    if not sec:
        print(lab, "NO SECTION")
        continue
    body = sec.group(1)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    code_text = html.unescape(code.group(1))
    exp_text = html.unescape(exp.group(1))
    twin = (ROOT / "tests/labs/E1" / f"{lab.replace('lab-E1-', 'lab-E1-')}.py").read_text(encoding="utf-8")
    twin_code_lines = twin.rstrip("\n").split("\n")
    page_lines = code_text.rstrip("\n").split("\n")
    same = twin_code_lines == page_lines
    print(f"{lab}: page code == twin: {same} (page {len(page_lines)} lines, twin {len(twin_code_lines)} lines)")
    if not same:
        import difflib

        for line in difflib.unified_diff(twin_code_lines, page_lines, "twin", "page", lineterm=""):
            print(line)
    out = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(ROOT / "tests/labs/E1" / f"{lab}.py")],
        capture_output=True,
        text=True,
    )
    print(f"{lab}: twin run exit {out.returncode}; output == expected block: {out.stdout.rstrip() == exp_text.rstrip()}")
    if out.stdout.rstrip() != exp_text.rstrip():
        print("STDOUT:", out.stdout)
        print("STDERR:", out.stderr)
