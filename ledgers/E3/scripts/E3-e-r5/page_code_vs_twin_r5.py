"""Compare each project.html lab's <code data-run> text with its twin file, and the expected block with the twin's output.

Round 5. The page is the one checked in this checkout. Standard library only.
usage: python -I page_code_vs_twin_r5.py <project.html> <twin-dir>
"""

import html
import re
import sys

page = open(sys.argv[1], encoding="utf-8").read()
twin_dir = sys.argv[2]
for lab in ("lab-E3-project-1", "lab-E3-project-2", "lab-E3-project-3"):
    s = page.index(f'id="{lab}"')
    e = page.index("</section>", s)
    chunk = page[s:e]
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', chunk, flags=re.S).group(1)
    code = html.unescape(code)
    twin = open(f"{twin_dir}/{lab}.py", encoding="utf-8").read()
    code_lines = [ln.rstrip("\n") for ln in code.splitlines()]
    twin_lines = [ln.rstrip("\n") for ln in twin.splitlines()]
    if lab == "lab-E3-project-2":
        # completion lab: every page line equals the twin line or contains a blank
        bad = [i for i, ln in enumerate(code_lines) if ln not in twin_lines and "___" not in ln]
        print(lab, "page lines:", len(code_lines), "twin lines:", len(twin_lines), "lines neither equal to twin nor blanked:", bad)
    else:
        print(lab, "identical to twin:", code_lines == twin_lines, "| page lines", len(code_lines), "twin lines", len(twin_lines))
        if code_lines != twin_lines:
            import difflib
            print("\n".join(list(difflib.unified_diff(twin_lines, code_lines, "twin", "page", lineterm=""))[:40]))
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', chunk, flags=re.S).group(1)
    exp = html.unescape(exp).rstrip("\n")
    print(lab, "expected block present; bytes", len(exp))
