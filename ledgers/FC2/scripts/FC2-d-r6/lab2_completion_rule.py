"""Check the completion rule for Lab 2: every page line equals the twin line or contains a blank (___).

Usage: python3 -I ledgers/FC2/scripts/FC2-d-r5/lab2_completion_rule.py <repo_root>
"""

import html
import os
import re
import sys

root = sys.argv[1]
page = open(os.path.join(root, "course", "modules", "FC", "FC2", "project.html"), encoding="utf-8").read()
start = page.index('id="lab-FC2-project-2"')
cm = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page[start:], re.S)
code = html.unescape(cm.group(1)).rstrip("\n").split("\n")
twin = open(os.path.join(root, "tests", "labs", "FC2", "lab-FC2-project-2.py"), encoding="utf-8").read()
twin = twin.rstrip("\n").split("\n")
print("page lines", len(code), "twin lines", len(twin))
bad = []
blanks = []
for i, (p, t) in enumerate(zip(code, twin), start=1):
    if p == t:
        continue
    if "___" in p:
        blanks.append((i, p.strip(), t.strip()))
    else:
        bad.append((i, p, t))
for b in blanks:
    print("blank line", b[0], "| page:", b[1], "| twin:", b[2])
print("lines differing without a blank:", bad)
print("rule holds:", not bad and len(code) == len(twin))
