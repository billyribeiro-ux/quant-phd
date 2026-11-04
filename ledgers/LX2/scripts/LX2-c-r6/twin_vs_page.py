"""For each project lab: page code (unescaped) vs twin file, twin run under python -I -W error, twin stdout vs page
expected block. Lab 2 page code has ___ blanks: its twin is the completed solution, so the comparison is line by line
(each page line equals the twin line or contains a blank) and the twin output must equal the expected block.

Usage: python3 -I twin_vs_page.py <repo_root>
"""
import html
import os
import re
import subprocess
import sys
import tempfile

root = sys.argv[1]
page = open(os.path.join(root, "course/modules/LX/LX2/project.html"), encoding="utf-8").read()
for lab_id in ["lab-LX2-project-1", "lab-LX2-project-2", "lab-LX2-project-3"]:
    m = re.search(
        r'<section class="lab[^"]*" id="%s"[^>]*>.*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*'
        r'<pre class="expected"[^>]*>(.*?)</pre>' % lab_id,
        page,
        flags=re.S,
    )
    assert m, lab_id
    code_page = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin_path = os.path.join(root, "tests/labs/LX2", lab_id + ".py")
    twin = open(twin_path, encoding="utf-8").read()
    twin_nl = twin.rstrip("\n")
    code_nl = code_page.rstrip("\n")
    if "___" in code_nl:
        pl = code_nl.split("\n")
        tl = twin_nl.split("\n")
        ok_lines = len(pl) == len(tl) and all(p == t or "___" in p for p, t in zip(pl, tl))
        print(f"{lab_id}: completion lab, page lines={len(pl)} twin lines={len(tl)} line-rule ok={ok_lines}")
        blanks = [p.strip() for p in pl if "___" in p]
        print(f"  blank lines on page: {blanks}")
        print(f"  twin lines at those positions: {[tl[i].strip() for i,p in enumerate(pl) if '___' in p]}")
    else:
        print(f"{lab_id}: page code == twin: {code_nl == twin_nl}")
    with tempfile.TemporaryDirectory() as scratch:
        proc = subprocess.run(
            [sys.executable, "-I", "-W", "error", twin_path],
            cwd=scratch, capture_output=True, text=True, timeout=60,
        )
    print(f"  rc={proc.returncode} stderr={proc.stderr!r}")
    out = proc.stdout.rstrip("\n")
    exp = expected.rstrip("\n")
    print(f"  twin stdout == page expected block: {out == exp}")
    if out != exp:
        print("  DIFF:")
        for a, b in zip(out.split("\n"), exp.split("\n")):
            if a != b:
                print("   out:", a, "| exp:", b)
    print("  output:")
    for line in out.split("\n"):
        print("   |", line)
