"""Round-12 verifier (M3 slice d): for each project lab, compare the page's data-run code with its twin, run the twin
under python -I -W error, and compare its stdout with the page's expected block. Run from the checkout root."""

import difflib
import html
import re
import subprocess
import sys

PAGE = "course/modules/M/M3/project.html"
text = open(PAGE, encoding="utf-8").read()
ids = ["lab-M3-project-1", "lab-M3-project-2", "lab-M3-project-3"]
for n, lab in enumerate(ids, start=1):
    section = text[text.index(f'id="{lab}"') :]
    section = section[: section.index("</section>")]
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', section, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section, re.S).group(1))
    twin = open(f"tests/labs/M3/lab-M3-project-{n}.py", encoding="utf-8").read()
    print(f"== {lab}: page code lines {code.count(chr(10))}, twin lines {twin.count(chr(10))}")
    diff = [d for d in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm="", n=0)]
    print("\n".join(diff) if diff else "page code identical to twin")
    res = subprocess.run([sys.executable, "-I", "-W", "error", f"tests/labs/M3/lab-M3-project-{n}.py"],
                         capture_output=True, text=True)
    print("twin exit", res.returncode, "stderr:", res.stderr.strip()[:200])
    out = res.stdout.rstrip("\n")
    exp = expected.rstrip("\n")
    print("expected block equals twin output:", out == exp)
    if out != exp:
        print("\n".join(difflib.unified_diff(exp.splitlines(), out.splitlines(), "expected", "output", lineterm="", n=0)))
    print(out)
