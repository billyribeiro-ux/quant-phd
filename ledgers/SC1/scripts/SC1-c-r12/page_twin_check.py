"""For L07 and L08: the lab code block on the page equals the twin, and the expected block equals the twin's output.

Usage: python -I page_twin_check.py <repo-root> <stdout-dir>   (stdout-dir holds lab_L07.stdout, lab_L08.stdout)
"""
import html
import re
import sys

root, outdir = sys.argv[1], sys.argv[2]
for lesson in ("L07", "L08"):
    text = open(f"{root}/course/modules/SC/SC1/{lesson}.html", encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    twin = open(f"{root}/tests/labs/SC1/lab-SC1-{lesson}-1.py", encoding="utf-8").read()
    print(lesson, "page code equals twin:", html.unescape(code.group(1)).rstrip("\n") == twin.rstrip("\n"))
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    out = open(f"{outdir}/lab_{lesson}.stdout", encoding="utf-8").read()
    print(lesson, "expected equals twin stdout:", html.unescape(exp.group(1)).rstrip("\n") == out.rstrip("\n"))
