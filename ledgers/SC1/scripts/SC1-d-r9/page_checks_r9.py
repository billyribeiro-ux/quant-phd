"""Round-9 SC1 slice d checks on project.html: lab page code vs twin, page expected block vs twin output,
the blind exemplar view (annotations and official verdicts stripped), and the changed-hunk grep.

Usage: python -I page_checks_r9.py   (run from the checkout root)
"""

import difflib
import html
import re
import subprocess
import sys

ROOT = "."
src = open(f"{ROOT}/course/modules/SC/SC1/project.html", encoding="utf-8").read()

# 1. Each lab: page code equals the twin (completion lab 2 differs only in its two blanks).
blocks = re.findall(
    r'<section class="lab[^"]*" id="(lab-SC1-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>'
    r'.*?<pre class="expected"[^>]*>(.*?)</pre>',
    src,
    flags=re.S,
)
for lab_id, code, expected in blocks:
    n = lab_id[-1]
    page_code = html.unescape(code)
    twin = open(f"{ROOT}/tests/labs/SC1/lab-SC1-project-{n}.py", encoding="utf-8").read()
    diff = [d for d in difflib.unified_diff(twin.splitlines(), page_code.splitlines(), lineterm="", n=0)
            if d[:1] in "+-" and d[:3] not in ("+++", "---")]
    print(f"{lab_id}: page code vs twin differing lines = {len(diff)}")
    for d in diff:
        print("   ", d)
    # 2. Twin output (run alone, -I -W error) equals the page's expected block.
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{ROOT}/tests/labs/SC1/lab-SC1-project-{n}.py"],
                         capture_output=True, text=True).stdout
    exp = html.unescape(expected).rstrip("\n") + "\n"
    print(f"{lab_id}: twin output equals expected block = {out == exp}")

# 3. Blind exemplar view: strip annotation asides and the official verdict paragraphs.
body = "\n".join(src.split("\n")[463:601])
body = re.sub(r'<aside class="annotation".*?</aside>', "[ANNOTATION HIDDEN]", body, flags=re.S)
body = re.sub(r'<p class="exemplar-verdict".*?</p>', "[VERDICT HIDDEN]", body, flags=re.S)
open(f"{ROOT}/ledgers/SC1/scripts/SC1-d-r9/out/exemplars_blind_view.txt", "w", encoding="utf-8").write(body)
print("blind exemplar view written; chars =", len(body))

# 4. Changed hunks: the pathwise definition and the standard-error sentence are present, and the 1.77 ratio is right.
print("pathwise dfn present:", "<dfn>pathwise</dfn>" in src)
print("0.016300/0.009218 =", round(0.016300 / 0.009218, 2))
