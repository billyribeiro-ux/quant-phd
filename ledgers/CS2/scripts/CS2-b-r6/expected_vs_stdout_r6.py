"""Verifier round 6: compare each CS2 L05-L08 expected block with the twin's stdout, token for token."""
import html
import re
import subprocess
import sys

root = sys.argv[1]
for n in (5, 6, 7, 8):
    page = open(f"{root}/course/modules/CS/CS2/L0{n}.html", encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    exp = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    line_no = page[: m.start()].count("\n") + 1
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/CS2/lab-CS2-L0{n}-1.py"],
                         capture_output=True, text=True, cwd="/tmp").stdout
    e, o = exp.strip().splitlines(), out.strip().splitlines()
    diffs = [(k, x, y) for k, (x, y) in enumerate(zip(e, o), 1) if x != y]
    print(f"L0{n}: expected starts line {line_no}, exp lines {len(e)}, stdout lines {len(o)}, equal={e == o}, diffs={diffs[:3]}")
